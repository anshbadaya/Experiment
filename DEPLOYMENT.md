# Production Deployment Guide

This guide explains how to deploy the Google Sheets API Service to production using Docker.

## Prerequisites

- Docker installed on your server
- Docker Compose installed
- At least 1GB of available RAM
- Port 5000 available

## Quick Deployment

### Option 1: Using the deployment script (Recommended)

```bash
# Make the script executable (if not already done)
chmod +x deploy.sh

# Run the deployment
./deploy.sh
```

### Option 2: Manual deployment

```bash
# Build and start the service
docker-compose up -d

# Check if it's running
docker-compose ps

# View logs
docker-compose logs -f
```

## Production Configuration

### Environment Variables

You can customize the deployment by setting environment variables in `docker-compose.yml`:

```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - WORKERS=4 # Number of Gunicorn workers
  - TIMEOUT=120 # Request timeout in seconds
```

### Scaling

To scale the service for higher load:

```bash
# Scale to 3 instances
docker-compose up -d --scale api=3

# Or modify docker-compose.yml to add more workers
```

### Health Checks

The service includes built-in health checks:

```bash
# Check service health
curl http://localhost:5000/matches

# View health status
docker-compose ps
```

## Monitoring and Logs

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs api
```

### Monitor Resource Usage

```bash
# Check container resource usage
docker stats

# Check disk usage
docker system df
```

## Security Considerations

### Production Security Checklist

- [ ] Change default port (if needed)
- [ ] Set up reverse proxy (nginx/apache)
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules
- [ ] Use secrets management for sensitive data
- [ ] Regular security updates

### Reverse Proxy Example (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Backup and Recovery

### Backup Strategy

```bash
# Backup the entire application
tar -czf backup-$(date +%Y%m%d).tar.gz .

# Backup only the code
tar -czf code-backup-$(date +%Y%m%d).tar.gz service.py requirements.txt
```

### Recovery

```bash
# Restore from backup
tar -xzf backup-YYYYMMDD.tar.gz

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Common Issues

1. **Port already in use**

   ```bash
   # Check what's using the port
   lsof -i :5000

   # Stop conflicting service or change port
   ```

2. **Service not starting**

   ```bash
   # Check logs
   docker-compose logs api

   # Check container status
   docker-compose ps
   ```

3. **Memory issues**

   ```bash
   # Check memory usage
   docker stats

   # Reduce workers in docker-compose.yml
   ```

### Performance Tuning

- **Increase workers**: Modify `--workers` in Dockerfile
- **Adjust timeout**: Modify `--timeout` in Dockerfile
- **Add caching**: Consider Redis for caching
- **Load balancing**: Use multiple instances with nginx

## Maintenance

### Regular Maintenance Tasks

```bash
# Update dependencies
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Clean up unused images
docker image prune -f

# Clean up unused volumes
docker volume prune -f

# Full system cleanup
docker system prune -a
```

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
./deploy.sh
```

## Support

For issues or questions:

1. Check the logs: `docker-compose logs api`
2. Verify the service is running: `docker-compose ps`
3. Test the endpoint: `curl http://localhost:5000/matches`
