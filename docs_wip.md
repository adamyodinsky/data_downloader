# This file contain documentation that might be used in the future but right now is not.


### Connect to the DB UI

1. Visit http://localhost:9000
2. Fill
   1. Email/Username: `my@email.com`
   2. Password: `password`
3. Press the login button.


### Start Downloading Data


```sh
make start
```

### Create Server 
<!-- TODO: This is not tested yet, test it, make it work, and add this to db_cli -->
```sql
CREATE SERVER IF NOT EXISTS postgres2 FOREIGN
DATA WRAPPER postgres_fdw
OPTIONS (host 'timescale', dbname 'postgres', port '5432');
```
[Reference](https://www.postgresql.org/docs/current/sql-createserver.html)
