# AWS RDS MySQL Setup Guide

Your app is now configured to use AWS RDS MySQL with credentials:
- **Endpoint**: `expensemanager.cjmwykkwio4g.us-east-2.rds.amazonaws.com`
- **Username**: `root`
- **Database**: `dexpense_manager`
- **Port**: `3306`

## Issue: Connection Timeout

If you see: `Can't connect to MySQL server on 'expensemanager.cjmwykkwio4g...' (60 Operation timed out)`

### Root Cause
Your RDS security group doesn't allow inbound connections from your local machine (or Streamlit Cloud).

### Solution: Update RDS Security Group

**For Local Development:**

1. Go to **AWS Console** → **RDS** → **Databases** → Select your DB instance
2. Click the security group under "Security groups" (e.g., `rds-launch-wizard-1`)
3. Go to **Inbound Rules** → **Edit inbound rules**
4. Add a new rule:
   - **Type**: MySQL/Aurora
   - **Port Range**: 3306
   - **Source**: Your local machine's IP (find it by running `curl ifconfig.me` in terminal)
   - Or for testing: Source = `0.0.0.0/0` (opens to all; NOT recommended for production)
5. Click **Save rules** and wait 30 seconds for the rule to take effect

**For Streamlit Cloud:**

Same steps, but use source: `0.0.0.0/0` (Streamlit Cloud's IPs are dynamic, so they recommend this)

### Verify Connection After Security Group Update

After updating the security group, test locally:
```bash
cd /Users/rameshjawali/Desktop/AIML/Course/codebasics_python_course_code/Trial/5_project_two_expense_management/Expense-Management-System_2/frontend
python3 db_helper.py
```

You should see:
```
DB Config: {'host': 'expensemanager.cjmwykkwio4g.us-east-2.rds.amazonaws.com', 'user': 'root', 'password': '***', 'database': 'dexpense_manager', 'port': 3306}
Expenses for today: []
Summary: []
```

## Code Changes Made

✅ `frontend/db_helper.py` now uses MySQL instead of SQLite
✅ `frontend/.streamlit/secrets.toml` updated with AWS RDS credentials
✅ All SQL queries updated to use `%s` placeholders (MySQL standard) instead of `?` (SQLite)

## Next Steps

1. **Fix AWS Security Group** (as per above)
2. **Test locally** to verify connection works
3. **Start Streamlit app**:
   ```bash
   cd /Users/rameshjawali/Desktop/AIML/Course/codebasics_python_course_code/Trial/5_project_two_expense_management
   streamlit run Expense-Management-System_2/streamlit_app.py
   ```
4. **Deploy to Streamlit Cloud**:
   - Push code to GitHub
   - On share.streamlit.io, add Secrets (Settings → Secrets):
     ```
     DB_HOST = "expensemanager.cjmwykkwio4g.us-east-2.rds.amazonaws.com"
     DB_USER = "root"
     DB_PASSWORD = "1OX10ec425"
     DB_PORT = "3306"
     DB_NAME = "dexpense_manager"
     ```
   - Deploy and verify

## Important Notes

- ⚠️ Never commit `.streamlit/secrets.toml` to GitHub (it's in `.gitignore`)
- 🔒 For production, use a strong password and restrict security group to known IPs
- 📊 AWS RDS costs money — check your AWS billing to monitor usage
