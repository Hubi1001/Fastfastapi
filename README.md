# FastAPI + PostgreSQL Integration

Aplikacja FastAPI zintegrowana z bazą danych PostgreSQL do zarządzania użytkownikami.

## 📋 Wymagania

- Python 3.8+
- PostgreSQL 12+
- pip

## 🚀 Instalacja

### 1. Zainstaluj PostgreSQL
Upewnij się, że masz zainstalowany PostgreSQL na swoim komputerze.

### 2. Utwórz bazę danych
```sql
-- Zaloguj się do PostgreSQL
psql -U postgres

-- Utwórz nową bazę danych
CREATE DATABASE fastapi_db;

-- Możesz też utworzyć dedykowanego użytkownika
CREATE USER fastapi_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
```

### 3. Skonfiguruj zmienne środowiskowe
Skopiuj plik `.env.example` do `.env` i uzupełnij danymi:

```bash
DB_USER=postgres
DB_PASSWORD=twoje_haslo
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
```

### 4. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

## 🏃 Uruchomienie

```bash
uvicorn myapi:app --reload
```

Aplikacja będzie dostępna pod adresem: `http://localhost:8000`

Dokumentacja API: `http://localhost:8000/docs`

## 📚 Endpointy API

### GET /
Sprawdź status API

### GET /users/
Pobierz wszystkich użytkowników

### GET /users/{user_id}
Pobierz użytkownika po ID

### POST /users/
Utwórz nowego użytkownika

Przykład body:
```json
{
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "role": "admin"
}
```

### PUT /users/{user_id}
Zaktualizuj użytkownika (częściowa aktualizacja)

Przykład body:
```json
{
  "name": "Jan Nowak"
}
```

### DELETE /users/{user_id}
Usuń użytkownika

## 🗂️ Struktura projektu

```
Fastfastapi/
├── myapi.py          # Główny plik aplikacji z endpointami
├── database.py       # Konfiguracja połączenia z bazą danych
├── models.py         # Modele SQLAlchemy
├── schemas.py        # Schematy Pydantic
├── .env              # Zmienne środowiskowe (nie w repo)
├── .env.example      # Przykładowy plik zmiennych
├── .gitignore        # Pliki ignorowane przez git
├── requirements.txt  # Zależności Pythona
└── README.md         # Ten plik
```

## 🔧 Rozwiązywanie problemów

### Problem z połączeniem do bazy danych
- Sprawdź czy PostgreSQL jest uruchomiony
- Zweryfikuj dane w pliku `.env`
- Upewnij się, że baza danych została utworzona

### Problem z importami
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Licencja

MIT
