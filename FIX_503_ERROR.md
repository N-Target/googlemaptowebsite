# 503 Hiba Megoldása - magyar-ai.com

## 🚨 Azonnali Megoldás

A 503 hiba azt jelenti, hogy a Passenger nem tudja elindítani az alkalmazást. Ez általában konfiguráció hiba.

### Gyors Javítás (5 perc)

```bash
# 1. SSH kapcsolódás
ssh your_username@magyar-ai.com

# 2. Navigálj a domain könyvtárba
cd ~/public_html/magyar-ai.com
# VAGY
cd ~/domains/magyar-ai.com/public_html

# 3. Futtasd az automatikus konfigurátort
bash configure_hostinger.sh

# 4. Kövesd a script utasításait
# A script automatikusan beállítja a felhasználónevedet és útvonalakat

# 5. Telepítsd a függőségeket (ha még nem tetted)
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
pip install -r requirements.txt

# 6. Inicializáld az adatbázist
python init_db.py

# 7. Indítsd újra
./restart.sh
```

## 🔍 Probléma Diagnosztika

### 1. Ellenőrizd a Konfigurációt

```bash
# Nézd meg a .htaccess fájlt
cat .htaccess | grep -E "PassengerAppRoot|PassengerPython"

# A kimenetnek ilyennek KELL lennie (a valódi felhasználóneveddel):
# PassengerAppRoot /home/u123456789/public_html/magyar-ai.com
# PassengerPython /home/u123456789/virtualenv/googlemaptowebsite/3.11/bin/python

# Ha még mindig "username" látszik, akkor HIBÁS!
```

### 2. Ellenőrizd a Virtual Environment-et

```bash
# Létezik?
ls -la ~/virtualenv/googlemaptowebsite/3.11/bin/python

# Ha hibát ad, hozd létre:
python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11
```

### 3. Ellenőrizd a Függőségeket

```bash
# Aktiváld a virtual environment-et
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate

# Teszteld az importokat
python -c "from main import app; print('✓ App betöltve sikeresen!')"

# Ha ImportError-t kapsz, telepítsd a függőségeket:
pip install -r requirements.txt
```

### 4. Ellenőrizd az Adatbázist

```bash
# Létezik?
ls -la googlemaptowebsite.db

# Ha nem, inicializáld:
python init_db.py
```

### 5. Ellenőrizd a Jogosultságokat

```bash
# Állítsd be a megfelelő jogosultságokat
chmod -R 755 ~/public_html/magyar-ai.com
chmod 644 .htaccess
chmod 644 passenger_wsgi.py
```

### 6. Nézd meg a Passenger Logokat

```bash
# Hostinger log fájlok (az útvonal változhat)
tail -100 ~/logs/error_log
# VAGY
tail -100 ~/domains/magyar-ai.com/logs/error_log

# Keresd a Passenger vagy Python hibákat
```

## 🛠️ Gyakori Hibák és Megoldások

### Hiba #1: "username" még mindig a fájlokban

**Megoldás:**
```bash
# Futtasd az auto-konfigurátort
bash configure_hostinger.sh
```

### Hiba #2: Python nem található

**Probléma:** Rossz Python útvonal
**Megoldás:**
```bash
# Találd meg a Python útvonalat
which python3.11

# Frissítsd a .htaccess-ben:
# PassengerPython /home/YOUR_USERNAME/virtualenv/googlemaptowebsite/3.11/bin/python
```

### Hiba #3: ModuleNotFoundError: No module named 'fastapi'

**Probléma:** Függőségek nincsenek telepítve
**Megoldás:**
```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
pip install -r requirements.txt
```

### Hiba #4: Database not found

**Probléma:** Adatbázis nincs inicializálva
**Megoldás:**
```bash
python init_db.py
```

### Hiba #5: Permission denied

**Probléma:** Rossz fájl jogosultságok
**Megoldás:**
```bash
chmod -R 755 ~/public_html/magyar-ai.com
```

## 📋 Teljes Ellenőrző Lista

Jelöld be amikor kész:

