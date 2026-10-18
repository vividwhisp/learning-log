# Kubernetes Fundamentals

## What Kubernetes Does

Kubernetes is a platform for deploying and operating containerized applications across a cluster of machines. It provides a declarative API: instead of manually starting every container, an operator describes the desired state, and Kubernetes controllers work to move the actual state toward that desired state. Kubernetes does not build application images; images are typically built by a separate tool or CI pipeline and then referenced by workloads.

A Kubernetes cluster contains a control plane and worker nodes. The control plane stores cluster state and makes scheduling and coordination decisions. Worker nodes run application workloads in Pods. In a managed Kubernetes service, the provider operates some or all of the control-plane components, while the user still configures workloads, access, networking, and resources.

## Pods, Deployments, and ReplicaSets

A Pod is the smallest deployable unit in Kubernetes. A Pod contains one or more closely related containers that share a network namespace and can share storage volumes. Containers inside the same Pod can communicate through `localhost`. Pods are disposable: a Pod may be replaced when a node fails, a rollout occurs, or a controller decides that replacement is needed. Applications should not rely on a Pod's IP address remaining stable.

A Deployment manages a replicated application through ReplicaSets. It is commonly used for stateless services such as HTTP APIs. The Deployment declares the desired number of replicas and a Pod template. Kubernetes creates or updates Pods to match that declaration and supports rolling updates and rollbacks.

Example Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: example/api:1.0.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
```

The Deployment selector must match the labels on its Pod template. Resource requests describe the resources Kubernetes uses for scheduling. Limits constrain resource use, with CPU throttling and memory termination behavior depending on the resource and runtime. Values should be based on observation and load testing rather than copied blindly.

## Services and Service Discovery

A Service provides a stable network endpoint for a changing set of Pods. The most common types are `ClusterIP` for cluster-internal access, `NodePort` for exposing a port on each node, and `LoadBalancer` for requesting an external load balancer when supported by the cluster environment. A Service selects backend Pods using labels. If the selector does not match any Pod labels, the Service may exist but have no usable endpoints.

Example Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - name: http
      port: 80
      targetPort: 8000
  type: ClusterIP
```

In this example, clients in the cluster connect to `api` on port 80, and traffic is forwarded to port 8000 on selected Pods. DNS-based service discovery normally lets other workloads address the Service by name.

## ConfigMaps, Secrets, and Configuration

A ConfigMap stores non-sensitive configuration data, such as feature flags or service settings. A Secret is intended for sensitive values such as credentials and tokens. A Secret is not automatically safe merely because it has a different object type: access should be restricted with RBAC, and encryption at rest should be configured where appropriate. Avoid hard-coding passwords, API keys, or database connection strings into images or public manifests.

Configuration may be exposed to a container through environment variables or mounted files. When configuration changes, whether an application sees the update immediately depends on how it is consumed and whether the process reloads it. Some changes require a Pod restart or rollout.

## Health Checks

A readiness probe answers whether a container is ready to receive traffic. A liveness probe helps Kubernetes decide whether a container is stuck and should be restarted. A startup probe gives a slow-starting application extra time before liveness or readiness checks take effect. These probes have different purposes and should not all point blindly at the same endpoint.

A readiness endpoint should reflect whether the instance can serve requests, including whether essential dependencies are available if that is part of the application's service contract. A liveness endpoint should avoid failing merely because a temporary dependency is unavailable; otherwise, the cluster can repeatedly restart healthy application processes during an external outage.

## Useful kubectl Commands

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs deployment/api
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl apply -f deployment.yaml
kubectl rollout status deployment/api
kubectl rollout undo deployment/api
```

`kubectl get` lists resources, `kubectl describe` provides detailed state and recent events, and `kubectl logs` displays container output. For a multi-container Pod, use `-c <container-name>` to select a container. When debugging a workload, check its state, events, logs, image name, resource constraints, configuration, and Service endpoints rather than assuming the application code is the only possible cause.

## Common Troubleshooting Patterns

`ImagePullBackOff` means Kubernetes is having trouble pulling an image; inspect the image reference, registry availability, and pull credentials. `CrashLoopBackOff` means a container repeatedly exits and Kubernetes is backing off before restarting it; examine current and previous logs, startup configuration, and probes. A Pod in `Pending` may be unschedulable because of resource requests, node selectors, taints, or storage constraints. A Service that cannot reach its backends often has a selector-label mismatch, incorrect target port, or an application that is not listening on the expected interface and port.

## Security and Operational Practices

Run containers with only the permissions they need. Use least-privilege RBAC, avoid privileged containers unless strictly necessary, and prefer non-root execution when the image and application support it. Keep images small and patched, pin versions deliberately, and scan images through an established security process. Use namespaces to organize workloads, but do not treat namespaces alone as a complete security boundary. Resource requests, limits, probes, logs, and rollout checks make applications easier to operate reliably.
