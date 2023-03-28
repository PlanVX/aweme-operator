#  Copyright (c) 2023.  The PlanVX Authors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import yaml

secretTemplate = """
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: {secret_name}
stringData:
  config.yaml: ""
"""


def gen_config(spec, name: str) -> (str, str):
    """
    generate a secret config for aweme app
    :param spec: a dict contains config
    :param name: app name
    :return: a tuple of (secret yaml, secret name)
    """
    config = yaml.dump(spec)
    secret_name = f"aweme-app-config-{name}"
    data = yaml.safe_load(secretTemplate.format(secret_name=secret_name))
    data["stringData"]["config.yaml"] = str(config)
    return data, secret_name
