from jinja2.environment import Template
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError

nr = InitNornir(config_file="config.yaml")


def load_vars(task):
    loader = task.run(task=load_yaml, file="group_vars/all.yaml")
    task.host["facts"] = loader.result
    push_config(task)

def push_config(task):
    template = task.run(task=template_file, template="configs.j2", path="templates")
    task.host["routing_config"] = template.result
    rendered = task.host["routing_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
 

results = nr.run(task=load_vars)
print_result(results)
failuers = nr.data.failed_hosts
if failuers:
    raise NornirExecutionError ("Nornir Failure Detected")


