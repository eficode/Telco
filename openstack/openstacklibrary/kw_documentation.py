# Copyright 2020 Eficode Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

call_connection_method = """Calls the given ``method`` of OpenStackSDKs 
[https://docs.openstack.org/openstacksdk/latest/user/connection.html#openstack.connection.Connection|connection object]
using the ``args`` and ``kwargs`` provided.

Uses Pythons ``getattr`` to get the method from current connection object and calls it with given arguments. This allows 
using OpenStackSDK methods that don't have a keyword implementation. See all methods and their arguments in 
[https://docs.openstack.org/openstacksdk/latest/user/connection.html#openstack.connection.Connection|OpenStacks Connection documentation].

*Examples:*\n
| Call Connection Method | create_user | Robot Framework | domain_id=default |
| Call Connection Method | create_flavor | name=robotflavor | ram=4000 | vcpus=2 | disk=20 | ephemeral=10 | swap=2000 |
"""


close_connection = """Closes current connection. A new connection is required before library keywords can be used again."""


connect = """Creates new connection to the given cloud using clouds.yaml file and ``openstack.connect()`` factory function.

OpenStackClient looks for a file called clouds.yaml in the following locations:
- current directory
- ~/.config/openstack
- /etc/openstack
The first file found wins.

See also [https://docs.openstack.org/python-openstackclient/latest/configuration/index.html#clouds-yaml|OpenStacks documentation about clouds.yaml]

*Arguments:*\n
``cloud`` Name of the cloud as defined in clouds.yaml

*Example:*
| Connect | openstack |
"""


create_aggregate = """Creates a new [https://docs.openstack.org/nova/latest/admin/aggregates.html|host aggregate]. 
Returns a dict representing the created host aggregate.

*Arguments:*\n
``name`` Name of the host aggregate being created\n
``availability_zone`` Availability zone to assign hosts (Optional)
"""


create_flavor = """Creates a new [https://docs.openstack.org/nova/latest/user/flavors.html|flavor].

Arguments without default values are required. Arguments are given as named arguments.

*Arguments:*
| *Argument* | *Description* | *Default value* |
| name | Name of the flavor |
| ram | Memory in MB for the flavor |
| vcpus | Number of VCPUs for the flavor |
| disk | Size of local disk in GB |
| flavorid | ID for the flavor | 'auto' |
| ephemeral | Ephemeral space size in GB | 0 |
| swap | Swap space in MB | 0 |
| rxtx_factor | RX/TX factor | 1.0 |
| is_public | Make flavor accessible to the public | True |

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] describing the new flavor.

*Example:*
| Create Flavor | name=example | ram=2000 | vcpus=2 | disk=20 |
"""


create_image = """Creates a new [https://docs.openstack.org/openstacksdk/latest/user/resources/image/v2/image.html#openstack.image.v2.image.Image|Image].

All named arguments are optional.

*Positional arguments:*\n
``name`` Name of the image. If it is a pathname of an image, the name will be constructed from the extensionless basename of the path.\n

*Named arguments:*\n
| *Argument* | *Type* | *Description* | *Default value* |
| filename | String | The path to the file to upload. | None |
| container | String | Name of the container in swift where images should be uploaded for import. | images |
| md5 | String | Md5 sum of the image file. Will be calculated if not given. | None |
| sha256 | String | Sha256 sum of the image file. Md5 will be calculated if not given. | None |
| disk_format | String | Disk format of the image. | default os-client-config value for the cloud |
| container_format | String | Container format of the image | default os-client-config value for the cloud |
| disable_vendor_agent | Boolean | Whether to append metadata flags to the image to inform the cloud not to expect a vendor agent to be running | True |
| wait | Boolean | If true, waits for image to be created. Defaults to true - however, be aware that one of the upload methods is always synchronous. | True |
| timeout | Number | Seconds to wait for image creation (None is forever) | 3600 |
| allow_duplicates | Boolean | If true, skips checks that enforce unique image name | False |
| meta | Dict | A dict of key/value pairs to use for metadata. Bypasses automatic type conversion. | None |
| volume | String | Name or ID or volume object of a volume to create an image from | None |

Additional kwargs will be passed as additional image metadata and will have all values converted to string except for min_disk, min_ram, 
size and virtual_size which will be converted to int.

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] of the created Image object.

*Examples:*\n
| Create Image | Empty Image |
| Create Image | example-image | filename=cirros-0.4.0-x86_64-disk.img | allow_duplicates=${True} |
"""


