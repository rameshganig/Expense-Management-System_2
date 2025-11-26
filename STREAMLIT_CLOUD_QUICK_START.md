# Quick Deploy to Streamlit Cloud

## TL;DR - 5 Minute Setup

### 1. GitHub Push
```bash
git add .
git commit -m "Ready for Streamlit Cloud"
git push
```

### 2. Streamlit Cloud
- Go to https://share.streamlit.io
- Click "New app"
- Select repo, branch (main), file (streamlit_app.py)
- Click Deploy

### 3. Add Secrets
In Streamlit Cloud app settings → Secrets:
```toml
DB_HOST = "your-db-host"
DB_USER = "your-db-user"  
DB_PASSWORD = "your-password"
DB_NAME = "expense_manager"
```

### 4. Done! 🎉
Your app is live at `https://your-username-projectname.streamlit.app`

---

## Database Options

| Option | Setup Time | Cost | Best For |
|--------|-----------|------|----------|
| PlanetScale | 5 min | Free/Paid | Quick setup, MySQL compatible |
| AWS RDS | 15 min | $$ | Production, scalable |
| CockroachDB | 5 min | Free tier | Distributed, reliable |
| Neon (PostgreSQL) | 5 min | Free tier | Modern, serverless |

**Recommendation**: Start with PlanetScale free tier, upgrade if needed.

---

## Key Files for Cloud

| File | Purpose |
|------|---------|
| `streamlit_app.py` | **Entry point for cloud** |
| `requirements.txt` | Dependencies |
| `.streamlit/secrets.toml` | ⚠️ Don't commit - use Cloud UI |
| `DEPLOYMENT.md` | Full guide |

---

## Common Issues

### "ModuleNotFoundError"
- Check imports in `streamlit_app.py`
- Verify `requirements.txt` has all packages

### "Database connection failed"
- Verify DB_HOST is cloud accessible
- Check firewall rules allow Streamlit Cloud IPs
- Test credentials locally first

### "Secrets not loading"
- Restart the app (3-dot menu → Rerun)
- Check secrets are in correct format
- Ensure TOML syntax is valid

---

## Monitor & Debug

### Logs
- Click "Manage app" → "Logs" in Streamlit Cloud
- Check for errors/warnings

### Performance
- Monitor "Statistics" tab
- Check app load time
- Optimize slow queries

---

## Next Steps

1. ✅ Deploy to cloud
2. 🔧 Configure database
3. 🧪 Test all features
4. 📊 Monitor performance
5. 🚀 Share with others!
