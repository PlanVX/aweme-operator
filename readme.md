# aweme operator

[![CI](https://github.com/PlanVX/aweme-operator/actions/workflows/ci.yaml/badge.svg)](https://github.com/PlanVX/aweme-operator/actions/workflows/ci.yaml)

这是一个 k8s operator，可以简化 aweme 在 kubernetes 集群中的部署。

## 安装

要安装这个 operator，你需要先安装 crd 定义和 operator 本身。

### 使用 kubectl 安装

首先部署 crd 定义：

```
kubectl apply -f https://github.com/PlanVX/aweme-operator/raw/master/deploy/awemeapps.yaml
```

然后部署 aweme operator：

```
kubectl apply -f https://github.com/PlanVX/aweme-operator/raw/master/deploy/operator.yaml
```

验证 operator 是否在 aweme-operator 命名空间中运行：

```
>  kubectl get deployment -n aweme-operator aweme-operator
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
aweme-operator   1/1     1            1           46s
```

## 使用

定义一个 aweme 应用：

```
apiVersion: sixwaaaay.io/v1
kind: AwemeApp
metadata:
  name: sample
spec:
  api:
    prefix: /v1
    address: :80
  mysql:
    dsn: ....
  redis:
    address:
      - .....
  s3:
    accessKey: ....
    secretKey: ....
    endpoint: ....
    bucket: ....
  jwt:
    secret: .....
    ttl: .....
  otel:
    endpoint: .....
    service: ....
    version: ......
    environment: .....
  release: true
```

然后使用 kubectl apply -f 命令来创建这个应用, 敏感信息会被储存到 secret ：

```
kubectl apply -f awemeapp.yaml
```

验证是否创建成功：

```
kubectl get aweme
```

## 清除

使用 kubectl delete -f 命令来清除这个应用，关联的 k8s 资源会自动被清除：

对于 crd 和 operator，你可以使用 kubectl delete -f 命令来清除：

```
kubectl delete -f https://github.com/PlanVX/aweme-operator/raw/master/deploy/operator.yaml
kubectl delete -f https://github.com/PlanVX/aweme-operator/raw/master/deploy/awemeapps.yaml
```
