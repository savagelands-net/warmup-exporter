# warmup

This is a library for communicating with a wifi-enabled home thermostat made by Warmup. At the time of writing, this only includes the warmup 4IE.

# warmup-exporter

Warmup Prometheus exporter.

This program can scrape data from Warmup API and format it such that Prometheus can scrape it.

I designed this to run on my home kubernetes cluster but it could just as easily be run using docker.

## Install
### Kubernetes
```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: warmup-exporter
  namespace: monitoring
  labels:
    app: warmup-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: warmup-exporter
  template:
    metadata:
      labels:
        app: warmup-exporter
    spec:
      nodeSelector:
        kubernetes.io/arch: amd64
      containers:
        - name: warmup-exporter
          image: savagemindz/warmup-exporter:latest
          resources:
            requests:
              cpu: 100m
              memory: "64M"
            limits:
              cpu: 100m
              memory: "128M"
          ports:
            - containerPort: 9101
              protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: warmup-exporter-service
  namespace: monitoring
spec:
  selector:
    app: warmup-exporter
  ports:
    - name: http
      protocol: TCP
      port: 9101
      targetPort: 9101
```

### Docker
```
docker run -d -p 9101:9101 savagemindz/warmup-exporter
```
```yaml
# scrape tplink devices
scrape_configs:
  - job_name: 'warmup-exporter'
    static_configs:
      - targets:
        # IP of the exporter
        - warmup-exporter-service:9101
    params:
      username:
        - "my@warmup_email_address"
      password:
        - "my_warmup_password"
      location:
        - YOUR_LOCATION_NAME
      room:
        - YOUR_ROOM_NAME
```

## Docker Build Instructions
```
docker build -t warmup-exporter ./
```

## Forked from:

- https://github.com/ha-warmup/warmup
- https://github.com/savagemindz/tplink-powerstats