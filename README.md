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

## 🎨 Admin Dashboard

Modern admin felület a teljes rendszer kezeléséhez:

- **📊 Dashboard** - Élő statisztikák és recent activity
- **⚙️ API Settings** - API kulcsok kezelése UI-ban (nem kódban!)
- **🤖 Prompt Editor** - AI prompt sablonok szerkesztése
- **🧪 Test & Preview** - Azonnali weboldal generálás tesztelése
- **🌐 Websites & Leads** - Menedzsment nézetek

**Elérés:** `http://localhost:8000/admin` vagy `https://magyar-ai.com/admin`

## Gyors Kezdés / Quick Start

### Helyi Fejlesztés / Local Development

#### Előfeltételek / Prerequisites

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

### 🚀 Hostinger Deployment (magyar-ai.com)

**FONTOS**: A kód GitHubon van, de **manuálisan kell telepítened** a Hostinger szerverre!

#### Első Telepítés

**Részletes útmutató**: Lásd [HOSTINGER_DEPLOYMENT.md](HOSTINGER_DEPLOYMENT.md) vagy [GYORS_TELEPITES.md](GYORS_TELEPITES.md)

```bash
# 1. SSH kapcsolat
ssh username@your_server

# 2. Navigálj a domain könyvtárába
cd ~/public_html/magyar-ai.com

# 3. Clone repository (ha még nincs)
git clone https://github.com/N-Target/googlemaptowebsite.git .
git checkout copilot/add-ai-web-generator

# 4. Automatikus konfiguráció (beállítja a username-t!)
bash configure_hostinger.sh

# 5. Követd a script utasításait
```

#### ⚡ Teljes Frissítés - Egy Parancs! (Ajánlott ✨)

**Az ÚJ all-in-one script mindent csinál automatikusan:**

```bash
cd ~/public_html/magyar-ai.com
bash teljes_telepites.sh
```

**Ez a script mindent megcsinál:**
1. ✅ Pre-deployment health check (rendszer, internet, Python, disk)
2. ✅ Konfiguráció (username, paths auto-detect)
3. ✅ Git pull (legújabb kód GitHub-ról)
4. ✅ Virtual environment beállítás
5. ✅ Függőségek telepítése
6. ✅ Adatbázis inicializálás/ellenőrzés
7. ✅ .env fájl ellenőrzés
8. ✅ Passenger újraindítás
9. ✅ Post-deployment verification

**Változtatások élőben 1-2 perc múlva!** ⚡

#### 🚀 Gyors Újraindítás (Kis Változtatásokhoz)

```bash
cd ~/public_html/magyar-ai.com
bash teljes_telepites.sh restart
```

**Frissítés 10-15 másodperc múlva!** ⚡⚡⚡

#### 🔄 Fejlesztési Munkafolyamat

**Lokális gépen:**
```bash
# 1. Végezd el a módosításokat
git add .
git commit -m "Leírás"
git push origin copilot/add-ai-web-generator
```

**Hostinger szerveren:**
```bash
# 2. Teljes frissítés (ajánlott)
cd ~/public_html/magyar-ai.com
bash teljes_telepites.sh

# VAGY gyors restart (ha nincs új dependency)
bash teljes_telepites.sh restart
```

**További dokumentáció**:
- 🇭🇺 **[KOMMUNIKACIO_ES_MUNKAFOLYAMAT.md](KOMMUNIKACIO_ES_MUNKAFOLYAMAT.md)** - Teljes munkafolyamat és kommunikáció
- 🇭🇺 **[FRISSITES_UTMUTATO.md](FRISSITES_UTMUTATO.md)** - Frissítési útmutató
- 🇭🇺 **[RENDSZER_ATTEKINTES.md](RENDSZER_ATTEKINTES.md)** - Rendszer áttekintés

**503 hiba?** Futtasd: `bash teljes_telepites.sh health` vagy lásd [FIX_503_ERROR.md](FIX_503_ERROR.md)

### ☁️ Vercel Deployment (Serverless)

**Az alkalmazás most már Vercel-re is telepíthető!** ✅

⚠️ **FONTOS FRISSÍTÉS**: A Vercel deployment konfiguráció javítva! Nincs több "Secret does not exist" hiba!

#### Gyors Telepítés / Quick Deploy

1. **Import projekt Vercel-be** → [vercel.com/new](https://vercel.com/new)
2. **Válaszd a repository-t**: `N-Target/googlemaptowebsite`
3. **Környezeti változók beállítása** a Vercel Dashboard-on (Settings → Environment Variables):
   
   ⚠️ **NE a vercel.json-ban, hanem a Dashboard-on állítsd be!**
   
   ```
   DATABASE_URL=<postgresql-connection-string>
   OPENAI_API_KEY=<your-key>
   GOOGLE_MAPS_API_KEY=<your-key>
   GOOGLE_PLACES_API_KEY=<your-key>
   APP_ENV=production
   ```
4. **Deploy** → 2-3 perc múlva kész!

**Elérés**: `https://your-project.vercel.app/admin`

**Dokumentáció**:
- 📘 **Angol**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- 📗 **Magyar**: [VERCEL_JAVITAS_MAGYAR.md](VERCEL_JAVITAS_MAGYAR.md)
- 🔧 **Hibaelhárítás**: [VERCEL_FIX_SUMMARY.md](VERCEL_FIX_SUMMARY.md)

**Előnyök**:
- ✅ Automatikus HTTPS
- ✅ Global CDN
- ✅ Azonnali deployment GitHub push-ból
- ✅ Ingyenes SSL
- ✅ Nincs szerver adminisztráció
- ✅ Működő konfiguráció (javított!)

**Adatbázis**: Vercel-hez PostgreSQL szükséges:
- **Vercel Postgres** (ajánlott, beépített)
- **Supabase** (ingyenes tier)
- **Neon** (serverless PostgreSQL)

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
