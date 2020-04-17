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
``client_secret`` CBAM Client secret

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
"""
