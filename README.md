
# Content-Based Recommender System

API de sistema de recomendaçao, da qual possui recomendação de filmes baseada em conteúdo.

## Stack
- [Vertical Slice Architecture](https://www.milanjovanovic.tech/blog/vertical-slice-architecture)
- FastAPI
- SQLModel
- Pydantic
- Pandas

## Recomendações
Para as recomendações leva-se em consideração os filmes que o usuário avaliou, do qual presumi-se que ele assistiu, e seus atores e diretores favoritos. A partir disso o sistema recomenda os filmes.

Pontos chaves das recomendações:
- Avaliações do usuário
- Gêneros dos filmes assistidos
- Atores favoritos
- Diretores favoritos

### Todos atores e diretores

Existe uma versão que ao invés de levar em consideração os atores e diretores favoritos do usuário, baseia-se em todos os atores e diretores dos filmes que o usuário avaliou/assitiu.

## Uso
A forma mais prática de rodar o projeto é criar um arquivo `.env` baseado no `.env.example` e executar via Docker Compose.

### Ambiente de desenvolvimento
Para configurar o ambiente local de desenvolvimento:
- Instale as dependências a partir do `requirements-dev.txt`:
    ```python
    pip install -r requirements-dev.txt
    ```
- Utilize os comandos via `task` para facilitar o fluxo de desenvolvimento.

#### IMPORTANTE
Para maior [segurança](https://brokkr.net/2022/03/29/publishing-docker-ports-to-127-0-0-1-instead-of-0-0-0-0/), garanta que os serviços Docker estejam acessíveis apenas localmente. Use o IP de loopback (`127.0.0.1`) ao invés de `0.0.0.0`.

### Comandos:
| Comando | Descrição |
| ------- | --------- |  
|`task create-migration`| Cria uma migração. Exemplo: `task create-migraton "my-migration"`|
| `task migrate`| Executa a migração no banco|
| `task test`| Executa os testes|
| `task list`| Executa o linter|
| `task format` | Executa o linter e então formata o código|
|`task run-dev`|Executa o FastAPI em dev mode|
|`task run-prod`|Executa o FastAPI para produção|
|`task export-deps`|Exporta as depedencias minimas|
|`task export-deps-dev`|Exporta as depedencias com as depedencias de desenvolvimento|
|`task populate-db`|Adiciona registros localizados no `/scripts` ao banco|

### Exempo de `.env`
Caso for rodar via docker compose, por favor, coloque como server/host a identificação do serviço. Exemplo:
- Postgres -> `db`
- Redis -> `cache`
```
POSTGRES_USER=my-user
POSTGRES_PASSWORD=super-stronger123
POSTGRES_SERVER=localhost
POSTGRES_DB=movies
POSTGRES_PORT=5432
POSTGRES_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}
#alembic without async migraton
ALEMBIC_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}

REDIS_HOST=localhost
REDIS_PASSWORD=super-stronger123
REDIS_PORT=6379
# cache time in seconds
CACHE_TIME=300

#API
SECRET_KEY=super-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

#features flag
TOP_N=20
```

### Registros pré-salvos
Caso você queria apenas testar a recomendação e não deseja criar milhares de registros manualmente, execute o comando `task populate-db`, dessa maneira o comando irá executar `populate.db` dentro de `/scripts` e irá salvar no bancos registros do `movies_dataset`.

IMPORTANTE: Para o script executar sem probelmas, altere o `POSTGRES_SERVER` para `localhost`.

## Documentação API
Abaixo segue a Documentação da API, mas para uma experiencia mais interativa, considere acessar os seguintes endpoints na API:
- `API_link/docs`
- `API_link/redoc`

### Importante
Com excessão da criação de usuário e login, todos os endpoints necessitam um Authorization token.

### Autenticando
Para autenticar envie uma requisicão post para o endpoint `/users` para criar um usuário, com o seguinte payload:
```json
{
    "name": "myuser",
    "email": "myuser@email.com",
    "password": "super-stronger"
}
```

Em seguida realize o login recebendo um `access_token` em `/auth/token`. Caso sua sessão for expirar renove-a enviando o `access_token` para `refresh-token`.

### Recurso usuários

| Endpoint | Descrição                       |
| :-------- | :-------------------------------- |
| GET /users      | Lista todos os usuários |
| POST /users | Criado um novo usuário |
| GET /users/{user_id} | Lista apenas o usuário informado |
| PATCH /users/{user_id} | Altera o usuário informado |
| DELETE /user/{user_id} | Deleta o usuário informado |
| GET /users/ratings | Lista as avaliações do usuário |
| GET /users/recommendations | Lista os filmes recomendados para o usuário |
| GET /users/favorites/actors | Lista os atores favoritos do usuário |
| POST /users/favorites/actors | Adiciona um ator aos favoritos do usuário |
| GET /users/favorites/directors | Lista os diretores favoritos do usuário |
| POST /users/favorites/directors | Adiciona um diretor aos favoritos do usuário |

#### Importante
A busca de todos os usuários é feita a partir de paginação, com os seguintes query parametes: `skip` e `limit`, ao não passar tais valores, a busca retorna os primeiros 100 usuário. Exemplo de busca dos próximos 100:

```http
GET /users?skip=100&limit=100
```

### Recurso filmes

| Endpoint | Descrição                       |
| :-------- | :-------------------------------- |
| GET /movies | Lista todos os filmes |
| POST /movies | Cria um novo filme |
| GET /movies/{movie_id} | Lista apenas o filme informado |
| PATCH /movies/{movie_id} | Altera o filme informado |
| DELETE /movies/{movie_id} | Deleta o filme informado |
| GET /movies/{movie_id}/ratings | Lista as avaliações do filme informado |
| POST /movies/{movie_id}/ratings | Cria uma avaliação pro filme informado |

#### Importante
A busca de todos os filmes é feita a partir de paginação, com os seguintes query parametes: `skip` e `limit`, ao não passar tais valores, a busca retorna os primeiros 100 filmes. Exemplo de busca dos próximos 100:

```http
GET /movies?skip=100&limit=100
```

### Recurso avaliações

| Endpoint | Descrição                       |
| :-------- | :-------------------------------- |
| GET /ratings | Lista todas as avaliações |
| PATCH /ratings/{rating_id} | Altera a avaliação do usuário |
| DELETE /ratings/{rating_id} | Deleta a avaliação do usuário |

#### Importante
A busca de todos as avaliações é feita a partir de paginação, com os seguintes query parametes: `skip` e `limit`, ao não passar tais valores, a busca retorna as primeiras 100 avaliações. Exemplo de busca dos próximos 100:

```http
GET /ratings?skip=100&limit=100
```
