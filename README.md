# How to start

1. Setup ingress. Go to the `ingress` directory and run:

```bash
docker compose up -d
```

2. Set environment variables. Create and add variables to `.env` in the project's root directory:
```
VIRTUAL_HOST=localhost
DB_PASS="0918240950"
DJANGO_DEBUG="True"
```

3. Run docker compose in the project's rood directory:
```bash
docker compose up
```

