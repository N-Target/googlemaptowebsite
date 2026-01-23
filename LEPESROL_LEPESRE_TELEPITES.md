# Lépésről Lépésre: magyar-ai.com 503 Hiba Megoldása

## ⚠️ FONTOS MEGÉRTENI

**A kód GitHubon van, DE NEM automatikusan települ a Hostinger szerverre!**

Én (Copilot) **NEM tudok** közvetlenül csatlakozni a Hostinger szerverhez.
- ❌ Nincs SSH hozzáférésem
- ❌ Nem tudom futtatni a scriptet helyetted
- ❌ Nem látom mi van a szerveren

**NEKED kell SSH-zni a szerverre és futtatni a telepítő scriptet!**

---

## 📋 PONTOS LÉPÉSEK A 503 HIBA MEGOLDÁSÁHOZ

### 1. ELŐKÉSZÜLET (Helyi gépeden)

Keresd meg a Hostinger bejelentkezési adataidat:
- Hostinger Dashboard: https://hpanel.hostinger.com
- SSH felhasználónév
- SSH jelszó vagy SSH kulcs
- Domain: magyar-ai.com

---

### 2. SSH KAPCSOLAT LÉTREHOZÁSA

#### Windows (PowerShell vagy CMD):
```bash
ssh u123456789@magyar-ai.com
# VAGY
ssh u123456789@srv123.hostinger.com
```

#### Mac/Linux (Terminal):
```bash
ssh u123456789@magyar-ai.com
# VAGY  
ssh u123456789@srv123.hostinger.com
```

**Cseréld le `u123456789`-t a saját Hostinger felhasználóneveddel!**

**Amikor kéri a jelszót:**
- Írd be a Hostinger SSH jelszavad
- ⚠️ **FONTOS**: Amikor írsz, NEM látsz karaktereket - ez normális!
- Csak írd be és nyomj Enter-t

---

### 3. NAVIGÁLÁS A DOMAIN MAPPÁJÁBA

Miután beléptél SSH-n:

```bash
# Próbáld ezeket sorban, amíg az egyik működik:

cd ~/public_html/magyar-ai.com
# VAGY
cd ~/domains/magyar-ai.com/public_html
# VAGY
cd /home/u123456789/domains/magyar-ai.com/public_html
```

**Ellenőrzés hogy jó helyen vagy:**
```bash
ls -la
# Látnod kell: passenger_wsgi.py, .htaccess, app/, stb.
```

---

### 4. ELSŐ ALKALOMMAL: GIT REPOSITORY KLÓNOZÁSA

Ha **még nincs** klónozva a repository:

```bash
# Töröld az esetleges régi fájlokat
cd ~/public_html
rm -rf magyar-ai.com
# VAGY ha létezik és nem git repo:
mv magyar-ai.com magyar-ai.com.backup

# Klónozd le a repository-t GitHubról
git clone -b copilot/add-ai-web-generator https://github.com/N-Target/googlemaptowebsite.git magyar-ai.com

# Lépj be a mappába
cd magyar-ai.com
```

---

### 5. AUTOMATIKUS TELEPÍTÉS (FUTTASD EZT!)

Most futtatd az ALL-IN-ONE telepítő scriptet:

```bash
bash teljes_telepites.sh
```

**Ez a script AUTOMATIKUSAN:**
1. ✅ Ellenőrzi a rendszert
2. ✅ Beállítja a konfigurációt (username, paths)
3. ✅ Frissíti a kódot GitHubról
4. ✅ Telepíti a függőségeket (Python packages)
5. ✅ Inicializálja az adatbázist
6. ✅ Ellenőrzi a .env fájlt
7. ✅ Újraindítja az alkalmazást
8. ✅ Ellenőrzi hogy minden működik

**Várakozási idő: 1-2 perc**

---

### 6. HA A SCRIPT HIBÁT JELENT

#### .env fájl hiányzik:

```bash
# Másold le a példa fájlt
cp .env.example .env

# Szerkeszd a .env fájlt
nano .env
# VAGY
vi .env
```

**Kötelező API kulcsok:**
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_MAPS_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_PLACES_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Mentsd el:
- **nano-ban**: `Ctrl+X`, majd `Y`, majd `Enter`
- **vi-ban**: `ESC`, majd `:wq`, majd `Enter`

