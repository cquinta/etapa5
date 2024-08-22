# Adicionando o Banco de Dados
## Secrets 

Nossa aplicação de exemplo vai utilizar o PostgreSQL para escrever e ler informações. 

Primeiro vamos criar o secret que vai cuidar da senha.  

Na sessão ```secrets``` do compose.yml adicione o secret pg_password.
Crie no diretório raiz do seu projeto o arquivo pg_password.txt e adicione no compose.yml, na sessão supracitada as instruções para criar o secret. 

```bash
secrets:
  pg_password:
    file: ./pg_password.txt
```
**OBS** Não esqueça de incluir o pg_password.txt no seu .gitignore para que sua senha não vá aparecer no seu repositório.


Agora na sessão de ``` services ``` vamos adicionar o serviço de banco de dados utilizando a imagem oficial do Postgres

```bash
 postgres:
    image: postgres
    ports:
      - 5432:5432

    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: heroes
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_password
    secrets:
      - pg_password
```

Para podermos verificar o que está acontecendo no postgres antes de trabalharmos na aplicação para que ela escreva e leia no mesmo, vamos adicionar um gerenciador de banco de dados gráfico, o pgadmin. Para tanto, vamos configurar o secret pgadm_password.

Crie o arquivo pgadm_password.txt no diretório raiz do seu projeto e adicione o mesmo no .gitignore. Na sessão secrets do compose.yml adicione as instruções para criação do secret. 

```bash
secrets:
  pgadm_password:
    file: ./pgadm_password.txt

```
Agora adicione, na sessão ```services``` do compose.yml o serviço do pgadm

```bash
dbadmin:
    image: dpage/pgadmin4
    ports:
      - 8080:80
    environment:
      - PGADMIN_DEFAULT_EMAIL=<seu e-mail>
      - PGADMIN_DEFAULT_PASSWORD_FILE=/run/secrets/pgadm_password
    secrets:
      - pgadm_password
```

Agora para que o banco de dados funcione em conjunto com a aplicação basta incluir o código necessário no diretório ./app




