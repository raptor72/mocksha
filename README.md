# mocksha
File-based http mockserver

## Ussage

```
   curl -X POST -H "Content-Type: application/json" -d '{"apihelper_proxy": {"https": "socks5"}, "users_file": "users", "key3": ["u0", "u1", "u2"]}' http://127.0.0.1:8089/many_people
```

```
   curl -X POST -H "Content-Type: application/json" -d '{"apihelperproxy": {"https": "socks5"}, "users_file": "users", "key3": ["u0", "u1", "u2"]}' http://127.0.0.1:8089/many_people
```

```
   curl -X POST -H "Content-Type: application/json" -d '{"k0": {"k01": "v01"}, "k1": "v1", "k2": ["v20", "v21", "v22"]}' http://127.0.0.1:8089/many_people
```

```
   curl -X POST -H "Content-Type: application/json" -d '{"k0": {"k01": "v01"}, "k1": "v1", "k2": ["v20", "v21", "v22", "v23"]}' http://127.0.0.1:8089/many_people
```
