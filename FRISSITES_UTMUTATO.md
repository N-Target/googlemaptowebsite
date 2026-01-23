# Frissítési Útmutató - Magyar-AI.com

## Gyors Frissítés (1 Parancs)

Ha már telepítve van a rendszer és csak frissíteni szeretnéd:

```bash
cd ~/public_html/magyar-ai.com
bash deploy_update.sh
```

**Ennyi!** A script automatikusan:
1. ✅ Lehúzza a legújabb kódot GitHubról
2. ✅ Frissíti a függőségeket
3. ✅ Ellenőrzi az adatbázist
4. ✅ Újraindítja az alkalmazást

Várd meg 10-15 másodpercet, majd nyisd meg: **https://magyar-ai.com/admin**

---

## Első Telepítés (Ha még nincs telepítve)

### 1. lépés: Kapcsolódj SSH-n keresztül

```bash
ssh your_username@your_server
```

### 2. lépés: Navigálj a domain mappába

```bash
cd ~/public_html/magyar-ai.com
```

Vagy ha így van:
```bash
cd ~/domains/magyar-ai.com/public_html
```

### 3. lépés: Clone a repository (ha még nincs)

```bash
git clone https://github.com/N-Target/googlemaptowebsite.git .
git checkout copilot/add-ai-web-generator
```

### 4. lépés: Automatikus konfiguráció

```bash
bash configure_hostinger.sh
```

Ez a script beállítja:
- Username helyettesítés `.htaccess` és `passenger_wsgi.py` fájlokban
- Virtual environment ellenőrzés
- Adatbázis ellenőrzés
- Útmutatás a hiányzó lépésekhez

### 5. lépés: Telepítsd a függőségeket

```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
pip install -r requirements.txt
```

### 6. lépés: Hozd létre a .env fájlt

```bash
cp .env.example .env
nano .env
```

Add meg az API kulcsokat (vagy később az admin felületen):
```
OPENAI_API_KEY=sk-...
GOOGLE_MAPS_API_KEY=AIza...
GOOGLE_PLACES_API_KEY=AIza...
```

### 7. lépés: Inicializáld az adatbázist

```bash
python init_db.py
```

### 8. lépés: Indítsd el az alkalmazást

```bash
mkdir -p tmp
touch tmp/restart.txt
```

### 9. lépés: Ellenőrizd

Várd meg 10-15 másodpercet, majd nyisd meg:
- **https://magyar-ai.com** - Főoldal (átirányít /admin-ra)
- **https://magyar-ai.com/admin** - Admin felület
- **https://magyar-ai.com/health** - Health check
- **https://magyar-ai.com/docs** - API dokumentáció

---

## Munkamenet: Kód Módosítás → Live Frissítés

### Lokális gépen (ahol fejlesztesz):

1. **Végezd el a módosításokat** a kódban
2. **Commit és push** GitHubra:
   ```bash
   git add .
   git commit -m "Leírás a változtatásról"
   git push origin copilot/add-ai-web-generator
   ```

### Hostinger szerveren (SSH):

3. **Egyetlen parancs** a frissítéshez:
   ```bash
   cd ~/public_html/magyar-ai.com
   bash deploy_update.sh
   ```

4. **Várd meg** 10-15 másodpercet
5. **Frissítsd** a böngészőt: **https://magyar-ai.com/admin**

**Kész!** A változtatásaid már élőben vannak! 🎉

---

## Gyakori Problémák

### 503 Error a frissítés után

**Megoldás:** Várj 15-30 másodpercet. A Passenger újraindítja az alkalmazást.

Ha nem szűnik meg:
```bash
cd ~/public_html/magyar-ai.com
python diagnose.py
```

### "Git pull" hibát ad

**Megoldás:** 
```bash
# Mentsd el a lokális változtatásokat
git stash

# Húzd le a legújabb verziót
git pull origin copilot/add-ai-web-generator

# Állítsd vissza a változtatásokat (ha szükséges)
git stash pop
```

### Módosítások nem jelennek meg

**Megoldás:**
```bash
# Hard restart
mkdir -p tmp
touch tmp/restart.txt

# Ellenőrizd a Passenger folyamatot
ps aux | grep passenger

# Ha nem fut, várj 10 másodpercet és próbáld újra
```

### API kulcsok nem működnek

**Megoldás 1:** Add meg az admin felületen
1. Nyisd meg: https://magyar-ai.com/admin
2. Kattints: "API Settings"
3. Add meg a kulcsokat
4. Mentés

**Megoldás 2:** Frissítsd a .env fájlt
```bash
cd ~/public_html/magyar-ai.com
nano .env
# Add meg a kulcsokat
# Mentés: Ctrl+X, Y, Enter
```

---

## Hasznos Parancsok

### Logok megtekintése
```bash
tail -f ~/logs/passenger.log
tail -f ~/logs/error.log
```

### Alkalmazás státusz
```bash
curl https://magyar-ai.com/health
```

### Adatbázis biztonsági mentése
```bash
cp app.db app.db.backup.$(date +%Y%m%d_%H%M%S)
```

### Virtual environment újraaktiválása
```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
```

### Passenger restart (ha a deploy_update.sh nem működik)
```bash
cd ~/public_html/magyar-ai.com
mkdir -p tmp
touch tmp/restart.txt
```

---

## Támogatás

**Diagnosztikai eszközök:**
```bash
python diagnose.py          # Teljes rendszer ellenőrzés
bash configure_hostinger.sh # Konfiguráció javítása
```

**Dokumentáció:**
- `FIX_503_ERROR.md` - 503 hiba megoldása
- `HOSTINGER_DEPLOYMENT.md` - Részletes deployment útmutató
- `ADMIN_PANEL_GUIDE.md` - Admin felület használata

**GitHub Issues:**
Ha problémád van, nyiss egy issue-t: https://github.com/N-Target/googlemaptowebsite/issues

---

## Összefoglalás

**Frissítés munkafolyamat:**
```
Lokális gép → Kód módosítás → git push
    ↓
Hostinger szerver → bash deploy_update.sh
    ↓
Élő weboldal → https://magyar-ai.com/admin
```

**Egy paranccsal:** `bash deploy_update.sh` ✨

Élvezd a gyors fejlesztést! 🚀