create_network = """Creates a [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/network.html|network].

*Arguments:*
| *Argument* | *Type* | *Description* |
| name | String | Name of the network being created |
| shared | boolean | Set the network as shared |
| admin_state_up | boolean | Set the network administrative state to up |
| external | boolean | Whether this network is externally accessible |
| provider | Dict/String | A dict of network provider options. Example: ``{ 'network_type': 'vxlan', 'segmentation_id': '1' }`` Accepts both dict and string representation of dict. |
| project_id | String | Specify the project ID this network will be created on |
| availability_zone_hints | List | A list of availability zone hints |
| port_security_enabled | boolean | Enable / Disable port security |
| mtu_size | int | Maximum transmission unit value to address fragmentation. Minimum value is 68 for IPv4, and 1280 for IPv6. |
| dns_domain | String | Specify the DNS domain associated with this network |

*Returns:*\n
The network object.

*Example:*\n
| Create Network | Robot Framework | provider={'network_type': 'vxlan', 'segmentation_id': '1'} | project_id=admin |
"""


create_project = """Creates a [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/project.html|project].

*Arguments:*\n
``name`` Name of the new project\n
``domain_id`` ID of the domain owning the project\n
``description`` (Optional) Project desription\n
``enabled`` (Optional) Boolean defining whether the project is enabled (True) or disabled (False). Default value is True.\n

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] representing the new project.
"""


create_security_group = """Creates a new [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/security-group.html|security group].

*Arguments:*\n
``name`` Name for the security group\n
``description`` Description for the security group\n
``project_id`` (Optional) Specify the project ID this security group will be created on\n

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] representing the new security group.
"""


create_security_group_rule = """Creates a new [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/security-group-rule.html|security group rule].

*Arguments:*
| *Argument* | *Type* | *Description* |
| security_group | String | The security group name or ID to associate with this security group rule. If a non-unique group name is given, an exception is raised. |
| port_range_min | int | The minimum port number in the range that is matched by the security group rule. If the protocol is TCP or UDP, this value must be less than or equal to the port_range_max attribute value. If nova is used by the cloud provider for security groups, then a value of None will be transformed to -1. |
| port_range_max | int | The maximum port number in the range that is matched by the security group rule. The port_range_min attribute constrains the port_range_max attribute. If nova is used by the cloud provider for security groups, then a value of None will be transformed to -1. |
| protocol | String | The protocol that is matched by the security group rule. Valid values are None, tcp, udp, and icmp. |
| remote_ip_prefix | String | The remote IP prefix to be associated with this security group rule. This attribute matches the specified IP prefix as the source IP address of the IP packet. |
| remote_group_id | String | The remote group ID to be associated with this security group rule. |
| direction | String | Ingress or egress: The direction in which the security group rule is applied. For a compute instance, an ingress security group rule is applied to incoming (ingress) traffic for that instance. An egress rule is applied to traffic leaving the instance. |
| ethertype | String | Must be IPv4 or IPv6, and addresses represented in CIDR must match the ingress or egress rules. |
| project_id | String | Specify the project ID this security group will be created on. |

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] representing the new security group rule.

*Examples:*\n
| Create Security Group Rule | testgroup | direction=egress | ethertype=IPv4 | project_id=admin |
| Create Security Group Rule | testgroup | port_range_min=8000 | port_range_max=9000 | protocol=tcp | remote_ip_prefix=0.0.0.0/0 | direction=ingress | project_id=admin |
"""


