# Google Map to Website - AI Website Generator & Lead System

## Áttekintés / Overview

AI-alapú automatizált weboldal-generáló és lead-szerző rendszer, amely Google Maps és Google Business adatok alapján készít professzionális weboldalakat interaktív widgetekkel és marketing automatizációval.

**An AI-based automated website generator and lead generation system** that creates professional websites based on Google Maps and Google Business data, enhanced with interactive widgets and marketing automation.

## Főbb Funkciók / Key Features

### 🌐 AI Weboldal Generálás / AI Website Generation
- Automatikus weboldal-készítés Google Maps adatok alapján
- AI-vezérelt tartalom generálás (OpenAI GPT-4)
- SEO-optimalizált kimenetek
- Többnyelvű támogatás (magyar, angol, német, francia, spanyol, olasz)

### 📊 Lead Menedzsment / Lead Management
- Automatikus lead gyűjtés
- Lead státusz követés
- Aktivitás naplózás
- Testreszabható mezők és címkék

### 🎨 Interaktív Widgetek / Interactive Widgets
- Kapcsolati űrlapok
- AI chatbot
- Időpontfoglalás
- Google Maps integráció
- Értékelések megjelenítése

### 📧 Marketing Automatizáció / Marketing Automation
- Email kampányok
- Lead szegmentáció
- Kampány követés (megnyitások, kattintások)
- Analitika dashboard

## Gyors Kezdés / Quick Start

### Előfeltételek / Prerequisites

```bash
# Python 3.9+
python --version

# Virtual environment (ajánlott)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# vagy / or
venv\Scripts\activate  # Windows
```

### Telepítés / Installation

```bash
# Függőségek telepítése
pip install -r requirements.txt

# Környezeti változók beállítása
cp .env.example .env
# Szerkeszd a .env fájlt az API kulcsokkal
```

### Konfiguráció / Configuration

Szerkeszd a `.env` fájlt:

```env
# API Keys (kötelező AI funkcióhoz)
OPENAI_API_KEY=your_openai_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Database
DATABASE_URL=sqlite:///./googlemaptowebsite.db

# Nyelv / Language
DEFAULT_LANGUAGE=hu
```

### Adatbázis Inicializálás / Database Initialization

```bash
# Adatbázis táblák létrehozása
python init_db.py
```

### Indítás / Running

```bash
# Fejlesztői módban
python main.py

# Vagy uvicorn használatával
uvicorn main:app --reload

# Az alkalmazás elérhető: http://localhost:8000
# API dokumentáció: http://localhost:8000/docs
```

## API Használat / API Usage

### Weboldal Generálás / Generate Website

```bash
curl -X POST "http://localhost:8000/api/v1/generator/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Kovács Étterem",
    "address": "Budapest, Andrássy út 1",
    "language": "hu",
    "include_widgets": true
  }'
```

### Lead Létrehozás / Create Lead

```bash
curl -X POST "http://localhost:8000/api/v1/leads/" \
  -H "Content-Type: application/json" \
  -d '{
    "website_id": 1,
    "name": "Nagy János",
    "email": "nagy.janos@example.com",
    "phone": "+36301234567",
    "message": "Szeretnék időpontot foglalni",
    "source": "contact_form"
  }'
```

### Widget Hozzáadás / Add Widget

```bash
curl -X POST "http://localhost:8000/api/v1/widgets/" \
  -H "Content-Type: application/json" \
  -d '{
    "website_id": 1,
    "widget_type": "contact_form",
    "name": "Kapcsolati Űrlap",
    "configuration": {
      "fields": ["name", "email", "phone", "message"],
      "email_notification": true
    },
    "position": "bottom"
  }'
```

### Marketing Kampány / Marketing Campaign

```bash
curl -X POST "http://localhost:8000/api/v1/marketing/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Üdvözlő Email",
    "campaign_type": "email",
    "subject": "Köszönjük az érdeklődését!",
    "content": "Tisztelt Ügyfelünk...",
    "target_criteria": {
      "status": "new"
    }
  }'
```

## Architektúra / Architecture

```
├── app/
│   ├── api/
│   │   └── routes/          # API végpontok
│   ├── core/                # Konfiguráció
│   ├── db/                  # Adatbázis
│   ├── models/              # Adatmodellek
│   ├── services/            # Üzleti logika
│   └── templates/           # HTML templates
├── static/                  # Statikus fájlok
│   └── generated/           # Generált weboldalak
├── main.py                  # Alkalmazás belépési pont
└── requirements.txt         # Python függőségek
```

## Technológiai Stack / Technology Stack

- **Backend**: FastAPI (Python)
- **AI**: OpenAI GPT-4
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Google APIs**: Google Maps, Google Places
- **Marketing**: Email automation, Lead tracking

## Deployment (EU/Hungary)

### Hostinger Deployment (magyar-ai.com)

**Részletes útmutató**: Lásd [HOSTINGER_DEPLOYMENT.md](HOSTINGER_DEPLOYMENT.md)

Gyors lépések:
```bash
# 1. SSH kapcsolat
ssh username@magyar-ai.com

# 2. Navigálj a domain könyvtárába
cd ~/public_html/magyar-ai.com

# 3. Virtual environment létrehozása
python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate

# 4. Függőségek telepítése
pip install -r requirements.txt

# 5. Konfiguráció
cp .env.example .env
nano .env  # Szerkeszd az API kulcsokkal

# 6. Adatbázis inicializálás
python init_db.py

# 7. .htaccess és passenger_wsgi.py frissítése a felhasználóneveddel

# 8. Újraindítás
mkdir -p tmp && touch tmp/restart.txt
```

**503 hiba megoldása**: Ellenőrizd a `passenger_wsgi.py` és `.htaccess` fájlokban a felhasználónevet és útvonalakat.

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build és futtatás
docker build -t googlemaptowebsite .
docker run -p 8000:8000 --env-file .env googlemaptowebsite
```

### Gyors Deployment Konfiguráció

A rendszer rövid ciklusidővel működik:
- Hostinger shared hosting támogatás
- Docker/Kubernetes deployment
- Automatikus CI/CD pipeline
- Környezeti változók alapú konfiguráció
- Zero-downtime deployment
- EU-GDPR kompatibilis

## Widget Típusok / Widget Types

| Típus | Leírás | Használat |
|-------|--------|-----------|
| `contact_form` | Kapcsolati űrlap | Lead gyűjtés |
| `chatbot` | AI chatbot | Automata ügyfélszolgálat |
| `booking` | Időpontfoglalás | Szolgáltatások |
| `map` | Google Maps | Helymeghatározás |
| `reviews` | Értékelések | Social proof |

## Lead Státuszok / Lead Statuses

- `new` - Új lead
- `contacted` - Kapcsolatba lépve
- `converted` - Konvertálva
- `lost` - Elveszett

## Marketing Kampány Típusok / Campaign Types

- `email` - Email kampány
- `sms` - SMS kampány
- `notification` - Push értesítés

## Fejlesztés / Development

```bash
# Tesztek futtatása
pytest

# Code style ellenőrzés
flake8 app/
black app/

# Adatbázis migráció
alembic upgrade head
```

## Licensz / License

MIT License

## Támogatás / Support

- GitHub Issues: [N-Target/googlemaptowebsite](https://github.com/N-Target/googlemaptowebsite)
- Dokumentáció: `/docs` endpoint

## Changelog

### v1.0.0 (2024)
- Kezdeti verzió AI weboldal generálással
- Lead menedzsment rendszer
- Interaktív widgetek
- Marketing automatizáció
- Többnyelvű támogatás (HU, EN, DE, FR, ES, IT)
