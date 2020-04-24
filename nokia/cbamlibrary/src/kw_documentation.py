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

connect_to_cbam = """Initializes connection with the CBAM REST API.

Gets authentication tokens required for accessing the API and creates a library connection object
which handles the requests. After initialization the tokens will be refreshed automatically when 
they expire. 

Arguments can also be provided with .env file located in the same directory, to prevent
secrets from being added to test logs on trace level. If both .env file and keyword argument are
given for the same argument, the keyword argument wins. It is possible to provide some arguments,
e.g. host and client_id as keyword arguments and use .env for the remaining client_secret by omitting 
it from keyword arguments.

*Arguments:*\n
``host`` CBAM host address\n
``client_id`` CBAM Client ID\n
``client_secret`` CBAM Client secret\n
``catalog_version`` Catalog API version, SOL005 by default. Supported versions are 'SOL005' and 'v18'\n
``kwargs`` Additional keyword arguments for [https://2.python-requests.org/en/v2.9.1|python requests],
e.g. [https://2.python-requests.org/en/v2.9.1/user/advanced/#ssl-cert-verification|SSL Cert verification] (see examples below).
These kwargs will be used for all requests made by the connection.

*.env file example:*\n
| HOST=localhost
| CLIENT_ID=robot
| CLIENT_SECRET=r0b07

*Examples:*\n
_Using keyword arguments_
| Connect To CBAM | host=localhost | client_id=robot | client_secret=r0b07 |
_Using .env file only_
| Connect To CBAM |
_Using combination of keyword arguments and .env file_
| Connect To CBAM | host=127.0.0.1 |
_Using Catalog API version 18_
| Connect To CBAM | catalog_version=v18 |
_Using .env file and requests configuration kwargs (Disable SSL Cert verification)_
| Connect To CBAM | verify=${False} |
"""


create_vnf = """Creates a new VNF using given VNF descriptor. Returns a JSON description of the created VNF.

*Arguments:*\n
``vnfd_id`` vnfdId of an onboarded VNF descriptor. List of all available VNFDs can be fetched using keyword `Get VNFDs`.
VNFD ID can also be taken from the return value of `Onboard VNFD` keyword.\n
``name`` Name of the created VNF\n
``description`` Optional description of the VNF

*Example return value:*\n
| {
|     "vnfInstanceName": "EXAMPLE-VNF",
|     "vnfProductName": "Example VNF",
|     "vnfSoftwareVersion": "1.0",
|     "instantiationState": "NOT_INSTANTIATED",
|     "vimConnectionInfo": [],
|     "vnfProvider": "Example",
|     "vnfdId": "example_vnfd",
|     "extensions": {
|         "security_group": [
|             "example-group"
|         ],
|         "up_core_gateway": "127.0.0.1",
|         "sig_core_gateway": "127.0.0.1",
|         "oam_gateway": "127.0.0.1",
|         "ue_sim_gateway": "127.0.0.1"
|     },
|     "vnfdVersion": "1.0",
|     "vnfConfigurableProperties": {
|         "operation_triggers": {}
|     },
|     "vnfPkgId": "example_vnfd",
|     "id": "CBAM-1234abcde56789fghijklmn",
|     "metadata": {}
| }

*Examples:*\n
| Create VNF | example-vnfd-id | Example VNF |
| Create VNF | example-vnfd-id | Example VNF | Example description |
"""


delete_vnf = """Deletes VNF by id.

*Arguments:*\n
``vnf_id`` ID of the VNF that will be deleted

*Example:*\n
| Delete VNF | CBAM-1234abcde56789fghijklmn |
"""

delete_vnfd = """Deletes VNFD by id.

*Arguments:*\n
``vnfd_id`` ID of the VNFD that will be deleted

*Example:*\n
| Delete VNFD | example-vnfd |
"""


disable_insecure_request_warning = """Disables urllib3.exceptions.InsecureRequestWarning which is printed on each 
request when SSL Cert verification is disabled.
"""


