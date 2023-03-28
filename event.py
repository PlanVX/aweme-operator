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

import kopf
import kubernetes

from app import gen_app
from app import gen_svc
from secret import gen_config


@kopf.on.create("awemeapps")
def create_fn(spec: kopf.Spec, name, namespace, logger, **kwargs):
    # create a secret
    secret = {
        k: v
        for k, v in spec.items()
        if k in ["api", "jwt", "mysql", "redis", "release", "s3", "otel"]
    }

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
    version = spec.get("otel", {}).get("version", "latest")
    deployment = gen_app(name, secret_name, version=version)
    kopf.adopt(deployment)

    resp = api.create_namespaced_deployment(body=deployment,
                                            namespace=namespace)
    logger.info(f"create a deployment result: {resp}")
