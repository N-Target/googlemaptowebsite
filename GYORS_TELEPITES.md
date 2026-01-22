# Hostinger Gyors Telepítési Útmutató - magyar-ai.com

## 🚀 5 Perces Telepítés

### 1. SSH Kapcsolat
```bash
ssh username@magyar-ai.com
```

### 2. Navigálás
```bash
cd ~/public_html/magyar-ai.com
# VAGY
cd ~/domains/magyar-ai.com/public_html
```

### 3. Virtual Environment
```bash
# Telepítés
python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11

# Aktiválás
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate

# Upgrade pip
pip install --upgrade pip

# Dependencies telepítése
pip install -r requirements.txt
```

### 4. Konfiguráció

#### A) .env fájl
```bash
cp .env.example .env
nano .env
```

Minimális konfiguráció:
```env
DATABASE_URL=sqlite:///./googlemaptowebsite.db
APP_ENV=production
```

#### B) passenger_wsgi.py frissítése
```bash
nano passenger_wsgi.py
```

Cseréld le ezt a sort:
```python
INTERP = os.path.join(os.environ['HOME'], 'virtualenv', 'googlemaptowebsite', '3.11', 'bin', 'python')
```

Ha a `$HOME` nem működik, használd a teljes útvonalat:
```python
INTERP = '/home/u123456789/virtualenv/googlemaptowebsite/3.11/bin/python'
```

Útvonal megtalálása:
```bash
echo $HOME
pwd
```

#### C) .htaccess frissítése
```bash
nano .htaccess
```

Cseréld le MINDENHOL a `username`-t a saját felhasználónevedre (pl. `u123456789`):

```apache
PassengerAppRoot /home/u123456789/public_html/magyar-ai.com
PassengerPython /home/u123456789/virtualenv/googlemaptowebsite/3.11/bin/python
```

### 5. Adatbázis Inicializálás
```bash
python init_db.py
```

### 6. Diagnosztika (opcionális de ajánlott)
```bash
python diagnose.py
```

Ha minden ✅, akkor jó vagy!

### 7. Újraindítás
```bash
mkdir -p tmp
touch tmp/restart.txt
```

### 8. Tesztelés
Látogass el: https://magyar-ai.com

## ⚠️ 503 Hiba? Gyors Ellenőrzés

### 1. Ellenőrizd a felhasználónevet
```bash
whoami
echo $HOME
```

Használd ezt a nevet a `.htaccess` és `passenger_wsgi.py` fájlokban!

### 2. Ellenőrizd a virtual environment útvonalat
```bash
ls -la ~/virtualenv/googlemaptowebsite/3.11/bin/python
```

Ha nem létezik, újra kell telepíteni:
```bash
python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11
```

### 3. Teszteld a Python importokat
```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
python -c "from main import app; print('OK')"
```

Ha hiba van, futtasd:
```bash
pip install -r requirements.txt
```

### 4. Ellenőrizd a jogosultságokat
```bash
chmod -R 755 ~/public_html/magyar-ai.com
```

### 5. Nézd meg a logokat
```bash
# Hostinger log fájlok helye változhat
tail -f ~/logs/error_log
# VAGY
tail -f ~/domains/magyar-ai.com/logs/error_log
```

## 📋 Checklist

- [ ] SSH kapcsolat működik
- [ ] Virtual environment létrehozva
- [ ] Dependencies telepítve (`pip list | grep fastapi`)
- [ ] .env fájl létezik és konfigurálva
- [ ] passenger_wsgi.py frissítve helyes username-mel
- [ ] .htaccess frissítve helyes username-mel
- [ ] Adatbázis inicializálva (`ls -la googlemaptowebsite.db`)
- [ ] diagnose.py futtatva és minden ✅
- [ ] Újraindítás végrehajtva (`tmp/restart.txt` létezik)
- [ ] Website elérhető: https://magyar-ai.com

## 🆘 Még mindig nem megy?

### Hostinger Support megkeresése:
1. Nézd meg a logokat és másold ki a hibát
2. Futtasd: `python diagnose.py > diagnostic.txt`
3. Küld el a Hostinger supportnak a diagnostic.txt-t

### Gyakori hibák:

**ImportError: No module named 'fastapi'**
```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
pip install -r requirements.txt
```

**Permission denied**
```bash
chmod -R 755 ~/public_html/magyar-ai.com
```

**Database is locked**
```bash
# SQLite probléma shared hosting-on
# Használj PostgreSQL-t production-ban
```

**Wrong Python version**
```bash
# Ellenőrizd hogy 3.11 van-e
python3.11 --version
# Ha nincs, kérd a Hostinger support-ot
```

## 🎉 Sikeres Telepítés Után

1. **API dokumentáció**: https://magyar-ai.com/docs
2. **Health check**: https://magyar-ai.com/health
3. **Generálj egy teszt weboldalt**:
```bash
curl -X POST https://magyar-ai.com/api/v1/generator/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Teszt Étterem",
    "address": "Budapest",
    "language": "hu"
  }'
```

## 📞 Segítség

- **Részletes útmutató**: `HOSTINGER_DEPLOYMENT.md`
- **Diagnosztikai eszköz**: `python diagnose.py`
- **GitHub Issues**: https://github.com/N-Target/googlemaptowebsite/issues

---

**Készítette**: AI Website Generator Team  
**Verzió**: 1.0.0  
**Utolsó frissítés**: 2026-01-22
