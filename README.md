# learning-log

A personal learning log documenting progress in software development.

## Go API

REST API built with Go and `chi` router.

### Endpoints

| Method | Path                          | Description          | Auth Header       |
|--------|-------------------------------|----------------------|-------------------|
| GET    | `/account/coins?username=`    | Get coin balance     | `Authorization`   |

### Quick Start (Docker Compose)

```bash
docker compose up --build
```

Starts the API on `http://localhost:8000` and PostgreSQL on `:5432`.

### Test Users

| Username | Auth Token | Coins |
|----------|-----------|-------|
| raj      | 123QWE    | 100   |
| alex     | 123ABC    | 200   |
| neel     | 123RTY    | 300   |

```bash
curl "http://localhost:8000/account/coins?username=raj" -H "Authorization: 123QWE"
```

### Database

- Uses PostgreSQL when `DATABASE_URL` env var is set, otherwise falls back to an in-memory mock
- Schema and seed data are embedded in the binary via `//go:embed`

## React / Next.js

Learning React and Next.js:

- **my-app**: Next.js project (bootstrapped with Create Next App)

## Data Structures & Algorithms

