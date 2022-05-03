"""
Author: ALjuboori
"""
import os
import sys
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import ipdb

config_file = sys.agrv[1]
nr = InitNornir(config_file="config.yaml")
nr.inventory.defaults.username= os.getenv("USERNAME")
nr.inventory.defaults.password = os.getenv("PASSWORD")

def pull_info(task):
  result= task.run(task= send_command, command= "show ip ospf neighbor")
  task.host["facts"] = result.scrapli_response.genie_parse_output()
  interfaces = task.host["facts"]["interfaces"]
  for intf in interfaces:
    neighbors = interfaces[intf]["neighbors"]
    for neighbor in neighbors:
      state= neighbors[neighbor]["state"]
      return state

state_result= nr.run(task=pull_info)
for host in nr.inventory.hosts.values():
  state= state_result[f"{host}"][0].result
  assert "Full" in state, "Failid"
  print("PASSED")
ipdb.set_trace()
