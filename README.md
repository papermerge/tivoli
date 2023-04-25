# JWT Token Validator

Validates, or to be technically correct verifies cryptographic
signature of the JWT token.


Minimal docker compose file:

```
version: "3.9"
services:
  web:
    image: papermerge/tivoli:0.1.0
    ports:
     - "7000:80"
    environment:
      PAPERMERGE__SECURITY__SECRET_KEY: <your secret string>
```

## Configurations

| Name | Description | Default |
| --- | --- | --- |
| `PAPERMERGE__SECURITY__SECRET` | (**required**) The secret string | |
| `PAPERMERGE__SECURITY__TOKEN_ALGORITHM` | Algorithm used to sign the token | HS256 |
