# Kubernetes

This folder contains files to publish the application to Kubernetes.

```bash
kubectl create namespace fortunecookies

kubectl apply -n fortunecookies -f cookies.yaml

kubectl apply -n fortunecookies -f cookies-ingress.yaml
```
