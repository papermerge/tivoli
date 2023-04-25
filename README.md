# JWT Token Validator

Validates, or to be technically correct verifies cryptographic
signature of the JWT token.


## Use it

Start with docker run command:

  docker run -e PAPERMERGE__SECURITY__SECRET_KEY=123 -p 7000:3000 papermerge/tivoli:0.1.0

Now any http request without proper `Authorization` header will return 401 Unauthorized:

    $ curl -v http://localhost:7000/some/url

    *   Trying 127.0.0.1:7000...
    * Connected to localhost (127.0.0.1) port 7000 (#0)
    > GET /some/url HTTP/1.1
    > Host: localhost:7000
    > User-Agent: curl/7.81.0
    > Accept: */*
    >
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 401 Unauthorized
    < date: Tue, 25 Apr 2023 06:52:41 GMT
    < server: uvicorn
    < www-authenticate: Bearer
    < content-length: 30
    < content-type: application/json
    <
    * Connection #0 to host localhost left intact
    {"detail":"Not authenticated"}%

"Proper" `Authorization` header looks like `Authorization: Bearer <jwt token>`, where jwt token was issued and signed with `PAPERMERGE__SECURITY__SECRET_KEY` secret.
On valid jwt token, token validator will respond with 200 OK http response code.

Minimal docker compose file:

```
version: "3.9"
services:
  web:
    image: papermerge/tivoli:0.1.0
    ports:
     - "7000:3000"
    environment:
      PAPERMERGE__SECURITY__SECRET_KEY: <your secret string>
```

## Configurations

| Name | Description | Default |
| --- | --- | --- |
| `PAPERMERGE__SECURITY__SECRET` | (**required**) The secret string | |
| `PAPERMERGE__SECURITY__TOKEN_ALGORITHM` | Algorithm used to sign the token | HS256 |
