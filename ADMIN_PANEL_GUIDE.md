# Admin Panel Gyors Útmutató

## Új Funkciók 🎉

Az alkalmazás most már egy gyönyörű admin felülettel rendelkezik, ahol minden beállítást könnyedén kezelhetsz!

### Hozzáférés

1. **Indítsd el az alkalmazást**:
```bash
python main.py
```

2. **Nyisd meg a böngésződben**:
```
http://localhost:8000/admin
```

vagy egyszerűen:
```
http://localhost:8000
```
(automatikusan átirányít az admin panelre)

## Főbb Funkciók

### 1. 📊 Dashboard
- **Élő statisztikák**: Weboldalak, leadek, widgetek, kampányok száma
- **Legutóbbi aktivitás**: Frissen generált weboldalak és leadek
- **Gyors áttekintés**: Minden fontos adat egy helyen

### 2. 🔑 API Beállítások
- **API kulcsok kezelése**: Nincs többé kód szerkesztés!
- **OpenAI API Key**: AI-powered website generation
- **Google Maps API Key**: Térkép és hely adatok
- **Google Places API Key**: Vállalkozás részletek

**Használat**:
1. Kattints az "API Beállítások" menüpontra
2. Írd be az API kulcsokat
3. Kattints a "Mentés" gombra
4. Kész! Az alkalmazás automatikusan használja őket

### 3. 🤖 AI Promptok
- **Prompt szerkesztő**: Szabd testre az AI válaszokat
- **Többnyelvű**: Magyar, angol, német támogatás
- **Aktív/inaktív**: Kapcsold be/ki a promptokat
- **Alapértelmezett**: Jelöld meg a használni kívánt promptot

**Új prompt létrehozása**:
1. Kattints az "Új Prompt" gombra
2. Add meg a nevet és nyelvet
3. Írd meg a prompt szövegét
4. Jelöld be az "Aktív" és "Alapértelmezett" opciókat
5. Mentés

**Prompt változók**:
- `{business_name}` - Vállalkozás neve
- `{address}` - Cím
- `{phone}` - Telefonszám
- `{business_type}` - Vállalkozás típusa

### 4. 🌐 Weboldalak
- **Összes generált weboldal** listája
- **Állapot** és **nyelv** szűrés
- **Közvetlen megtekintés**: Kattints a "Megtekintés" gombra

### 5. 👥 Leadek
- **Lead táblázat**: Összes lead egy helyen
- **Szűrés**: Név, email, státusz szerint
- **Exportálás**: (hamarosan)

### 6. 🧪 Teszt & Preview
**Ez a legfontosabb funkció fejlesztőknek!**

Azonnal kipróbálhatod a weboldal generálást:
1. Adj meg egy vállalkozás nevet
2. Adj meg egy címet
3. Válassz nyelvet
4. Kattints a "Weboldal Generálás" gombra
5. Látod az eredményt + link a kész oldalra

**Nincs kód írás, nincs API hívás kézzel!**

## Adatbázis Beállítások

Az API kulcsok és promptok az adatbázisban tárolódnak:
- **AppSettings** tábla: API kulcsok és konfiguráció
- **AIPromptTemplate** tábla: AI promptok

**Előnyök**:
- ✅ Nincs több `.env` fájl szerkesztés
- ✅ Változtatások azonnal életbe lépnek
- ✅ Könnyű backup és migráció
- ✅ Verziókezelés a promptokhoz

## Biztonsági Megjegyzések (Dev Mode)

Jelenleg **fejlesztői módban** vagyunk:
- ⚠️ Nincs bejelentkezés (authentication)
- ⚠️ Nincs jogosultságkezelés (authorization)
- ⚠️ Admin panel mindenki számára elérhető

**Ez szándékos!** A gyors fejlesztés érdekében.

A második verzióban kerül be:
- 🔐 JWT alapú bejelentkezés
- 👤 Felhasználókezelés
- 🔒 Role-based access control
- 🛡️ Rate limiting
- 📝 Audit log

## UI Dizájn Elemek

### Színsémák
- **Gradiens lila-kék**: Főbb gombok és fejlécek
- **Statisztika kártyák**: Kék, zöld, lila, narancs
- **Állapot jelzők**: Zöld (aktív/új), szürke (inaktív)

### Ikonok
- Font Awesome 6.4.0 használata
- Minden funkcióhoz vizuális jelzés

### Responsiv Dizájn
- Desktop: Teljes sidebar + tartalom
- Tablet: Optimalizált elrendezés
- Mobile: (készül) Hamburger menü

## Gyakori Problémák & Megoldások

### "Nincs adat a dashboard-on"
- Futtasd: `python init_db.py` az adatbázis inicializálásához
- Generálj egy teszt weboldalt a "Teszt & Preview" oldalon

### "API kulcs nem működik"
- Ellenőrizd, hogy helyesen írtad-e be
- Kattints újra a "Mentés" gombra
- Nézd meg az "Összes Beállítás" részt, hogy létrejött-e

### "Prompt nem jelenik meg a generálásban"
- Ellenőrizd, hogy "Aktív" állapotban van-e
- Ellenőrizd, hogy "Alapértelmezett"-nek van-e jelölve
- Megfelelő nyelvet választottad?

## Következő Lépések

1. **Adj meg API kulcsokat** (OpenAI, Google Maps)
2. **Hozz létre egy custom promptot** magyar nyelven
3. **Tesztelj egy weboldal generálást**
4. **Nézd meg a dashboardot** - minden frissül automatikusan!

## Kapcsolat & Támogatás

Ha bármi kérdésed van vagy hibát találsz:
- Nézd meg a böngésző konzolt (F12)
- Ellenőrizd a szerver logokat
- Írd meg a problémát részletesen

## Verzió

**v1.0.0 - Dev Mode**
- Admin UI: ✅ Kész
- API kulcsok: ✅ Kész
- Prompt editor: ✅ Kész
- Teszt interface: ✅ Kész
- Security: ⏳ V2-ben

---

**Élvezd a fejlesztést! 🚀**
