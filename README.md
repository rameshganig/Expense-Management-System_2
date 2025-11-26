# 💰 Expense Management System

A full-stack expense tracking application built with Streamlit and FastAPI. Track daily expenses by category and analyze spending patterns with interactive analytics.

**[📱 Try the Live Demo](https://streamlit.io/cloud)** | **[📖 Deployment Guide](./DEPLOYMENT.md)**

## Features

- ✅ Add/Update expenses by date
- 📊 Visual analytics with category breakdown
- 💾 Persistent MySQL database storage
- 🎨 Clean, intuitive UI
- ☁️ Ready for Streamlit Cloud deployment

## Project Structure

```
project-root/
├── streamlit_app.py              # Main app entry point (for Streamlit Cloud)
├── api.py                        # Optional FastAPI backend
├── requirements.txt              # Python dependencies
├── DEPLOYMENT.md                 # Cloud deployment guide
├── frontend/
│   ├── app.py                    # Local Streamlit app
│   ├── add_update_ui.py          # Add/Update expenses UI
│   ├── analytics_ui.py           # Analytics dashboard
│   ├── db_helper.py              # Database operations
│   ├── logging_setup.py          # Logging configuration
│   └── .streamlit/config.toml    # Streamlit settings
├── database/
│   └── expense_db_creation.sql   # MySQL schema
└── README.md                     # This file
```

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- MySQL server running locally
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/expense-management-system.git
   cd expense-management-system
   ```

2. **Install dependencies:**:   
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database** (MySQL):
   ```bash
   mysql -u root -p < database/expense_db_creation.sql
   ```

4. **Configure secrets** (create `frontend/.streamlit/secrets.toml`):
   ```toml
   DB_HOST = "localhost"
   DB_USER = "root"
   DB_PASSWORD = "your_password"
   DB_NAME = "expense_manager"
   ```

5. **Run the application**:
   
   Option A - Streamlit only (direct database access):
   ```bash
   streamlit run frontend/app.py
   ```

   Option B - With FastAPI backend:
   ```bash
   # Terminal 1: Start API server
   cd frontend
   python -m uvicorn server:app --reload

   # Terminal 2: Start Streamlit app
   streamlit run frontend/app.py
   ```

## Cloud Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set main file to `streamlit_app.py`
4. Add database secrets in the Cloud UI (Settings → Secrets)

**See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions**

## Usage

### Add/Update Expenses
1. Select a date
2. Enter amount, category, and notes for each expense
3. Click "Submit" to save

### View Analytics
1. Select start and end dates
2. Click "Get Analytics"
3. View expense breakdown by category

## Technologies

- **Frontend**: [Streamlit](https://streamlit.io/) - Fast web app framework
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
- **Database**: MySQL with `mysql-connector-python`
- **Data Processing**: Pandas for analytics
- **Deployment**: Streamlit Cloud, Railway, Render, or self-hosted

## Configuration

### Environment Variables

```bash
DB_HOST          # Database host (default: localhost)
DB_USER          # Database user (default: root)
DB_PASSWORD      # Database password
DB_NAME          # Database name (default: expense_manager)
API_URL          # API endpoint (default: http://localhost:8000)
USE_API          # Use API or direct DB (default: false)
```

## Database Schema

### expenses table
```sql
CREATE TABLE expenses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  expense_date DATE NOT NULL,
  amount FLOAT NOT NULL,
  category VARCHAR(255) NOT NULL,
  notes TEXT,
  KEY idx_date (expense_date)
);
```

## Expense Categories

- Rent
- Food
- Shopping
- Entertainment
- Other

## Performance Considerations

- Queries are optimized with indexes on `expense_date`
- For Streamlit Cloud, direct database access is recommended
- For high traffic, consider deploying API separately and using caching

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make changes and test locally
4. Commit changes (`git commit -am 'Add improvement'`)
5. Push to branch (`git push origin feature/improvement`)
6. Create Pull Request

## License

This project is open source and available under the MIT License.

## Support

- 📖 See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment help
- 🐛 Report issues on GitHub
- 💡 Suggest features via Issues

## Roadmap

- [ ] User authentication & multi-user support
- [ ] Recurring expenses
- [ ] Budget alerts
- [ ] CSV export functionality
- [ ] Mobile app version
- [ ] Dark mode theme
