# Hostinger Deployment Guide

## Magyar-ai.com Hostinger Deployment

This guide explains how to deploy the application on Hostinger shared hosting.

### Prerequisites
- Hostinger account with Python support
- SSH access to your Hostinger server
- Domain (magyar-ai.com) configured

### Deployment Steps

#### 1. Connect to SSH

```bash
ssh username@magyar-ai.com
```

#### 2. Navigate to your domain directory

```bash
cd ~/public_html/magyar-ai.com
# vagy
cd ~/domains/magyar-ai.com/public_html
```

#### 3. Create Virtual Environment

```bash
python3.11 -m venv ~/virtualenv/googlemaptowebsite/3.11
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
```

#### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configure Environment

```bash
# Copy and edit .env file
cp .env.example .env
nano .env
```

Set the following in `.env`:
```env
DATABASE_URL=sqlite:///./googlemaptowebsite.db
APP_ENV=production
OPENAI_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here
```

#### 6. Initialize Database

```bash
python init_db.py
```

#### 7. Configure Passenger

Create or edit `.htaccess` in your domain root:

```apache
PassengerEnabled on
PassengerAppRoot /home/username/public_html/magyar-ai.com
PassengerBaseURI /
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/username/virtualenv/googlemaptowebsite/3.11/bin/python
```

**Important**: Replace `username` with your actual Hostinger username.

#### 8. Restart Application

```bash
# Create restart.txt to trigger restart
mkdir -p tmp
touch tmp/restart.txt
```

### Common Issues and Solutions

#### 503 Service Unavailable

**Possible causes:**

1. **Python version mismatch**
   - Check if Python 3.11 is available: `python3.11 --version`
   - Update `.htaccess` with correct Python version

2. **Virtual environment path incorrect**
   - Verify path in `passenger_wsgi.py` matches your setup
   - Update INTERP variable with correct path

3. **Missing dependencies**
   - Reinstall: `pip install -r requirements.txt`

4. **Database not initialized**
   - Run: `python init_db.py`

5. **Permission issues**
   - Fix permissions: `chmod -R 755 ~/public_html/magyar-ai.com`

6. **Application errors**
   - Check logs: `tail -f ~/logs/error_log` (path may vary)

#### Debug Steps

1. **Check Python version:**
```bash
which python3.11
python3.11 --version
```

2. **Test virtual environment:**
```bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
python -c "import fastapi; print('FastAPI OK')"
```

3. **Test application locally:**
```bash
cd ~/public_html/magyar-ai.com
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
python -c "from main import app; print('App OK')"
```

4. **Check error logs:**
```bash
# Common log locations on Hostinger
tail -f ~/logs/error_log
tail -f ~/domains/magyar-ai.com/logs/error_log
```

5. **Verify file permissions:**
```bash
ls -la ~/public_html/magyar-ai.com/
```

### Alternative: Simplified Deployment (If Passenger Issues)

If Passenger continues to have issues, you can use a startup script:

Create `start.sh`:
```bash
#!/bin/bash
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate
cd ~/public_html/magyar-ai.com
uvicorn main:app --host 0.0.0.0 --port 8000 &
```

Then run: `chmod +x start.sh && ./start.sh`

### Hostinger-Specific Configuration

#### Update passenger_wsgi.py paths

Edit `passenger_wsgi.py` and update:
- Replace `/home/username/` with your actual home path
- Verify virtualenv path matches your setup

Find your home directory:
```bash
echo $HOME
pwd
```

### Production Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with production values
- [ ] Database initialized
- [ ] `passenger_wsgi.py` paths updated
- [ ] `.htaccess` configured correctly
- [ ] File permissions set (755)
- [ ] Application restarted (`touch tmp/restart.txt`)
- [ ] Logs checked for errors

### Support

If issues persist:
1. Contact Hostinger support with error logs
2. Check Hostinger documentation for Python app deployment
3. Verify your hosting plan supports Python applications

### Performance Notes

For production on shared hosting:
- Consider using PostgreSQL instead of SQLite for better concurrency
- Enable caching where possible
- Monitor resource usage
- Set up proper logging

### Next Steps After Deployment

1. Test all endpoints: `https://magyar-ai.com/docs`
2. Generate a test website
3. Configure API keys for production use
4. Set up monitoring and alerts
5. Configure backup strategy
