#
# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from .poium import Page
from .page_objects import PageElement
from .page_objects import PageElements

__author__ = "rinkky"

__version__ = "0.3.1"

'''
0.3.1 version update:
* add a new way to get element with context
* delete PageSelect and PageWait
'''

__author__ = "fnngj"

__version__ = "0.3.0"

'''
0.1 version update:
* page object based on selenium.

0.1.3 version update:
* adding class PageSelect

0.1.4 version update:
* adding class PageWait

0.1.5 version update:
* new common mouse operations

0.2.1 version update:
* adding appium support

0.2.2 version update:
To better fit the project, update the name is poium.

0.2.3 version update:
* adding javascript operating api

0.3.0 version update:
* Project code refactoring.
'''