- [ ] SSH kapcsolat működik
- [ ] Navigáltál a helyes könyvtárba (`pwd` parancs)
- [ ] `configure_hostinger.sh` futtatva
- [ ] `.htaccess` nem tartalmaz "username" szöveget
- [ ] `passenger_wsgi.py` nem tartalmaz "username" szöveget
- [ ] Virtual environment létezik (`ls ~/virtualenv/googlemaptowebsite/3.11/bin/python`)
- [ ] Függőségek telepítve (`pip list | grep fastapi`)
- [ ] `.env` fájl létezik (`ls .env`)
- [ ] Adatbázis inicializálva (`ls googlemaptowebsite.db`)
- [ ] Jogosultságok rendben (`ls -la`)
- [ ] `tmp/restart.txt` frissítve (`./restart.sh`)
- [ ] Logok ellenőrizve hibákért

## 🔧 Kézi Konfiguráció (Ha az auto-script nem működik)

### 1. .htaccess szerkesztése

```bash
nano .htaccess
```

Cseréld le MINDEN `username` előfordulást a valódi Hostinger felhasználóneveddel:

```apache
PassengerAppRoot /home/YOUR_ACTUAL_USERNAME/public_html/magyar-ai.com
PassengerPython /home/YOUR_ACTUAL_USERNAME/virtualenv/googlemaptowebsite/3.11/bin/python
```

### 2. passenger_wsgi.py szerkesztése

```bash
nano passenger_wsgi.py
```

Módosítsd az INTERP sort:

```python
INTERP = '/home/YOUR_ACTUAL_USERNAME/virtualenv/googlemaptowebsite/3.11/bin/python'
```

És add hozzá az app könyvtár útvonalát:

```python
sys.path.insert(0, '/home/YOUR_ACTUAL_USERNAME/public_html/magyar-ai.com')
os.chdir('/home/YOUR_ACTUAL_USERNAME/public_html/magyar-ai.com')
```

## 🆘 Ha Még Mindig Nem Működik

### Próbáld ki ezt a minimális konfigurációt:

**Új .htaccess:**
```apache
PassengerEnabled on
PassengerAppRoot /home/YOUR_USERNAME/public_html/magyar-ai.com
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/YOUR_USERNAME/virtualenv/googlemaptowebsite/3.11/bin/python
```

**Új passenger_wsgi.py:**
```python
import sys
import os

# Cseréld le YOUR_USERNAME-t
sys.path.insert(0, '/home/YOUR_USERNAME/public_html/magyar-ai.com')
os.chdir('/home/YOUR_USERNAME/public_html/magyar-ai.com')

# Aktiváld a virtual environment
activate_this = '/home/YOUR_USERNAME/virtualenv/googlemaptowebsite/3.11/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

from main import app
application = app
```

### Tesztelés

```bash
# Teszteld lokálisan
cd ~/public_html/magyar-ai.com
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
python -c "from main import app; print('OK')"

# Ha ez működik, de a weboldal nem, akkor Passenger konfiguráció hiba van
```

## 📞 Hostinger Support Megkeresése

Ha semmi nem segít, vedd fel a kapcsolatot a Hostinger support-tal:

**Szükséges információk:**
1. Domain név: magyar-ai.com
2. Probléma: 503 Service Unavailable
3. Python verzió: 3.11
4. Framework: FastAPI + Passenger
5. Csatold a log fájlt: `~/logs/error_log` utolsó 100 sora

```bash
# Log készítése supportnak
tail -100 ~/logs/error_log > error_log_for_support.txt
```

## ✅ Sikeres Telepítés Ellenőrzése

Ha minden jól van beállítva:

1. **https://magyar-ai.com** - Betölt az admin panel
2. **https://magyar-ai.com/health** - Visszaad `{"status": "healthy"}`
3. **https://magyar-ai.com/docs** - API dokumentáció látható

## 🎯 Következő Lépések Siker Után

1. Állítsd be az API kulcsokat az admin felületen
2. Hozz létre egy teszt weboldalt
3. Ellenőrizd a funkciók működését

---

**Verzió:** 1.0.0  
**Frissítve:** 2026-01-23  
**Support:** GitHub Issues
