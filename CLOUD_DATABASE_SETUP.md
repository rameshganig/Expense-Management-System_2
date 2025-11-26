# ☁️ Setting Up Cloud Database for Streamlit Cloud

## Problem
Your app is trying to connect to `localhost` (your local machine), but Streamlit Cloud can't access your computer. You need a **cloud-hosted MySQL database**.

## Solution: Use PlanetScale (Recommended ⭐)

**Why PlanetScale?**
- ✅ Free MySQL-compatible database
- ✅ 5GB free storage
- ✅ Easy setup (5 minutes)
- ✅ No credit card needed for free tier
- ✅ Works perfectly with Streamlit Cloud

### Step 1: Create PlanetScale Account
1. Go to https://planetscale.com
2. Click "Sign up"
3. Sign up with GitHub or email

### Step 2: Create a Database
1. Click "Create a new database"
2. Name it: `expense_manager`
3. Select region closest to you
4. Click "Create database"

### Step 3: Get Connection String
1. In your database dashboard, click "Connect"
2. Choose "MySQL" from the dropdown
3. Click "Create password" (if not already created)
4. Copy the connection string (looks like):
   ```
   mysql://user:password@aws.connect.psdb.cloud/expense_manager?sslaccept=strict
   ```

### Step 4: Extract Database Credentials
From the connection string above, extract:
```
DB_HOST = "aws.connect.psdb.cloud"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "expense_manager"
DB_PORT = "3306"
```

### Step 5: Create Your Database Schema
1. In PlanetScale dashboard, go to "Console"
2. Paste the contents of `database/expense_db_creation.sql`
3. Execute the SQL

Or locally:
```bash
mysql -h aws.connect.psdb.cloud -u your_username -p'your_password' < database/expense_db_creation.sql
```

### Step 6: Add Secrets to Streamlit Cloud
1. Go to your Streamlit app
2. Click menu (≡) → "Settings"
3. Click "Secrets"
4. Add this:
   ```toml
   DB_HOST = "aws.connect.psdb.cloud"
   DB_USER = "your_username"
   DB_PASSWORD = "your_password"
   DB_NAME = "expense_manager"
   DB_PORT = "3306"
   ```
5. Click "Save"
6. Your app will automatically restart with new secrets

---

## Alternative Options

### Option A: AWS RDS (Production)
- Cost: $$
- Setup time: 15 minutes
- Best for: Production apps with high traffic

**Steps:**
1. Go to https://aws.amazon.com/rds
2. Create MySQL database
3. Note endpoint, username, password
4. Allow Streamlit Cloud IP in security group
5. Create database schema via MySQL client
6. Add credentials to Streamlit Cloud secrets

### Option B: DigitalOcean Managed Database
- Cost: $$
- Setup time: 10 minutes
- Best for: Medium-scale apps

**Steps:**
1. Go to https://www.digitalocean.com
2. Create Managed MySQL cluster
3. Get connection string
4. Create database schema
5. Add to Streamlit Cloud secrets

### Option C: CockroachDB (Serverless)
- Cost: Free tier available
- Setup time: 5 minutes
- Best for: Quick, reliable deployments

**Steps:**
1. Go to https://cockroachlabs.cloud
2. Create cluster (serverless free tier)
3. Get connection string
4. Set up database
5. Add to secrets

---

## Verify Connection Works

### Local Test
Update `frontend/.streamlit/secrets.toml`:
```toml
DB_HOST = "aws.connect.psdb.cloud"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "expense_manager"
DB_PORT = "3306"
```

Then run locally:
```bash
streamlit run streamlit_app.py
```

If it works locally, it will work on Streamlit Cloud!

### Streamlit Cloud Check
1. Go to your app
2. Click menu (≡) → "Manage app"
3. Click "Logs"
4. Look for "Application startup complete" (success) or connection errors

---

## Troubleshooting

### Error: "Access denied for user"
- ❌ Wrong username or password
- ✅ Double-check credentials in Streamlit Cloud secrets
- ✅ Verify PlanetScale password is active

### Error: "Can't connect to MySQL server"
- ❌ Wrong hostname
- ✅ Use exact hostname from PlanetScale connection string
- ✅ Ensure DB_PORT is "3306" for PlanetScale

### Error: "Unknown database"
- ❌ Database doesn't exist
- ✅ Run `database/expense_db_creation.sql` in PlanetScale Console
- ✅ Verify DB_NAME matches your database name

### Data not showing after restart
- ❌ App restarted and lost sample data
- ✅ Run the SQL file again in PlanetScale Console
- ✅ Or manually insert test data

---

## Next Steps

1. ✅ Set up cloud database (PlanetScale recommended)
2. ✅ Get connection credentials
3. ✅ Add secrets to Streamlit Cloud
4. ✅ Your app will work automatically!

---

## Quick Reference

| Task | Time | Link |
|------|------|------|
| PlanetScale signup | 2 min | https://planetscale.com |
| Create database | 2 min | Dashboard |
| Get credentials | 1 min | Connect button |
| Add to secrets | 1 min | Streamlit Cloud Settings |
| **Total** | **~5 min** | |

**Your app will be live on Streamlit Cloud once you add the database credentials!** 🚀