create_user = """Creates a new [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/user.html|user].

*Arguments:*\n
| *Argument* | *Type* | *Required* |
| name | String | Yes |
| domain_id | String | Yes |
| password | String | No |
| email | String | No |
| default_project | String (project name or id) | No | 
| enabled | Boolean (True by default) | No |
| description | String | No |

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] representing the new user.

*Examples:*\n
| Create User | Robot Framework | domain_id=default |
| ${user} | Create User | Example User | domain_id=default | password=secret |
"""


get_domain_id = """Returns domain ID as a String.

*Arguments:*\n
``domain_name`` Name of the domain\n

*Example:*\n
| ${id} | Get Domain ID | Default |
| Log | ${id} | # Logs 'default' |
"""


import_image = """Import image using [https://docs.openstack.org/glance/latest/admin/interoperable-image-import.html|Interoperable Image Import].

Creates an empty image object first using `Create Image` keyword and then imports the image content with OpenStacks interoperable image import process.

*Arguments:*\n
``name`` Name of the image. If it is a pathname of an image, the name will be constructed from the extensionless basename of the path.\n
``method`` Import method, either 'glance-direct' (default) or 'web-download'.\n
``uri`` URL of the image file, required only when using the web-download import method.\n
``store`` Used when enabled_backends is activated in glance. Value can be id of a store or a 
[https://docs.openstack.org/openstacksdk/latest/user/resources/image/v2/service_info.html#openstack.image.v2.service_info.Store|Store instance].\n
``**image_attrs`` Optional named arguments that will be passed to `Create Image` keyword. See the keyword documentation for `Create Image`.

*Example:*\n
| Import Image | example-image | method=web-download | uri=https://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img | disk-format=qcow2 | container-format=bare | md5=443b7623e27ecf03dc9e01ee93f67afe | allow_duplicates=${True} |
"""


list_flavors = """Prints a list of existing flavors in JSON format.

Output can be filtered by using the optional ``fields`` argument: only values from listed fields will be printed.

*Available fields:*
- links
- name
- description
- disk
- is_public
- ram
- vcpus
- swap
- ephemeral
- is_disabled
- rxtx_factor
- extra_specs
- id
- name
- location

*Example:*
| List Flavors | id | name |

*Output:*
| [
|    {
|        "id": "1",
|        "name": "m1.tiny"
|    },
|    {
|        "id": "2",
|        "name": "m1.small"
|    },
|    {
|        "id": "3",
|        "name": "m1.medium"
|    }
| ]
"""


update_aggregate = """Updates a [https://docs.openstack.org/nova/latest/admin/aggregates.html|host aggregate].

*Positional arguments:*\n
``aggregate`` Name or ID of the aggregate being updated\n

*Named arguments:*\n
``name`` New aggregate name\n
``availability_zone`` Availability zone to assign to hosts\n

*Returns:*\n
A dict representing the updated host aggregate

*Examples:*\n
| Update Aggregate | example | availability_zone=updated_zone |
| Update Aggregate | example | name=New Name |
| Update Aggregate | example | name=Aggregate X | availability_zone=zone_x |
"""


update_image = """Updates an [https://docs.openstack.org/openstacksdk/latest/user/resources/image/v2/image.html#openstack.image.v2.image.Image|Image].

*Arguments:*\n
``image`` Image ID or Image instance\n
``**attrs`` Image attributes to be updated as key=value pairs

*Example:*\n
| Update Image | abcd-1234 | name=updated-example |
"""


update_security_group = """Updates a [https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/security-group.html|security group].

*Positional arguments:*\n
``security_group`` Name or ID of the security group to update\n

*Named arguments:*\n
``name`` New name for the security group\n
``description`` New description for the security group\n

*Returns:*\n
A [https://github.com/Infinidat/munch|munch.Munch] describing the updated security group.

*Examples:*\n
| Update Security Group | example-group | description=Updated description |
| Update Security Group | example-group | name=Updated name |
"""