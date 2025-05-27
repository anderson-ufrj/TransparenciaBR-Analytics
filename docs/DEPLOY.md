# 🚀 Guia de Deploy

Este documento descreve como fazer deploy do TransparenciaBR Analytics em diferentes ambientes.

## 📋 Pré-requisitos

### Recursos Mínimos

- **CPU**: 2 vCPUs
- **RAM**: 4GB
- **Armazenamento**: 20GB SSD
- **Bandwidth**: 10GB/mês
- **Python**: 3.8+
- **Sistema**: Ubuntu 20.04+ / CentOS 8+ / Docker

### Credenciais Necessárias

- Token da API Portal da Transparência
- Email cadastrado na API
- (Opcional) Credenciais de banco de dados
- (Opcional) Chaves de serviços em nuvem

## 🐳 Deploy com Docker (Recomendado)

### 1. Dockerfile

```dockerfile
FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando padrão
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - TRANSPARENCIA_API_TOKEN=${TRANSPARENCIA_API_TOKEN}
      - TRANSPARENCIA_EMAIL=${TRANSPARENCIA_EMAIL}
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    command: redis-server --appendonly yes

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  redis_data:
```

### 3. Executar Deploy

```bash
# Clonar repositório
git clone https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics

# Configurar variáveis de ambiente
cp .env.template .env
# Editar .env com suas credenciais

# Build e execução
docker-compose up -d

# Verificar status
docker-compose ps
docker-compose logs -f app
```

## ☁️ Deploy na AWS

### 1. EC2 com Docker

```bash
# 1. Criar instância EC2 (t3.medium recomendado)
# 2. Configurar Security Group (portas 22, 80, 443, 8501)
# 3. Conectar via SSH

# Instalar Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy da aplicação
git clone https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics
cp .env.template .env
# Configurar .env

docker-compose up -d
```

### 2. ECS (Elastic Container Service)

```json
{
  "family": "transparencia-analytics",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "transparencia-analytics:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "TRANSPARENCIA_API_TOKEN",
          "value": "seu-token-aqui"
        },
        {
          "name": "TRANSPARENCIA_EMAIL",
          "value": "seu-email@exemplo.com"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/transparencia-analytics",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:8501/_stcore/health || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### 3. Application Load Balancer

```yaml
# alb.yaml (CloudFormation)
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  ALB:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: transparencia-analytics-alb
      Type: application
      Scheme: internet-facing
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      SecurityGroups:
        - !Ref ALBSecurityGroup

  ALBListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ALBTargetGroup
      LoadBalancerArn: !Ref ALB
      Port: 443
      Protocol: HTTPS
      Certificates:
        - CertificateArn: !Ref SSLCertificate

  ALBTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: transparencia-analytics-tg
      Port: 8501
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: ip
      HealthCheckPath: /_stcore/health
```

## 🌊 Deploy no DigitalOcean

### 1. App Platform

```yaml
# .do/app.yaml
name: transparencia-analytics
services:
- name: web
  source_dir: /
  github:
    repo: anderson-ufrj/TransparenciaBR-Analytics
    branch: main
  run_command: streamlit run src/dashboard/app.py --server.port=8080 --server.address=0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 8080
  health_check:
    http_path: /_stcore/health
  envs:
  - key: TRANSPARENCIA_API_TOKEN
    value: ${TRANSPARENCIA_API_TOKEN}
  - key: TRANSPARENCIA_EMAIL
    value: ${TRANSPARENCIA_EMAIL}
```

### 2. Droplet Tradicional

```bash
# Criar droplet Ubuntu 20.04
# Conectar via SSH

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Clonar e configurar aplicação
git clone https://github.com/anderson-ufrj/TransparenciaBR-Analytics.git
cd TransparenciaBR-Analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar aplicação
cp .env.template .env
# Editar .env

# Criar serviço systemd
sudo tee /etc/systemd/system/transparencia.service > /dev/null <<EOF
[Unit]
Description=TransparenciaBR Analytics
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/TransparenciaBR-Analytics
Environment=PATH=/home/ubuntu/TransparenciaBR-Analytics/venv/bin
ExecStart=/home/ubuntu/TransparenciaBR-Analytics/venv/bin/streamlit run src/dashboard/app.py --server.port=8501 --server.address=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable transparencia
sudo systemctl start transparencia
```

## 🔧 Configuração do Nginx

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8501;
    }

    server {
        listen 80;
        server_name seu-dominio.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name seu-dominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # SSL configurations
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # Gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support for Streamlit
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
        }

        # Static files caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## 🔒 SSL/TLS (Let's Encrypt)

### Certificado Automático

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Certificado Manual

```bash
# Gerar certificado autoassinado (desenvolvimento)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem
```

## 📊 Monitoramento

### 1. Health Checks

```python
# src/dashboard/health.py
import streamlit as st
from datetime import datetime
import psutil
import requests

