# Orquestrando o deploy de uma Aplicação/Arquitetura no DockerHost

Ao invés de subir o container utilizando o client de linha de comando do docker, vamos utilizar o docker compose, que nos permitirá subir a aplicação de foram orquestrada possibilitando adicionar outros componentes (containers) e outras configurações.

## O primeiro arquivo compose.yaml

Neste primeiro arquivo, o objetivo é obter um resultado semelhante ao que obteríamos através da linha de comando do cliente docker, utilizando o docker compose. 

Na raiz do seu repositório crie um arquivo chamado compose.yaml. Vamos subir a aplicação que acabamos de criar na etapa anterior através do docker compose.

O arquivo deve ter o conteúdo similar ao seguinte: 

```bash
services:
  server:
    build:
      context: .
    image: <repositorio>/imagem
    
    ports:
      - 8000:8000

```

Para facilitar estamos incluindo o instrução build para que a imagem seja construida localmente.

Para fazer o deploy no dockerhost execute o comando: 

```bash
docker compose up --build
```

O resultado deve ser semelhante ao seguinte: 

```bash

docker compose up --build
[+] Building 10.7s (13/13) FINISHED                                                                                                                                                   docker-container:container
 => [server internal] load build definition from Dockerfile                                                                                                                                                0.0s
 => => transferring dockerfile: 271B                                                                                                                                                                        0.0s
 => WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 2)                                                                                                                              0.0s
 .
 .
 .
 => [server] resolving provenance for metadata file                                                                                                                                                         0.0s
[+] Running 2/2
 ✔ Network docrepo_default     Created                                                                                                                                                                      0.1s
 ✔ Container docrepo-server-1  Created                                                                                                                                                                      0.1s
Attaching to server-1
server-1  | INFO:     Started server process [1]
server-1  | INFO:     Waiting for application startup.
server-1  | INFO:     Application startup complete.
server-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
Teste o acesso através do comando curl localhost:8000. 

* Utilize o comando docker container ls e verifique o container com o nome do repositório e do serviço concatenados. 
* Verifique a criação da rede específica onde a aplicação vai rodar. 

Termine o deploy através do ctrl-c e depois docker compose down 

## Inclusão de variáveis de ambiente:
### Através da instrução environment

No compose.yaml

```bash
environment:
      - APP_VERSION=1.0.2
      - TOKEN=${TOKEN}
```

No app.py

```bash
import os
@app.get("/variaveis")
async def variaveis():
    variaveis = dict()
    variaveis['version'] = os.environ.get('APP_VERSION')
    variaveis['token']=os.environ.get('TOKEN')
    return {"variaveis": variaveis}

```

Faça o teste ```bash curl localhost:8000/variaveis``` primeiro sem criar a variável TOKEN e depois criando através do comando ``` export TOKEN=<valor> ``` 

### Através de arquivo de variáveis de ambiente

É possível criar um arquivo com variáveis de ambiente para ser lido na criação da imagem da seguinte forma: 
Crie, na raiz do seu projeto, um diretório chamado vars. Dentro deste diretório crie um arquivo, por exemplo dev.env, contendo suas variáveis de ambiente, por exemplo: 

```bash
BANCODEV=devdb
```
No compose.yml

```bash
env_file:
      - ./vars/dev.env
```
No app.py

```bash


@app.get("/variaveis")
async def variaveis():
    variaveis = dict()
    variaveis['version'] = os.environ.get('APP_VERSION')
    variaveis['token']=os.environ.get('TOKEN')
    variaveis['bancodev']=os.environ.get('DEVDB')
    return {"variaveis": variaveis}

```
Agora faça o teste novamente através do comando ``` curl localhost:8000/variaveis```

## Arquivos de Configuração

Crie na raiz do seu projeto o arquivo config-dev.yaml

No docker-compose. 

```bash
configs:
      - source: my_config
        target: /app/config-dev.yaml

configs:
  my_config:
    file: ./config-dev.yaml

```

No app.py
```bash
variaveis['CONFIG'] = open('/app/config-dev.yaml', "r").read()
```
Agora faça o teste novamente através do comando ``` curl localhost:8000/variaveis```

## Secrets

Informações que possuam algum nível de confidencialidade deve ser passadas através de secrets. 

Para criar um secret crie, na raiz do seu projeto um arquivo, por exemplo, api_key.txt e insira nele a chave que deseja passar para o container. 

No docker-compose 

```bash

    secrets:
      - api_key

secrets:
  api_key:
    file: ./app/api_key.txt

```

No app.py
```bash
variaveis['API_KEY'] = open('/run/secrets/api_key', "r").read()
```
Agora faça o teste novamente através do comando ``` curl localhost:8000/variaveis```

**OBS** Não esqueça de incluir o api_key.txt no seu .gitignore para que ele não vá para o repositório no github. 

Por padrão a informação estará disponível no /run/secrets do seu container, se houver necessidade de modificar este comportamente pode-se utilizar a instrução ```source``` conforme abaixo: 

```bash
secrets:
      - source: api_key
        target: /app/api_key.txt

```

