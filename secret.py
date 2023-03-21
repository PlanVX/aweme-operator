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