get_vnfs = """Returns a list of all VNFs.

*Example:*\n
_Log names of all VNF instances_
| ${VNFs} | Get VNFs |
| FOR | ${VNF} | IN | @{VNFs} |
| | LOG | ${VNF}[vnfInstanceName] |
| END |
"""


get_vnfds = """Returns a list of all VNFDs.

*Example:*\n
_Log names of all VNFDs_
| ${VNFDs} | Get VNFDs |
| FOR | ${VNFD} | IN | @{VNFDs} |
| | LOG | ${VNFD}[name] |
| END |
"""


modify_vnf = """Modifies existing VNF.

*Arguments:*\n
``vnf_id`` ID of the VNF that will be modified\n
``modifications`` Changes in json format. Accepts dict, string and list types, see the examples.

*Modifications model*:\n
_All fields are optional_
| {
|   "vnfInstanceName": "Example",
|   "vnfInstanceDescription": "Example",
|   "metadata": {
|     "example_key": "example value"
|   },
|   "vnfConfigurableProperties": {
|     "example_key": "example value"
|   },
|   "extensions": {
|     "example_key": "example value"
|   },
|   "vimConnectionInfo": [
|     {
|       "id": "example-abcd12345",
|       "vimType": "OPENSTACK_V3",
|       "interfaceInfo": {
|         "endpoint": "https://example.test/example"
|       },
|       "accessInfo": {
|         "username": "username",
|         "password": "password",
|         "region": "example",
|         "tenant": "example",
|         "project": "example",
|         "userDomain": "example",
|         "projectDomain": "example"
|       }
|     }
|   ]
| }

*Examples:*\n
Simple modifications are easy to do using BuiltIn
[https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Create%20Dictionary|Create Dictionary] keyword,
for example changing VNF name and description:
| &{modifications} | Create Dictionary | vnfInstanceName=Modified name | vnfInstanceDescription=Modified description |
| Modify VNF | CBAM-1234abcd5678efgh91011ijkl | ${modifications} |

However creating nested json objects with dicts can be cumbersome and non-readable, since every object needs to be created using the Create Dictionary
keyword. For example changing VNF metadata requires creating the metadata object first and then assigning that as the value for metadata
key in the outer object:
| &{metadata} | Create Dictionary | firstkey=firstvalue | secondkey=secondvalue |
| &{modifications} | Create Dictionary | metadata=${metadata} |
| Modify VNF | CBAM-1234abcd5678efgh91011ijkl | ${modifications} |

To make using nested objects easier the modifications argument also supports stringified JSON. To provide a JSON string as an argument
you can use [https://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Set%20Variable|Set Variable] keyword or 
[https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#variable-table|Variable table]. When splitting the string
on multiple lines with Set Variable, Robot handles it as a list with each row as a separate item. Library will turn these lists to string
format automatically. Here's the Set Variable version of the previous metadata example:
| ${modifications}    Set Variable
| ...  {
| ...     "metadata": {
| ...       "firstkey": "firstvalue",
| ...       "secondkey": "secondvalue"
| ...     }
| ...  }
| Modify VNF    CBAM-1234abcd5678efgh91011ijkl    ${modifications}

It is also possible to use Robot Frameworks [https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#variable-files|variable files]
which allows creating dictionaries using Python syntax.
"""


onboard_vnfd = """Uploads the VNF template package to the CBAM VNF catalog. Returns a JSON description of the VNFD.

*Arguments:*\n
``vnfd`` Path to the vnfd zip file

*Example return value:*\n
| {
|     "id": "1",
|     "name": "example_vnfd",
|     "version": "1.0",
|     "references": [],
|     "vnfdId": "example_vnfd",
|     "vimType": "openstack",
|     "provider": "Example",
|     "productName": "Example VNF",
|     "swVersion": "1.0"
| }

*Example:*\n
| ${vnfd} | Onboard VNFD | /Users/Robot/Documents/project/vnfd.zip |
| Log | ${vnfd}[vnfdId] | # Log the VNFD ID. This could be given as an argument for `Create VNF` keyword. |
"""
