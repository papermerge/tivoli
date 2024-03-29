# Tivoli

JWT token validator is a http proxy that for every HTTP request verifies the 
presence and validity of jwt token. Also, it checks that user with ID 
`user_id` is present in database (it checks `core_user` table, column `id`).
Tivoli reads JWT token from:

- `Authorization` header
- cookie header

Regarding database, Tivoli needs only table presence of table `core_user` with
at least one column `id`.

## Use it

Start with docker run command:

    docker run
        -e PAPERMERGE__SECURITY__SECRET_KEY=123 \
        -e PAPERMERGE__DATABASE__URL=<sqlalchemy database url> \
        -p 7000:3000 papermerge/tivoli:0.3.0

For any http request without valid jwt token will return 401 Unauthorized.
JWT token can be set either as part of `Authorization` header or as part
of `PAPERMERGE__SECURITY__COOKIE_NAME` cookie (defaults to 'access_token'):

    $ curl -v http://localhost:7000/some/url

    < HTTP/1.1 401 Unauthorized


`Authorization` header format is `Authorization: Bearer <jwt token>`,
where jwt token was issued and signed with `PAPERMERGE__SECURITY__SECRET_KEY` secret.

On valid jwt token, token validator will respond with 200 OK http response code.


    $  curl -v -H 'Authorization: Bearer <valid token>' http://localhost:8000/random/url

    < HTTP/1.1 200 OK

JWT token can be passwed via cookie (by default named 'access_token'):

    $ curl --cookie 'access_token=<valid token>' http://localhost:8000/whatever/url

    < HTTP/1.1 200 OK

Minimal docker compose file:

```
version: "3.9"
services:
  web:
    image: papermerge/tivoli:0.3.0
    ports:
     - "7000:3000"
    environment:
      PAPERMERGE__SECURITY__SECRET_KEY: <your secret string>
      PAPERMERGE__DATABASE__URL: <sqlalchemy database url>
```

It support PostreSql, MySql/MariaDB, and SqlLite.

For PostgreSQL use following docker compose:

```
version: "3.9"
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
     - "7000:3000"
    environment:
      PAPERMERGE__SECURITY__SECRET_KEY: 123
      PAPERMERGE__DATABASE__URL: postgresql://postgres:123@db:5432/postgres
    depends_on:
        - db

  db:
    image: bitnami/postgresql:14.4.0
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=123

volumes:
  postgres_data:
```

For MariaDB/MySql use:

```
version: "3.9"
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
     - "7000:3000"
    environment:
      PAPERMERGE__SECURITY__SECRET_KEY: 123
      PAPERMERGE__DATABASE__URL: mysql://user:password@127.0.0.1:3306/mydatabase
    depends_on:
        - db

  db:
    image: mariadb:11.2
    volumes:
      - maria:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - 3306:3306

volumes:
  maria:
```


## Configurations

| Name                                    | Description                                         | Default       |
|-----------------------------------------|-----------------------------------------------------|---|
| `PAPERMERGE__SECURITY__SECRET`          | (**required**) The secret string used to sign token |               |
| `PAPERMERGE__SECURITY__TOKEN_ALGORITHM` | Algorithm used to sign the token                    | HS256         |
| `PAPERMERGE__SECURITY__COOKIE_NAME`     | Name of cookie which contains jwt token             | access_token  |
| `PAPERMERGE__DATABASE__URL`             | DATABASE URL                                        |sqlite:////db/db.sqlite3|
