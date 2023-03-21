import kopf
import kubernetes

from app import gen_app, gen_svc
from secret import gen_config


@kopf.on.create('awemeapps')
def create_fn(spec: kopf.Spec, name, namespace, logger, **kwargs):
    # create a secret
    secret = {k: v for k, v in spec.items() if k in ['api', 'jwt', 'mysql', 'redis', 'release', 's3', 'otel']}

    api = kubernetes.client.CoreV1Api()
    rf, secret_name = gen_config(secret, name=name)
    kopf.adopt(rf)
    resp = api.create_namespaced_secret(
        namespace=namespace,
        body=rf,
    )
    logger.info(f"create a secret result: {resp}")
    # create a service
    svc = gen_svc(name, target_port=80)
    kopf.adopt(svc)

    resp = api.create_namespaced_service(
        namespace=namespace,
        body=svc,
    )
    logger.info(f"create a service result: {resp}")

    # create a deployment
    api = kubernetes.client.AppsV1Api()

    deployment = gen_app(name, secret_name)
    kopf.adopt(deployment)

    resp = api.create_namespaced_deployment(body=deployment, namespace=namespace)
    logger.info(f"create a deployment result: {resp}")
