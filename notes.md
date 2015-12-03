# Mongodb Notes

### Login (ix)

mongo --port [port] -u [username] -p [password] admin

### Create/Add user

- 3.x: db.createUser({user: "meetme_user", pwd: "peach-cobbler", roles: ["readWrite"]})
- 2.4: db.addUser({user: "meetme_user", pwd: "peach-cobbler", roles: ["readWrite"]})

### Other commands

- use meetme: switch to db meetme
- show users: shows all users
