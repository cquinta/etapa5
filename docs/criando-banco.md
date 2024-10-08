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

Agora para que o banco de dados funcione em conjunto com a aplicação basta incluir o código necessário no diretório ./app retirando os comentários dos seguintes trechos.

```Bash

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




@app.on_event("startup")
def on_startup():
    create_db_and_tables()






@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

```

Para persistir os dados no banco de dados adiciono o volume da seguinte forma: 

```
 postgres:
    image: postgres
    ports:
      - 5432:5432

    secrets:
      - pg_password
    environment:
      POSTGRES_USER: postgres
      POSTGRES_DB: heroes
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_password
      DB_HOST: 0.0.0.0
    volumes:
      - db_data:/var/lib/postgresql/data






volumes:
  db_data:

```







