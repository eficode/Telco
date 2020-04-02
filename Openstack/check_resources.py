import openstack, json, argparse, os
from jira_issue import create_jira_issue

def get_nsd_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("nsd_path", help="Path to json file containing NSD configuration")
    return parser.parse_args().nsd_path

def create_connection():
    return openstack.connect(cloud="openstack")

def get_flavors_from_nsd(nsd_path):
    """Returns a list of all flavor keys in given network service descriptor"""
    requested_flavors = []
    with open(nsd_path) as nsd_file:
        data = json.load(nsd_file)
        print("Flavors required in ", nsd_path, ":", sep="")
        try:
            for vnfd in data['vnfd']:
                flavors = [flavor["flavour_key"] for flavor in vnfd["deployment_flavour"]]
                requested_flavors.extend(flavors)
                print("  -", vnfd['name'], ": ", ", ".join(flavors), sep="")
        except KeyError as e:
            raise ValueError("NSD json is missing key: " + str(e)) from None
        except TypeError as e:
            raise ValueError("NSD json is invalid. Exception message: " + str(e)) from None
    return requested_flavors

def get_system_requirements_for_flavors(requested_flavors):
    """Sums resource requirements of all requested flavors and returns them in a dict"""
    requirements = {
        "ram": 0,
        "vcpus": 0,
        "disk": 0
    }
    for requested_flavor in requested_flavors:
        flavor = get_flavor_by_name(requested_flavor)
        add_requirement(requirements, flavor)
    print("Resources required by all flavors combined:")
    for key, value in requirements.items():
        print("  ", key, ": ", value, sep="")
    return requirements

def get_flavor_by_name(name):
    flavors = connection.compute.flavors()
    for flavor in flavors:
        if flavor.name == name:
            return flavor
    raise ValueError("No flavor was found with name: " + name)

def add_requirement(requirements, flavor):
    # Swap can be empty, check and set value to 0 if it is
    swap = 0 if not flavor.swap else flavor.swap
    requirements["ram"] = requirements["ram"] + flavor.ram
    requirements["vcpus"] = requirements["vcpus"] + flavor.vcpus
    requirements["disk"] = requirements["disk"] + flavor.disk + flavor.ephemeral + swap
        
def check_hypervisor_resources(requirements):
    """Checks if there is a hypervisor with available resources matching NSDs requirements"""
    hypervisors = connection.compute.hypervisors(details=True)
    for hypervisor in hypervisors:
        if (hypervisor["memory_free"] >= requirements["ram"] and
            hypervisor["vcpus"] - hypervisor["vcpus_used"] >= requirements["vcpus"] and
            hypervisor["local_disk_free"] >= requirements["disk"]):
            print_hypervisor_info(["id", "name", "memory_free", "vcpus", "vcpus_used", "local_disk_free"], hypervisor)
            return hypervisor
    # If method has not returned before getting here, there are no hypervisors with enough resources available. Create issue and raise error.
    generate_jira_issue(requirements)
    raise ValueError("No hypervisor with required resources available")

def generate_jira_issue(requirements):
    build_name = os.environ.get("BUILD_DISPLAY_NAME", "<Build number>")
    branch = os.environ.get("BRANCH_NAME", "<Branch name>")
    build_url = os.environ.get("BUILD_URL", "<Build url>")
    create_jira_issue("TEST - Build " + build_name + " on " + branch + " failed", 
                        "Build " + build_name + " on branch " + branch + " failed because no hypervisor with required " +
                        "resources was available.\n" + build_url + "\n\nRequirements:\n" + str(requirements))

def print_hypervisor_info(keys, hypervisor):
    print("Hypervisor matching the resource requirements found:")
    for key in keys:
        print("  ", key, ": ", hypervisor[key], sep="")

if __name__ == "__main__":
    nsd_path = get_nsd_path()
    requested_flavors = get_flavors_from_nsd(nsd_path)
    connection = create_connection()
    requirements = get_system_requirements_for_flavors(requested_flavors)
    check_hypervisor_resources(requirements)
