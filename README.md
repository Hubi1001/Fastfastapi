# FastAPI + PostgreSQL Integration

Aplikacja do zarządzania użytkownikami: REST API w FastAPI z bazą PostgreSQL (lub SQLite do szybkiego startu) oraz frontend w React (Vite, Tailwind CSS).

## 🧰 Stos technologiczny

- **Backend:** FastAPI, SQLAlchemy 2, Pydantic 2 (walidacja danych, w tym adresów e-mail), Uvicorn
- **Baza danych:** PostgreSQL (Docker Compose) lub SQLite
- **Frontend:** React 18, Vite, Tailwind CSS, Axios
- **Testy:** pytest + FastAPI TestClient (automatyczne), skrypt smoke testu dla działającego serwera

## 📋 Wymagania

- Python 3.12 lub 3.13
- Node.js 18+ (tylko dla frontendu)
- Docker (opcjonalnie, dla PostgreSQL)

## 🚀 Szybki start (SQLite)

```bash
pip install -r requirements.txt
cp .env.sqlite .env              # Windows: copy .env.sqlite .env
uvicorn myapi:app --reload
```

- API: `http://localhost:8000`
- Dokumentacja interaktywna (Swagger): `http://localhost:8000/docs`

## 🐘 Uruchomienie z PostgreSQL (Docker)

1. Skopiuj `.env.example` do `.env` i ustaw własne hasło w `DB_PASSWORD`.
2. Uruchom bazę danych. `docker-compose.yml` czyta te same wartości z `.env`, więc kontener i API używają tych samych danych logowania:

```bash
docker compose up -d
uvicorn myapi:app --reload
```

Baza nasłuchuje tylko na `127.0.0.1`, więc nie jest dostępna z innych komputerów w sieci.

## 🖥️ Frontend

```bash
cd frontend
npm install
npm run dev                      # Windows: można też uruchomić start.bat
```

Aplikacja działa pod adresem `http://localhost:5173`. Adres API można zmienić zmienną `VITE_API_URL` (np. w pliku `frontend/.env.local`).

## ✅ Testy

```bash
pip install -r requirements-dev.txt
pytest                           # testy automatyczne na tymczasowej bazie SQLite
```

Smoke test i dane przykładowe (wymagają uruchomionego serwera):

```bash
python test_api.py               # 20 sprawdzeń, kod wyjścia 1 przy pierwszym błędzie
python add_random_users.py 10    # dodaje 10 losowych użytkowników (Faker, polskie imiona)
```

## 📚 Endpointy API

| Metoda | Ścieżka | Opis | Kody odpowiedzi |
|--------|---------|------|-----------------|
| GET | `/` | Status API | 200 |
| GET | `/users/` | Lista użytkowników | 200 |
| GET | `/users/{user_id}` | Użytkownik po ID | 200, 404, 422 |
| POST | `/users/` | Utworzenie użytkownika | 201, 400 (zajęty e-mail), 422 (błędne dane) |
| PUT | `/users/{user_id}` | Częściowa aktualizacja | 200, 400, 404, 422 |
| DELETE | `/users/{user_id}` | Usunięcie użytkownika | 200, 404 |

Przykład body dla `POST /users/`:

```json
{
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "role": "admin"
}
```

`PUT /users/{user_id}` zmienia tylko przesłane pola; pole pominięte lub z wartością `null` pozostaje bez zmian:

```json
{
  "name": "Jan Nowak"
}
```

## 🔒 Walidacja i bezpieczeństwo

- Adres e-mail jest walidowany (`EmailStr`) i musi być unikalny; konflikt zwraca 400, a nie błąd serwera.
- Pola `name` i `role` muszą mieć od 1 do 100 znaków (tyle mieszczą kolumny w bazie).
- CORS dopuszcza tylko originy z `CORS_ORIGINS` (domyślnie serwer deweloperski Vite), bez ciasteczek.
- Hasło do bazy jest wyłącznie w `.env`, który nie trafia do repozytorium.

## 🗂️ Struktura projektu

```
Fastfastapi/
├── myapi.py              # Aplikacja FastAPI z endpointami
├── database.py           # Połączenie z bazą danych (DATABASE_URL z .env)
├── models.py             # Modele SQLAlchemy
├── schemas.py            # Schematy Pydantic z walidacją
├── tests/                # Testy automatyczne (pytest)
├── test_api.py           # Smoke test dla działającego serwera
├── add_random_users.py   # Generator przykładowych danych
├── queries.sql           # Przykładowe zapytania SQL
├── docker-compose.yml    # PostgreSQL w Dockerze
├── .env.example          # Konfiguracja PostgreSQL (wzór)
├── .env.sqlite           # Konfiguracja SQLite
├── requirements.txt      # Zależności aplikacji
├── requirements-dev.txt  # Zależności do testów i skryptów
└── frontend/             # Aplikacja React (Vite)
```

## 🔧 Rozwiązywanie problemów

### `DATABASE_URL is not set`
Brakuje pliku `.env`. Skopiuj `.env.sqlite` (SQLite) albo `.env.example` (PostgreSQL) jako `.env`.

### Problem z połączeniem do bazy danych
- Sprawdź, czy kontener działa: `docker compose ps`
- Zweryfikuj dane w pliku `.env`

### Frontend nie widzi API
- Sprawdź, czy API działa pod `http://localhost:8000`
- Jeśli frontend działa pod innym adresem, dopisz go do `CORS_ORIGINS` w `.env`

## 📝 Licencja

MIT
