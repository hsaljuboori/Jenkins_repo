import os
import sys
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError

#added this comment to trigger an update#

config_file = sys.argv[1]
nr = InitNornir(config_file=config_file)
nr.inventory.defaults.username= os.getenv("USERNAME")
nr.inventory.defaults.password= os.getenv("PASSWORD")

def load_vars(task):
    loader = task.run(task=load_yaml, file="group_vars/all.yaml")
    task.host["facts"] = loader.result
    push_config(task)

def push_config(task):
    template = task.run(task=template_file, template="ospf.j2", path="templates")
    task.host["routing_config"] = template.result
    rendered = task.host["routing_config"]
    configuration = rendered.splitlines()
    task.run(task=send_configs, configs=configuration)
 
results = nr.run(task=load_vars)
print_result(results)
failuers = nr.data.failed_hosts
if failuers:
    raise NornirExecutionError ("Nornir Failure Detected")
