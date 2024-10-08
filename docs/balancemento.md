# Incluindo o balanceador de carga

Vamos utilizar o nginx na porta 8081 e fazer com que ele carregue o arquivo de configuração nginx.conf para o diretório /etc/nginx/nginx.conf, através do uso do config conforme explicado anteriormente. 

No compose.yml

```bash
services:
  nginx:
    image: nginx:1.26.1-alpine
    ports:
      - 8081:8081
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
    depends_on:
      apiserver:
        condition: service_healthy
    restart: always

  apiserver:
    build:
      context: .
    image: cquinta/etapa5:latest
    
    #ports:
    #  - 8000:8000
    
    healthcheck:
      test: ["CMD", "curl", "-f" , "http://localhost:8000/"]
      interval: 1m30s
      timeout: 5s
      retries: 5
      start_period: 30s
      
        
  
  

configs:
  my_config:
    file: ./config-dev.yaml
  nginx_config:
    file: ./nginx.conf

```
Crie um arquivo nginx.conf no diretório raiz do seu projeto com a seguinte configuração.


```bash
user nginx;
worker_processes auto;

error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}   

http {
    upstream backend {
        server apiserver:8000;
}

    server{
        listen 8081;
        location / {
            proxy_pass http://backend;
        }   
    }
}
```


  