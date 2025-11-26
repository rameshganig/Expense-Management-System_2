# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account with repository containing this code
- Streamlit Cloud account (https://streamlit.io/cloud)
- Database (MySQL) - either local or cloud-hosted (e.g., AWS RDS, PlanetScale)

## Deployment Steps

### 1. Push Code to GitHub
```bash
cd /path/to/project
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Set Up Streamlit Cloud
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Select the branch (usually `main`)
5. Set the main file path to: `streamlit_app.py`
6. Click "Deploy"

### 3. Configure Secrets in Streamlit Cloud
After deployment, you need to add database credentials:

1. Go to your app in Streamlit Cloud
2. Click the three dots (⋯) menu → "Settings"
3. Go to "Secrets" section
4. Add the following secrets:

```toml
DB_HOST = "your-database-host"
DB_USER = "your-database-user"
DB_PASSWORD = "your-database-password"
DB_NAME = "expense_manager"
```

If using a separate API service (optional):
```toml
USE_API = "false"  # Set to "true" if using external API
API_URL = "https://your-api-url.com"
```

### 4. Database Configuration

#### Option A: Use Existing Local Database (VPN/SSH Tunnel Required)
- Set up SSH tunneling to your local MySQL server
- Update DB_HOST in secrets accordingly

#### Option B: Cloud-Hosted Database (Recommended)
Popular options:
- **PlanetScale** (MySQL-compatible, free tier available)
  - Create a database
  - Get connection details
  - Use those in secrets

- **AWS RDS MySQL**
  - Create RDS instance
  - Note endpoint, username, password
  - Allow Streamlit Cloud IP in security groups

- **DigitalOcean Managed Database**
  - Create MySQL cluster
  - Get connection string

#### Option C: Local Database with Ngrok (Development Only)
```bash
ngrok tcp 3306
```
Then use the ngrok URL as DB_HOST in secrets.

### 5. Verify Deployment
1. Open your Streamlit app URL
2. Test the "Add/Update" tab
3. Test the "Analytics" tab
4. Check for any errors in the "Logs" section in Streamlit Cloud

## File Structure

```
project-root/
├── streamlit_app.py          # Main Streamlit app (entry point for Cloud)
├── api.py                     # Optional FastAPI backend
├── requirements.txt           # Python dependencies
├── frontend/
│   ├── add_update_ui.py
│   ├── analytics_ui.py
│   ├── db_helper.py
│   ├── logging_setup.py
│   ├── server.py
│   └── .streamlit/
│       ├── config.toml
│       └── secrets.toml (DO NOT COMMIT - use Cloud secrets)
├── database/
│   └── expense_db_creation.sql
└── README.md
```

## Important Notes

### For Streamlit Cloud:
- **DO NOT commit `secrets.toml`** - Add to `.gitignore` and use Cloud UI instead
- The app uses **direct database queries** by default (not API calls)
- This means all database access happens directly from the Streamlit app

### For Local Development:
```bash
# Terminal 1: Start FastAPI backend
cd frontend
python -m uvicorn server:app --reload

# Terminal 2: Start Streamlit app
streamlit run app.py
```

### For Production with Separate API:
- Deploy API separately (Railway, Render, Heroku, etc.)
- Set `USE_API="true"` and `API_URL` in secrets
- Update `frontend/server.py` imports if needed

## Troubleshooting

### Database Connection Fails
- Check `DB_HOST` is accessible from Streamlit Cloud IP
- Verify credentials in secrets are correct
- Check database firewall rules allow connections

### ModuleNotFoundError
- Ensure all imports use relative paths
- Check all dependencies are in `requirements.txt`

### Secrets Not Loaded
- Go to app Settings → Secrets
- Add secrets again
- Redeploy or restart the app

## Monitoring

In Streamlit Cloud:
- Check "Logs" tab for runtime errors
- Monitor "App usage" statistics
- Set up email alerts for failures

## Next Steps

1. Monitor app performance
2. Set up automated backups for database
3. Consider scaling database as needed
4. Add more expense categories or features as needed
