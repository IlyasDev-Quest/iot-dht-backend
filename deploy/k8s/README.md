# IoT DHT Backend - K3s Deployment Guide

FastAPI backend for IoT DHT sensors deployed on **Kubernetes (K3s)** in **Oracle Cloud Infrastructure (OCI)**.

---

## 📋 Prerequisites

- Ubuntu 20.04+ (OCI instance)
- Docker installed
- Python 3.14+
- PostgreSQL database (Aiven or self-hosted)
- Minimum: 2GB RAM, 2 vCPU
- SSH access to server

---

## 🏗️ Architecture

```
Internet (Port 30080)
         ↓
OCI Security List (Ingress: 30080/TCP)
         ↓
K3s NodePort Service (30080 → 8000)
         ↓
FastAPI Pod (Uvicorn on 8000)
         ↓
PostgreSQL Database
```

---

## ⚡ Quick Start

### 1. Install K3s

```bash
curl -sfL https://get.k3s.io | sh -

mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
chmod 600 ~/.kube/config

kubectl get nodes
```

### 2. Build & Import Image

```bash
cd ~/iot-dht-backend/app
docker build -t iot-dht-backend:latest --target prod .

docker save iot-dht-backend:latest -o /tmp/iot-dht-backend.tar
sudo k3s ctr images import /tmp/iot-dht-backend.tar
```

### 3. Create Secrets

```bash
kubectl create secret generic postgres-secret \
  --from-literal=database_url='postgresql://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require'

kubectl create secret generic app-secret \
  --from-literal=secret_key="$(openssl rand -hex 32)"
```

### 4. Deploy Application

```bash
mkdir -p ~/iot-dht-backend/k8s
cd ~/iot-dht-backend/k8s

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get pods
kubectl logs -f deployment/iot-dht-backend
```

### 5. Configure Network Access

**OCI Console → VCN → Security Lists → Default Security List:**

- Add **Ingress rule**: TCP / Port 30080 / Source 0.0.0.0/0

**Local firewall:**

```bash
sudo iptables -I INPUT -p tcp --dport 30080 -j ACCEPT
```

---

## ⚙️ Configuration

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iot-dht-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: iot-dht-backend
  template:
    metadata:
      labels:
        app: iot-dht-backend
    spec:
      containers:
        - name: iot-backend
          image: iot-dht-backend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: database_url
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: secret_key
            - name: CORS_ORIGINS
              value: '["*"]'
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
```

### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: iot-dht-backend-service
spec:
  type: NodePort
  selector:
    app: iot-dht-backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
      nodePort: 30080
```

### Optional: HTTPS with Ingress

`ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: iot-backend-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    traefik.ingress.kubernetes.io/router.entrypoints: web,websecure
spec:
  tls:
    - hosts:
        - api.yourdomain.com
      secretName: iot-backend-tls
  rules:
    - host: api.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: iot-dht-backend-service
                port:
                  number: 8000
```

`letsencrypt-issuer.yaml`

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            class: traefik
```

---

## 🔐 HTTPS Setup (Optional)

1. Install cert-manager:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
kubectl get pods -n cert-manager
```

2. Configure DNS:
   Point domain → server public IP.

3. Apply issuer and ingress:

```bash
kubectl apply -f letsencrypt-issuer.yaml
kubectl apply -f ingress.yaml
```

4. Test HTTPS:

```
https://api.yourdomain.com/health
```

---

## 📡 API Endpoints

| Endpoint | URL                             | Description    |
| -------- | ------------------------------- | -------------- |
| Health   | `/health`                       | Service health |
| Docs     | `/docs`                         | API docs       |
| Readings | `/api/v1/dht11/readings`        | Get all        |
| Latest   | `/api/v1/dht11/readings/latest` | Most recent    |
| Create   | `/api/v1/dht11/readings`        | POST           |

---

## 🧪 Example Usage

```bash
curl http://YOUR_IP:30080/health
curl http://YOUR_IP:30080/api/v1/dht11/readings/latest
```

HTTPS:

```bash
curl https://api.yourdomain.com/health
```

---

## 🔍 Monitoring & Troubleshooting

```bash
kubectl get pods
kubectl logs -f deployment/iot-dht-backend
kubectl get events --sort-by='.lastTimestamp'
```

Common fixes:

- **CrashLoopBackOff** → Check DB secret.
- **No external access** → Check OCI rule + firewall.
- **DB error** → Decode secret:

```bash
kubectl get secret postgres-secret -o jsonpath='{.data.database_url}' | base64 -d
```

---

## 🔄 Updates

```bash
docker build -t iot-dht-backend:v2 --target prod .
docker save -o /tmp/iot-dht-backend-v2.tar iot-dht-backend:v2
sudo k3s ctr images import /tmp/iot-dht-backend-v2.tar
kubectl set image deployment/iot-dht-backend iot-backend=iot-dht-backend:v2
kubectl rollout status deployment/iot-dht-backend
```

Scale:

```bash
kubectl scale deployment iot-dht-backend --replicas=3
```

---

## 🔒 Security Best Practices

- Replace `CORS_ORIGINS="*"` with actual domain.
- Enable HTTPS.
- Rotate secrets.
- Restrict OCI ingress to specific IPs.
- Use namespaces.

---

## 🧹 Cleanup

```bash
kubectl delete deployment iot-dht-backend
kubectl delete service iot-dht-backend-service
kubectl delete secret postgres-secret app-secret
/usr/local/bin/k3s-uninstall.sh
```

---

## 📄 License

MIT License
