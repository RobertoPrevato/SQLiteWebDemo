# Kubernetes

This folder contains files to publish the application to Kubernetes.

```bash
kubectl create namespace fortunecookies

kubectl apply -n fortunecookies -f cookies.yaml

kubectl apply -n common-ingress -f cookies-ingress.yaml
```

See the status of the deployment:

```bash
kubectl get pods -n fortunecookies

kubectl describe pod <pod-name> -n fortunecookies
```
