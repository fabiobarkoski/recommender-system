
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
