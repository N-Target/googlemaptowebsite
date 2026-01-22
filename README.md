# Google Maps to Website - AI-Powered Website Generator

Egy AI-alapú, automatizált weboldal-generáló és lead-szerző rendszer, amely a Landingsite.ai alapjaira épül, de kibővítve globális trend-elemzéssel, interaktív widgetekkel és marketing automatizációval.

## 🎯 Áttekintés

A rendszer luxus-pozicionált, rövid ciklusidővel működik, fókuszban a szépségipar (pl. fodrászok) és autószerviz iparágak, kezdeti rollout Magyarországon és az EU-ban.

### Kulcselvek

- **Integráltság**: Minden marketing igény (ScoreApp logik, luxus design) technikai háttere (Smart Crop AI, Agent-alapú szövegírás)
- **Költséghatékonyság**: Token-optimalizált működés és AI-váltó logika (Gemini Flash egyszerű feladatokra, GPT-4o komplexekre)
- **Felhasználói Élmény**: Satori-élmény – gyors, hangalapú, kódmentes (pl. Voice-to-JSON Editor)
- **Üzleti Modell**: Starter (ingyenes demo), A-Plan (egyszeri díj), B-Plan/Luxury Leap (havi előfizetés korlátlan tokennel)

## 🚀 Főbb Funkciók

### 1. AI-Powered Website Generation
- Google Maps üzletadatok automatikus importálása
- AI-generált professzionális szövegek (magyar, angol, német)
- Iparág-specifikus luxus dizájn sablonok
- Automatikus SEO optimalizáció

### 2. Intelligens AI Model Váltás
- **Gemini Flash**: Egyszerű feladatok (szövegformázás, egyszerű fordítás)
- **GPT-4o**: Komplex feladatok (kreatív szövegírás, trend-elemzés)
- Automatikus token költség optimalizáció

### 3. Smart Crop AI
- Automatikus képvágás és optimalizáció
- Responsive image set generálás
- Web-optimalizált fájlméretek

### 4. Voice-to-JSON Editor
- Hangalapú adatbevitel
- Automatikus strukturált JSON konverzió
- Kapcsolati űrlap kitöltés hangvezérléssel

### 5. Globális Trend Elemzés
- Iparág-specifikus trend monitoring
- Konkurencia elemzés
- Akcionálható ajánlások

### 6. Lead Management
- Automatikus lead rögzítés
- ScoreApp logika integráció
- Email/SMS automatizáció (tervezett)

### 7. Üzleti Tervek

#### Starter Plan (Ingyenes)
- 1,000 AI token
- 1 weboldal
- Alapvető funkciók
- Email támogatás

#### A-Plan (49,900 HUF egyszeri)
- 50,000 AI token
- 5 weboldal
- Teljes AI funkciók
- Google Maps integráció

#### B-Plan (29,900 HUF/hó)
- Korlátlan AI tokenek
- Korlátlan weboldalak
- Trend analízis
- Prémium sablonok

#### Luxury Leap (99,900 HUF/hó)
- Minden B-Plan funkció
- Dedikált account manager
- Egyedi fejlesztések
- White-label opció

## 📦 Telepítés

### Előfeltételek
- Node.js 18+
- Python 3.9+
- MongoDB 6+
- OpenAI API key
- Google Gemini API key
- Google Maps API key

### Backend Telepítés

```bash
# Klónozás
git clone https://github.com/N-Target/googlemaptowebsite.git
cd googlemaptowebsite

# Node.js függőségek telepítése
npm install

# Python függőségek telepítése
pip install -r requirements.txt

# Környezeti változók beállítása
cp .env.example .env
# Szerkessze a .env fájlt az API kulcsokkal
```

### Konfiguráció

Szerkessze a `.env` fájlt:

```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
GOOGLE_MAPS_API_KEY=...
MONGODB_URI=mongodb://localhost:27017/googlemaptowebsite
JWT_SECRET=your_secure_secret_here
PORT=3000
```

### Indítás

```bash
# Fejlesztői mód
npm run dev

# Éles mód
npm start
```

Az alkalmazás elérhető: `http://localhost:3000`

## 📚 API Dokumentáció

### Authentikáció

#### Regisztráció
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "businessName": "My Salon",
  "language": "hu"
}
```

#### Bejelentkezés
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Weboldal Generálás

```http
POST /api/websites/generate
Authorization: Bearer {token}
Content-Type: application/json

{
  "businessName": "Szépség Szalon",
  "location": "Budapest",
  "businessType": "beauty",
  "language": "hu"
}
```

### Lead Létrehozás

```http
POST /api/leads
Content-Type: application/json

{
  "websiteId": "website_id_here",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+36301234567",
  "message": "Időpontot szeretnék foglalni"
}
```

### Előfizetés Kezelés

```http
GET /api/subscriptions/plans

POST /api/subscriptions/upgrade
Authorization: Bearer {token}
Content-Type: application/json

{
  "plan": "b-plan"
}
```

## 🏗️ Architektúra

```
googlemaptowebsite/
├── src/
│   ├── config/           # Konfigurációs fájlok
│   │   └── ai.config.js  # AI model választó logika
│   ├── models/           # MongoDB modellek
│   │   ├── user.model.js
│   │   ├── website.model.js
│   │   └── lead.model.js
│   ├── controllers/      # Request handlerek
│   │   ├── auth.controller.js
│   │   ├── website.controller.js
│   │   ├── lead.controller.js
│   │   └── subscription.controller.js
│   ├── services/         # Üzleti logika
│   │   ├── ai.service.js
│   │   ├── googlemaps.service.js
│   │   └── website-generator.service.js
│   ├── routes/           # API route-ok
│   ├── middleware/       # Express middleware-ek
│   └── index.js          # Alkalmazás belépési pont
├── ai_services/          # Python AI szolgáltatások
│   ├── smart_crop.py     # Képfeldolgozás
│   ├── voice_to_json.py  # Hangfelismerés
│   └── trend_analyzer.py # Trend elemzés
├── public/
│   └── templates/        # Website sablonok
└── tests/                # Tesztek

```

## 🛠️ Technológiai Stack

### Backend
- **Node.js + Express**: REST API
- **MongoDB**: Adatbázis
- **Mongoose**: ODM
- **JWT**: Authentikáció

### AI Services
- **OpenAI GPT-4o**: Komplex szöveggenerálás
- **Google Gemini**: Gyors, költséghatékony feladatok
- **Python**: AI szolgáltatások (PIL, scipy)

### Integráció
- **Google Maps API**: Üzletadatok
- **Google Places API**: Részletes információk

## 🧪 Tesztelés

```bash
# Unit tesztek futtatása
npm test

# Python tesztek
python -m pytest ai_services/
```

## 📈 Jövőbeli Fejlesztések

- [ ] Voice-to-JSON Editor frontend
- [ ] Real-time chat widget
- [ ] A/B testing rendszer
- [ ] Analytics dashboard
- [ ] Email/SMS marketing automatizáció
- [ ] Multi-language AI support bővítése
- [ ] Advanced ScoreApp integráció
- [ ] White-label platform

## 🤝 Közreműködés

Jelenleg a projekt zártkörű fejlesztés alatt áll.

## 📄 Licenc

Copyright © 2024 N-Target. Minden jog fenntartva.

## 📞 Támogatás

Email: support@n-target.com
Web: https://n-target.com

---

**Powered by AI • Built with ❤️ in Hungary**
