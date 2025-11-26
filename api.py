"""
FastAPI backend for Expense Tracking System
Run separately from Streamlit app, or deploy on a cloud service like Railway, Render, or Heroku
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))

from fastapi import FastAPI, HTTPException
from datetime import date
from frontend.db_helper import fetch_expenses_for_date, insert_expense, delete_expenses_for_date, fetch_expense_summary
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Expense Tracking API", version="1.0.0")


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/")
def read_root():
    return {"message": "Expense Tracking API", "version": "1.0.0"}


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    delete_expenses_for_date(expense_date)
    for expense in expenses:
        insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
