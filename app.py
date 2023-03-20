import yaml

appTemplate = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aweme-app-{name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aweme
  template:
    metadata:
      labels:
        app: aweme
    spec:
      containers:
        - name: aweme-app-{name}
          image: planvx/aweme:{version}
          resources:
            limits:
              cpu: 2000m
              memory: 2048Mi
            requests:
              cpu: 100m
              memory: 128Mi
          ports:
            - containerPort: {port}
          volumeMounts:
            - name: config-volume
              mountPath: /app/configs
      volumes:
        - name: config-volume
          secret:
            secretName: {config_secret}
            items:
              - key: config.yaml
                path: config.yml 
"""

svcTemplate = """
apiVersion: v1
kind: Service
metadata:
    name: aweme-app-{name}
spec:
    selector:
        app: aweme
    ports:
        - protocol: TCP
          port: {port}
          targetPort: {target_port}
    type: LoadBalancer
"""


def gen_app(name: str, config_secret: str, port: int = 80, version: str = 'latest') -> str:
    """
    generate a deployment for aweme app crd
    :param name:  aweme app name
    :param config_secret:  secret name
    :param port: port of deployment
    :param version:  image version
    :return: an object to describe the deployment
    """
    return yaml.safe_load(appTemplate.format(port=port, version=version, name=name, config_secret=config_secret))


def gen_svc(name: str, port: str = 80, target_port: int = 8081) -> str:
    """
    generate a service for aweme app crd
    :param name: aweme app name
    :param port: port of deployment
    :param target_port: port of service
    :return: an object to describe the service
    """
    return yaml.safe_load(svcTemplate.format(port=port, target_port=target_port, name=name))
