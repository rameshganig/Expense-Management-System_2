import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import os


# For cloud deployment, use direct database queries instead of API
# In Streamlit Cloud, both app and API can access the same database
USE_API = os.getenv("USE_API", "false").lower() == "true"
API_URL = os.getenv("API_URL", "http://localhost:8000")


def analytics_tab():
    from db_helper import fetch_expense_summary
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        try:
            if USE_API:
                # Use API endpoint if configured
                payload = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                response = requests.post(f"{API_URL}/analytics/", json=payload, timeout=10)
                response.raise_for_status()
                response_data = response.json()
            else:
                # Use direct database query (works in Streamlit Cloud)
                data = fetch_expense_summary(start_date, end_date)
                if data is None:
                    st.error("Failed to retrieve expense summary from the database.")
                    return

                total = sum([row['total'] for row in data])

                response_data = {}
                for row in data:
                    percentage = (row['total'] / total) * 100 if total != 0 else 0
                    response_data[row['category']] = {
                        "total": row['total'],
                        "percentage": percentage
                    }

            data = {
                "Category": list(response_data.keys()),
                "Total": [response_data[category]["total"] for category in response_data],
                "Percentage": [response_data[category]["percentage"] for category in response_data]
            }

            if len(data["Category"]) == 0:
                st.info("No expenses found for the selected date range.")
                return

            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="Percentage", ascending=False)

            st.subheader("📊 Expense Breakdown By Category")

            col1, col2 = st.columns([2, 1])
            with col1:
                st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], use_container_width=True)

            with col2:
                df_display = df_sorted.copy()
                df_display["Total"] = df_display["Total"].map("${:.2f}".format)
                df_display["Percentage"] = df_display["Percentage"].map("{:.1f}%".format)
                st.table(df_display)

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")
        except Exception as e:
            st.error(f"Error retrieving analytics: {str(e)}")


