# Vercel Deployment Guide / Vercel Telepítési Útmutató

## English

### Quick Deploy to Vercel

This application is now configured for Vercel deployment! Follow these steps:

#### 1. Prerequisites
- A Vercel account (sign up at [vercel.com](https://vercel.com))
- The repository connected to Vercel

#### 2. Deploy Steps

1. **Import Project to Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Select this repository: `N-Target/googlemaptowebsite`
   - Click "Import"

2. **Configure Environment Variables:**
   In Vercel dashboard, add these environment variables:
   ```
   DATABASE_URL=<your-postgresql-connection-string>
   OPENAI_API_KEY=<your-openai-key>
   GOOGLE_MAPS_API_KEY=<your-google-maps-key>
   GOOGLE_PLACES_API_KEY=<your-google-places-key>
   APP_ENV=production
   ```

3. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete (2-3 minutes)
   - Your site will be live at `https://your-project.vercel.app`

#### 3. Access Admin Panel
- Visit: `https://your-project.vercel.app/admin`
- Configure API keys if not set in environment
- Test website generation

#### 4. Database Setup
For Vercel deployment, use a PostgreSQL database:
- **Recommended:** Vercel Postgres, Supabase, or Neon
- Set `DATABASE_URL` environment variable
- Database will initialize automatically on first request

#### 5. Important Notes
- Static files are served from `/static` directory
- Serverless functions have time limits (10-60 seconds depending on plan)
- Cold starts may occur after inactivity
- For production, consider upgrading to Vercel Pro for better performance

---

## Magyar (Hungarian)

### Gyors Telepítés Vercel-re

Ez az alkalmazás most már Vercel telepítésre konfigurálva van! Kövesd ezeket a lépéseket:

#### 1. Előfeltételek
- Vercel fiók (regisztráció: [vercel.com](https://vercel.com))
- Repository összekapcsolva Vercel-lel

#### 2. Telepítési Lépések

1. **Projekt Importálása Vercel-be:**
   - Menj ide: [vercel.com/new](https://vercel.com/new)
   - Válaszd ki ezt a repository-t: `N-Target/googlemaptowebsite`
   - Kattints az "Import" gombra

2. **Környezeti Változók Beállítása:**
   A Vercel dashboard-on add hozzá ezeket a környezeti változókat:
   ```
   DATABASE_URL=<postgresql-kapcsolat-string>
   OPENAI_API_KEY=<openai-kulcs>
   GOOGLE_MAPS_API_KEY=<google-maps-kulcs>
   GOOGLE_PLACES_API_KEY=<google-places-kulcs>
   APP_ENV=production
   ```

3. **Telepítés:**
   - Kattints a "Deploy" gombra
   - Várj míg a build elkészül (2-3 perc)
   - Az oldal elérhető lesz: `https://your-project.vercel.app`

#### 3. Admin Panel Elérése
- Látogass el ide: `https://your-project.vercel.app/admin`
- Állítsd be az API kulcsokat ha nincs környezeti változóban
- Teszteld a weboldal generálást

#### 4. Adatbázis Beállítás
Vercel telepítéshez PostgreSQL adatbázist használj:
- **Ajánlott:** Vercel Postgres, Supabase, vagy Neon
- Állítsd be a `DATABASE_URL` környezeti változót
- Az adatbázis automatikusan inicializálódik az első kérésnél

#### 5. Fontos Megjegyzések
- A statikus fájlok a `/static` könyvtárból szolgáltatva vannak
- A serverless funkcióknak van időkorlátjuk (10-60 másodperc, terv függvényében)
- "Cold start" előfordulhat inaktivitás után
- Éles használatra fontold meg a Vercel Pro előfizetést a jobb teljesítményért

---

## Technical Details / Technikai Részletek

### Files Added for Vercel
- `vercel.json` - Vercel configuration
- `api/index.py` - ASGI entrypoint for Vercel
- `.vercelignore` - Files to exclude from deployment

### Compatibility
✅ Works with existing Hostinger deployment
✅ Maintains all features (admin, API, widgets, leads)
✅ Supports both SQLite (dev) and PostgreSQL (production)

### Troubleshooting / Hibaelhárítás

**Problem:** Build fails with "No flask entrypoint found"
**Solution:** Make sure `api/index.py` exists and imports from `main.py`

**Problem:** 500 errors on deployment
**Solution:** Check Vercel logs and ensure all environment variables are set

**Problem:** Database connection errors
**Solution:** Verify `DATABASE_URL` is set correctly in Vercel dashboard

**Problem:** Static files not loading
**Solution:** Ensure `/static` directory exists and contains required files

For more help, check:
- Vercel docs: [vercel.com/docs](https://vercel.com/docs)
- Project README: [README.md](./README.md)
- Admin Panel Guide: [ADMIN_PANEL_GUIDE.md](./ADMIN_PANEL_GUIDE.md)
