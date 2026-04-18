# Guia de Versionamento
Para permitir o ORM das classes do python para os relacionamentos banco de dados, são utilizados o SQLAlchemy em conjunto com o Alembic. Os passos para realizar corretamente a migração serão descritos abaixo.

## Setup
Essas são as coisas feitas nos arquivos relacionados ao alembic para a conexão com o neon postgre

### Arquivos pessoais

#### backend/core/settings.py
``` Python

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str 
    DB_HOST: str
    DB_NAME: str 

    model_config = SettingsConfigDict(env_file="../.env")

    def get_neonsql_link(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}?sslmode=require&channel_binding=require"
    
settings = Settings()
```

#### backend/db/connection.py

``` Python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from core.settings import settings

db_engine = create_engine(settings.get_neonsql_link(), echo=False, future=True)
Base = declarative_base()
```

#### backend/models/__init__.py

``` Python
from .constallation import Constallation
from .star import Star
from .starsEdge import StarsEdge
```

### Tratamento nos arquivos do Alembic

#### alembic.ini

Descomentar file_template (opcional):
``` alembic.ini
# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

Comentar sqlalchemy.url:
``` alembic.ini
# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

#### alembic/env.py

Importar os módulos:
```Python
import sys
import os
from logging.config import fileConfig
from alembic import context

from db.connection import Base, db_engine
from core.settings import settings
from models import *
```

Relizar configurações iniciais:
```Python
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

Alterar funções de migração:
```Python
def run_migrations_offline() -> None:
    url = settings.get_neonsql_link()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = db_engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## Operacional

### Revision
Sempre que alterações nas classes forem realizadas, verificadas e consolidadas; deve se rodar o seguinte commando na pasta backend:

```bash
alembic revision --autogenerate -m "comentário sobre a migração"
```

Esse comando deve criar um arquivo em backend/alembic/versions, com seu momento de criação junto do comentário, como:

2026_01_06_19_48-8090132ef6f5_initial_migration.py

### Upgrade
Após essas alterações, podemos realizar a migração dos metadados das relações para o banco de dados, por meio do comando:

```bash
alembic upgrade head
```

### Downgrade
Caso notado erro no arquivo de migração após o upgrade já ter sido realizado, podemos executar o seguinte comando para reverter a última migração e realizar a alterações necessárias em backend/alembic/versions

```bash
alembic downgrade -1
```

Se desejarmos efetivamente abandonar alguma migração, devemos excluir sua representante em versions e todas as pastas __pycache__ em backend/alembic.