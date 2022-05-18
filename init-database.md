# How to Initialize Database

Suppose you are just run `docker compose up` and evertithing is up

* create interactive web instance
```bash
docker compose run -i web sh
```

* Make inicial migration
```bash
./manage.py migrate
```

* If it fails comment out `values` in routes/urls.py
* Try again

* Done

