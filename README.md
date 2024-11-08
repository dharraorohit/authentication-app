# Project setup

Clone the project and run following docker compose command to start service.

```bash
docker compose up
```
Do retry same command multiple times because in some cases due to network failure, docker compose gives error.

# CURLs

Sign-up:
```
curl --location 'http://127.0.0.1:8081/signup' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "email": "test1@email.com",
    "password":"test1"
}'
```

Login:
```
curl --location 'http://127.0.0.1:8081/login' \
--header 'Content-Type: application/json' \
--data-raw '{   
    "email": "test1@email.com",
    "password":"test1"
}'
```

Hello World:
```
curl --location 'http://127.0.0.1:8081/hello-world' \
--header 'x-access-token: jwt-token-here'
```

Revoke token:
```
curl --location --request DELETE 'http://127.0.0.1:8081/revoke-token' \
--header 'x-access-token: jwt-token-here'
```

Refresh token:
```
curl --location 'http://127.0.0.1:8081/refresh-token' \
--header 'x-access-token: jwt-token-here'
```

# Notes

1) Implemented expire token mechanism by Story created_at timestamp in jwt token payload and then checked the timestamp at time of token verification.

2) Implemented Revoke token mechanism by storing a entry in TokenData table and storing the respective TokenData id in jwt token. 
To revoke token, update the TokenData's is_revoked flag to false. 
To check if the token is revoked, get TokenData id from jwt token payload and then check in TokenData table.

