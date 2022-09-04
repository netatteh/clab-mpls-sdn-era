"""Configuration deployment for the lab environment

This script deploys the configuration for the devices in the Containerlab environment.
The current method is to generate startup-config files and store them where the
routers can take advantage of them. In the future, however, direct configuration with
Nornir/Netmiko may be desired. As such, we utilize Nornir already at this stage for
inventory management.
"""
from os.path import dirname, join
import yaml
import subprocess
import re
import argparse
from functools import reduce
import shlex

from nornir import InitNornir
from nornir.core import Nornir
from nornir.core.task import Result, Task
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result


def remove_string_prefix(string: str, prefix: str) -> str:
    """Remove a given prefix from string. If prefix is not found, no nothing."""
    if string.startswith(prefix):
        return string[len(prefix) :]


def initialize_nornir(
    lab_name: str,
    num_workers: int = 10,
) -> Nornir:
    """Initialize a Nornir instance

    Utilize the already existing Ansible inventory created by Containerlab.

    Args:
        lab_name: The name of the Containerlab topology as defined in the topology file
        num_workers:
            The maximum number of parallel processes for device connectivity
    Returns:
        A Nornir object representing the given inventory.
    """
    inventory_path = join(dirname(__file__), "clab-" + lab_name + "/")

    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": num_workers,
            },
        },
        inventory={
            "plugin": "AnsibleInventory",
            "options": {
                "hostsfile": inventory_path + "ansible-inventory.yml",
            },
        },
        core={"raise_on_error": True},
    )
    nr.inventory.defaults.platform = "juniper_junos"
    nr.inventory.defaults.username = "root"
    nr.inventory.defaults.password = "clab123"
    return nr


def render_config_template(task: Task, fabric_yaml: str, template_prefix) -> Result:
    """Render device configuration template

    Render the configuration parameters to a device specific config file
    based on the given Go configuration template. Store the results in the
    Nornir host data key 'config'

    Args:
        task: A Nornir task object
        fabric_yaml: The Containerlab topology file containing the variables
            referenced in the configuration template
        template_prefix: The prefix for the Go template files. These files
            should be located in the same directory with this script.

    Returns: A Nornir 'Result' object. The output of this function is
        saved in the Nornir host object as described above.
    """

    with open(fabric_yaml, "r") as fd:
        fabric_dict = yaml.safe_load(fd)
        lab_name = fabric_dict.get("name")

    hostname = remove_string_prefix(task.host.name, "clab-" + lab_name + "-")

    # To keep things simple, utilize existing Containerlab templating functionality.
    command_str = (
        "containerlab config -t "
        + fabric_yaml
        + " template -p ./templates -l "
        + template_prefix
        + " -f "
        + hostname
    )
    command = shlex.split(command_str)
    process = subprocess.run(command, check=True, capture_output=True)
    # The 'clab config' command output is for some reason forwarded to stderr
    config = re.findall(r"\[\[(.*?)\]\]", process.stderr.decode("UTF-8"), re.M)
    output_list = config[0].replace("\\n", "\n").replace('\\"', '"').splitlines()
    output_list_formatted = [x.rstrip()[5:] for x in output_list]
    task.host.data["config"] = output_list_formatted

    return Result(host=task.host, message="Configuration rendered.")


def configure_devices(task: Task, lab_name: str) -> Result:
    """Configure a device according to the config in task.host.data['config']"""
    hostname = remove_string_prefix(task.host.name, "clab-" + lab_name + "-")
    config_path = join(dirname(__file__), "startup_config/")
    config_list = task.host.data.get("config")
    with open(join(config_path, hostname + ".conf"), "w") as fd:
        for line in config_list:
            print(line, file=fd)
    return Result(host=task.host, message="Configuration completed successfully")


def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Containerlab config script")
    parser.add_argument(
        "configured_devices",
        type=str,
        help="A comma separated list of hostnames to generate config for",
    )
    parser.add_argument(
        "template_prefix",
        type=str,
        help="The prefix string indicating the template used for config generation",
    )

    return parser.parse_args()


def main():
    args = parse_cmd_args()
    lab_name = "sdnera"
    device_list = args.configured_devices.split(",")
    device_full_names = ["clab-" + lab_name + "-" + x for x in device_list]
    filter_terms = [F(name=x) for x in device_full_names]
    filter_object = reduce(lambda f1, f2: f1 | f2, filter_terms)
    nr = initialize_nornir(lab_name="sdnera").filter(filter_object)
    render_result = nr.run(
        task=render_config_template,
        fabric_yaml="mpls_sdn_era.clab.yml",
        template_prefix=args.template_prefix,
    )
    print_result(render_result, vars=["message"])
    print_result(nr.run(configure_devices, lab_name=lab_name), vars=["message"])


if __name__ == "__main__":
    SystemExit(main())