Majd futtasd újra:
```bash
bash teljes_telepites.sh
```

---

### 7. ELLENŐRZÉS

#### A. Nézd meg az alkalmazás logokat:
```bash
tail -f ~/logs/magyar-ai.com/error.log
# Vagy
tail -f ~/public_html/magyar-ai.com/passenger.log
```

`Ctrl+C` a kilépéshez

#### B. Teszteld a weboldalt:

**Böngészőben nyisd meg:**
- https://magyar-ai.com/health
- https://magyar-ai.com/admin
- https://magyar-ai.com/docs

**Ha működik:**
- ✅ `/health` → `{"status": "healthy"}` választ kell kapnod
- ✅ `/admin` → Admin panel betöltődik
- ✅ `/docs` → API dokumentáció látható

**Ha 503-at kapsz:**
```bash
# Futtasd a diagnosztikai eszközt
python3.11 diagnose.py
```

---

### 8. GYORS ÚJRAINDÍTÁS (Ha kell)

Ha már telepítve van és csak újra akarod indítani:

```bash
cd ~/public_html/magyar-ai.com
bash teljes_telepites.sh restart
```

Ez csak 10-15 másodperc!

---

## 🔧 GYAKORI PROBLÉMÁK ÉS MEGOLDÁSOK

### "Permission denied" hiba:
```bash
chmod +x teljes_telepites.sh
chmod +x configure_hostinger.sh
bash teljes_telepites.sh
```

### "Python not found" hiba:
```bash
# Ellenőrizd melyik Python van:
which python3.11
which python3
which python

# Használd a teljes útvonalat:
/usr/bin/python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11
```

### "Git not found" hiba:
A Hostingeren alapból telepítve van. Ha mégsem:
```bash
# Lépj kapcsolatba a Hostinger support-tal
# hpanel.hostinger.com → Support
```

### "No space left on device":
```bash
# Ellenőrizd a helyet:
df -h

# Törölj felesleges fájlokat vagy frissítsd a csomagot
```

---

## 📞 HA TOVÁBBRA IS 503-AT KAPSZ

### 1. Futtasd a teljes diagnosztikát:
```bash
cd ~/public_html/magyar-ai.com
python3.11 diagnose.py > diagnostic_report.txt
cat diagnostic_report.txt
```

### 2. Nézd meg a Passenger logot:
```bash
tail -100 ~/public_html/magyar-ai.com/passenger.log
```

### 3. Ellenőrizd az Apache logot:
```bash
tail -100 ~/logs/magyar-ai.com/error.log
```

### 4. Küldd el a log-okat IDE (GitHub PR kommentben):
```
@copilot A diagnostic report és error log tartalma:
[másold ide a log tartalmát]
```

---

## ✅ SIKERES TELEPÍTÉS UTÁN

1. **Nyisd meg**: https://magyar-ai.com/admin
2. **Állítsd be az API kulcsokat** az admin felületen
3. **Teszteld a weboldal generálást** a "Test & Preview" oldalon
4. **Kezdj el használni!**

---

## 🔄 JÖVŐBELI FRISSÍTÉSEK (Ha változtatok a kódon)

### GitHub PR-ben:
```
@copilot add új funkció XYZ
```

### Hostinger szerveren (SSH):
```bash
cd ~/public_html/magyar-ai.com
bash teljes_telepites.sh
# Vár 1-2 percet
# Ellenőrzés: https://magyar-ai.com/admin
```

**Ennyi az egész!** 🚀

---

## 📝 ÖSSZEFOGLALÁS

**MIT CSINÁLTAM (Copilot):**
✅ Kód írás és push GitHubra
✅ Deployment scriptek létrehozása
✅ Dokumentáció magyarul

**MIT KELL NEKED CSINÁLNI:**
1. ❗ SSH-zni a Hostinger szerverre
2. ❗ Klónozni/frissíteni a repository-t
3. ❗ Futtatni: `bash teljes_telepites.sh`
4. ❗ Beállítani az API kulcsokat (admin panel vagy .env)
5. ✅ Használni az oldalt!

**NEM automatikus CI/CD** - te kontrollálod mikor frissül a server!

---

**Ha bármi kérdésed van, írj ide GitHub PR kommentben @copilot-tal!**