def health_check():
    """Endpoint de health check"""
    try:
        # Verificar memória
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            return False
        
        # Verificar API
        client = TransparenciaAPIClient(...)
        if not client.health_check():
            return False
        
        return True
    except:
        return False
```

### 2. Métricas com Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'transparencia-analytics'
    static_configs:
      - targets: ['app:8501']
    metrics_path: /metrics
    scrape_interval: 30s
```

### 3. Logs Centralizados

```yaml
# docker-compose.yml (adicionar)
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"

  # ELK Stack (opcional)
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    environment:
      - discovery.type=single-node
    volumes:
      - esdata:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push Docker image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: transparencia-analytics
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster production --service transparencia-analytics --force-new-deployment
```

### Deploy Automatizado

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Iniciando deploy..."

# Verificar ambiente
if [ -z "$ENVIRONMENT" ]; then
    echo "❌ Variável ENVIRONMENT não definida"
    exit 1
fi

# Build da imagem
echo "📦 Construindo imagem Docker..."
docker build -t transparencia-analytics:$GITHUB_SHA .

# Testes
echo "🧪 Executando testes..."
docker run --rm transparencia-analytics:$GITHUB_SHA pytest

# Deploy baseado no ambiente
case $ENVIRONMENT in
    "staging")
        echo "🔧 Deploy para staging..."
        docker-compose -f docker-compose.staging.yml up -d
        ;;
    "production")
        echo "🚀 Deploy para produção..."
        docker-compose -f docker-compose.prod.yml up -d
        ;;
    *)
        echo "❌ Ambiente desconhecido: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "✅ Deploy concluído!"
```

## 📈 Scaling e Performance

### 1. Load Balancing

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app1:
    build: .
    environment:
      - INSTANCE_ID=app1
    networks:
      - app-network

  app2:
    build: .
    environment:
      - INSTANCE_ID=app2
    networks:
      - app-network

  app3:
    build: .
    environment:
      - INSTANCE_ID=app3
    networks:
      - app-network

  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2
      - app3
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 2. Cache Distribuído

```python
# src/utils/cache.py
import redis
import json
from typing import Any, Optional

class DistributedCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
    
    def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        self.redis_client.setex(key, ttl, json.dumps(value))
```

### 3. Database Optimization

```python
# src/data/database.py
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        try:
            yield conn
        finally:
            conn.close()
```

## 🔍 Troubleshooting

### Problemas Comuns

1. **Porta já em uso**:
```bash
sudo lsof -i :8501
sudo kill -9 <PID>
```

2. **Problemas de memória**:
```bash
# Verificar uso de memória
docker stats
# Aumentar limite
docker run -m 2g transparencia-analytics
```

3. **SSL/TLS issues**:
```bash
# Verificar certificado
openssl x509 -in cert.pem -text -noout
# Testar conectividade
curl -k https://seu-dominio.com/_stcore/health
```

4. **API rate limiting**:
```bash
# Verificar logs
docker-compose logs app | grep "rate"
# Ajustar configuração
REQUESTS_PER_MINUTE=20
```

### Logs de Debug

```bash
# Docker Compose
docker-compose logs -f --tail=100

# Kubernetes
kubectl logs -f deployment/transparencia-analytics

# Systemd
sudo journalctl -u transparencia -f
```

## 📱 Deploy Mobile/PWA

### Configuração PWA

```json
// public/manifest.json
{
  "name": "TransparenciaBR Analytics",
  "short_name": "TransparenciaBR",
  "description": "Análise de dados do Portal da Transparência",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#FFFFFF",
  "theme_color": "#047857",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## 🎯 Checklist de Deploy

- [ ] **Ambiente configurado**
  - [ ] Recursos de servidor adequados
  - [ ] Dependências instaladas
  - [ ] Credenciais configuradas
  
- [ ] **Segurança**
  - [ ] SSL/TLS configurado
  - [ ] Firewall configurado
  - [ ] Secrets gerenciados adequadamente
  - [ ] Headers de segurança
  
- [ ] **Performance**
  - [ ] Cache configurado
  - [ ] Gzip habilitado
  - [ ] CDN configurado (se aplicável)
  - [ ] Load balancer (se aplicável)
  
- [ ] **Monitoramento**
  - [ ] Health checks funcionando
  - [ ] Logs configurados
  - [ ] Métricas coletadas
  - [ ] Alertas configurados
  
- [ ] **Backup**
  - [ ] Dados importantes protegidos
  - [ ] Estratégia de backup definida
  - [ ] Recovery testado

Este guia cobre os principais cenários de deploy. Para casos específicos, consulte a documentação da plataforma escolhida.