# FastAPI Frontend

Nowoczesny interfejs użytkownika zbudowany z React + Vite + Tailwind CSS

## 🚀 Instalacja

```bash
cd frontend
npm install
npm run dev
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5173`

## 📋 Funkcjonalności

✅ Przeglądanie wszystkich użytkowników
✅ Dodawanie nowych użytkowników
✅ Edycja istniejących użytkowników
✅ Usuwanie użytkowników
✅ Wyszukiwanie po nazwie lub email
✅ Filtrowanie po roli
✅ Dwa widoki: siatka i tabela
✅ Ciemny motyw
✅ Responsywny design

## 🎨 Technologie

- **React 18** - Biblioteka UI
- **Vite** - Szybki bundler
- **Tailwind CSS** - Framework CSS
- **Axios** - HTTP client
- **Lucide React** - Ikony
- **PostgreSQL** - Baza danych (backend)

## 🔗 API Integration

Frontend komunikuje z FastAPI backend poprzez:
- `http://localhost:8000/users/` - Pobranie wszystkich użytkowników
- `http://localhost:8000/users/` (POST) - Dodanie użytkownika
- `http://localhost:8000/users/{id}` (PUT) - Edycja użytkownika
- `http://localhost:8000/users/{id}` (DELETE) - Usunięcie użytkownika

## 📁 Struktura projektu

```
frontend/
├── src/
│   ├── components/
│   │   ├── UserForm.jsx      # Modal do dodawania/edycji
│   │   ├── UserCard.jsx      # Karta użytkownika w widoku siatki
│   │   └── UserTable.jsx     # Tabela użytkowników
│   ├── App.jsx               # Główny komponent
│   ├── main.jsx              # Entry point
│   └── index.css             # Style Tailwind
├── index.html                # HTML template
├── vite.config.js            # Konfiguracja Vite
├── tailwind.config.js        # Konfiguracja Tailwind
├── postcss.config.js         # Konfiguracja PostCSS
└── package.json              # Zależności
```

## 🎯 Szybki start

1. Upewnij się, że backend FastAPI działa na porcie 8000
2. Zainstaluj zależności: `npm install`
3. Uruchom dev server: `npm run dev`
4. Otwórz `http://localhost:5173` w przeglądarce

## 🔨 Build

```bash
npm run build
```

Zbudowana aplikacja będzie w folderze `dist/`

## 📝 Licencja

MIT
