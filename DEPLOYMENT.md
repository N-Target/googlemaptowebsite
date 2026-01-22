# Deployment Guide

## Docker Deployment

### Prerequisites
- Docker 20+
- Docker Compose 2+

### Build and Run

```bash
# Build containers
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Environment Setup

### 1. MongoDB Setup

```bash
# Install MongoDB
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### 2. Node.js Application

```bash
# Clone repository
git clone https://github.com/N-Target/googlemaptowebsite.git
cd googlemaptowebsite

# Install dependencies
npm ci --production

# Set up environment
cp .env.example .env
nano .env  # Edit with production values

# Install PM2
npm install -g pm2

# Start application
pm2 start src/index.js --name googlemaptowebsite

# Save PM2 configuration
pm2 save
pm2 startup
```

### 3. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 5. Environment Variables

Production `.env`:

```env
NODE_ENV=production
PORT=3000

# MongoDB
MONGODB_URI=mongodb://localhost:27017/googlemaptowebsite

# API Keys (use production keys)
OPENAI_API_KEY=sk-prod-...
GEMINI_API_KEY=...
GOOGLE_MAPS_API_KEY=...

# JWT Secret (generate strong secret)
JWT_SECRET=your_very_long_and_secure_random_string_here

# AI Configuration
DEFAULT_AI_MODEL=gemini-flash
COMPLEX_AI_MODEL=gpt-4o
TOKEN_THRESHOLD=1000

# Localization
DEFAULT_LANGUAGE=hu
SUPPORTED_LANGUAGES=hu,en,de
```

## Monitoring

### Application Logs

```bash
# PM2 logs
pm2 logs googlemaptowebsite

# MongoDB logs
tail -f /var/log/mongodb/mongod.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Check

```bash
curl http://localhost:3000/health
```

## Backup

### MongoDB Backup

```bash
# Create backup
mongodump --uri="mongodb://localhost:27017/googlemaptowebsite" --out=/backup/mongodb/$(date +%Y%m%d)

# Restore backup
mongorestore --uri="mongodb://localhost:27017/googlemaptowebsite" /backup/mongodb/20240101
```

### Automated Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/backup/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mongodump --uri="mongodb://localhost:27017/googlemaptowebsite" --out="$BACKUP_DIR/$DATE"

# Keep only last 7 days of backups
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} \;
```

## Scaling

### Horizontal Scaling with PM2

```bash
# Start multiple instances
pm2 start src/index.js -i max --name googlemaptowebsite

# Or specify number of instances
pm2 start src/index.js -i 4 --name googlemaptowebsite
```

### Load Balancing with Nginx

```nginx
upstream googlemaptowebsite {
    least_conn;
    server localhost:3000;
    server localhost:3001;
    server localhost:3002;
    server localhost:3003;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://googlemaptowebsite;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Security Best Practices

1. **Use strong JWT secret**
2. **Enable MongoDB authentication**
3. **Use HTTPS only in production**
4. **Rate limiting** (implement with express-rate-limit)
5. **Input validation** (implement with express-validator)
6. **Regular security updates**
7. **Monitor API key usage**
8. **Implement CORS properly**

## Performance Optimization

1. **Enable MongoDB indexes**
```javascript
db.websites.createIndex({ userId: 1 })
db.websites.createIndex({ url: 1 })
db.leads.createIndex({ websiteId: 1 })
```

2. **Enable Redis caching** (optional)
3. **Use CDN for static assets**
4. **Optimize images**
5. **Enable gzip compression**

## Troubleshooting

### Application won't start
```bash
# Check logs
pm2 logs googlemaptowebsite

# Check port availability
netstat -tlnp | grep 3000

# Check MongoDB connection
mongo mongodb://localhost:27017/googlemaptowebsite
```

### High memory usage
```bash
# Monitor PM2 processes
pm2 monit

# Restart application
pm2 restart googlemaptowebsite
```

### Database issues
```bash
# Check MongoDB status
sudo systemctl status mongod

# Repair database
mongod --repair
```
