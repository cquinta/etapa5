# Empacotando um app
## Construção do Reposítório de Código

Primeiro vamos construir o repositório de código da imagem. Para realizar esta tarefa vamos utilizar o GitHub. 
É possível criar o repositório vazio através da interface web ou através client do git. 

Primeiro configure sua identidade no GitHub

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --list

```

Inicialize o repositório a ser criado.

```bash
cd /path/to/your/project
git init

```
Esta etapa cria um diretório .git no diretório do seu projeto.

Crie um arquivo README.MD, adicione-o a staging area e faça o seu primeiro commit

```bash
touch README.MD
git add .
git commit -m"first commit"

```

Adicione o repositório remoto a ser criado no GitHub
```bash
git remote add origin https://github.com/cquinta/<seurepositorio>.git

git push --set-upstream origin main

git push
```

**OBS** Para que o repositório seja criado com sucesso é necessário estar logado no git e para isso é preciso criar um token para isso veja a documentação [aqui](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

## Criação do ambiente de trabalho DEV

O exemplo a seguir mostra a criação de um ambiente de trabalho inicial para python, dependendo da linguagem de programação que você for utilizar será necessário modificar os comandos. 

Os comandos abaixo criarão e ativarão um ambiente virtual python para programação.

```bash
python3 -m venv .venv
source .venv/bin/activate
```
**OBS** para que os comandos funcionem a contento é necessário ter o python instalado, mais informações [aqui](https://www.python.org/downloads/)

Apos a execução do comando acima seu shell vai apresentar o (.venv) conforme abaixo: 
```bash

(.venv) cquinta@BOOK-KE5DF3VR3U:~/infnet/sandbox/docrepo
```

Agora vamos criar nosso primeiro app, para isso criaremos um diretório app
```bash
mkdir ./app
cd app
```
E dentro dele um arquivo app.py com o seguinte conteúdo

```
from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```
Será necessário instalar o módulo fastapi e o uvicorn no python.
```bash
pip install fastapi
pip install uvicorn
pip freeze > requirements.txt
```
O último comando vai gerar um arquivo requirements.txt com todos os módulos nas suas versões instaladas. 
Agora vamos iniciar nossa aplicação pela primeira vez

```bash
uvicorn app:app --host=0.0.0.0 --port=8000
```
Em outro terminal utilize o comando curl para ver o resultado 
```bash
curl http://localhost:8000

```
## Empacotando a nossa Primeira aplicação

Agora vamos criar uma imagem docker com a nossa aplicação

Primeiro vamos desativar o virtual environment do python, pois não iremos utilizado por hora e vamos para a pasta raiz do nosso projeto.
```bash
deactivate
cd ..
ls 
```
O resultado dos comandos acima deve ser semelhante ao seguinte: 

```bash
$ deactivate
$ cd ..
$ ls
README.MD  app

```
Agora vamos criar um arquivo Dockerfile, no diretório raiz do nosso projeto, com o seguinte conteúdo: 
```bash
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base
WORKDIR app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app .
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

Vamos construir nossa imagem e rodar nosso container pela primeira vez verificar o resultado

```bash
docker build -t <repositorio>/<imagem>:v0.1
docker container run --rm -p 8000:8000  <repositorio>/<imagem>:v0.1
curl http://localhost:8000
```
PRONTO !! containerizamos nosso primeiro app. 

## Pipeline
Agora vamos automatizar via git actions a construção e o upload da imagem para o Docker Hub. 

Na raiz do seu repositório crie o diretório .github e dentro dele o diretório workflows, dentro deste último crie um arquivo .yml com o nome que desejar, no nosso caso será dockerimage.yml, com o seguinte conteúdo. 

No exemplo o action ocorrera no branch master. 

```bash
name: Docker Image CI

on:
  push:
    branches:
      - master
    tags:
      - "v*.*.*"
  

jobs:

  build:

    runs-on: ubuntu-latest

    
    steps:
      - name: check repository
        uses: actions/checkout@v4

      - name: login to docker registry
        uses: docker/login-action@v3
        with:
          username: ${{secrets.DOCKERHUB_USERNAME}}
          password: ${{secrets.DOCKERHUB_TOKEN}}
            
      - name: build and push docker image to registry
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          platforms: linux/amd64
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/${{ github.event.repository.name }}:${{ github.ref_name }}
```

Antes de fazer o add não esqueça de criar, na raiz do seu repositório os arquivos .gitignore e .dockerignore e inclua, no primeiro tudo que não deve ir para o repositório no github e no segundo tudo que não deve ser copiado para dentro da imagem. 

Agora faça o add, o commit e o push para o GitHub. 

```bash
git add .
git commit -m"criando a pipeline de contrução e push da imagem"
git push

```
Verifique no GitHub se a construção da imagem e o push para o Docker Hub ocorreram com sucesso. 

**OBS** Para que esta ação funcione é necessário:

* Possuir conta e senha no DockerHub
* Criar um token no DockerHub [Documentação aqui](https://docs.docker.com/security/for-developers/access-tokens/)
* Criar no repositório do github, os dois segredos: secrets.DOCKERHUB_USERNAME e secrets.DOCKERHUB_TOKEN [Documentação aqui](https://docs.github.com/pt/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

Após testar o funcionamento modifique a instrução "on" para workflow_call ( só pode ser chamado a partir de outro workflow) para que a pipeline não fique rodando em todos os pushs. 

Para um melhor entendimento dos gatilhos para as actions veja [aqui](https://docs.github.com/pt/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)







