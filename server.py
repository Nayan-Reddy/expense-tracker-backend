from fastapi import FastAPI, HTTPException, Request
from datetime import date
from typing import List
from pydantic import BaseModel
import db_helper

app = FastAPI()


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date
    session_id: str


@app.get("/")
def root():
    return {"message": "Expense Tracker backend is running"}


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date, request: Request):
    session_id = request.query_params.get("session_id", "demo")
    expenses = db_helper.fetch_expenses_for_date(expense_date, session_id)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense], request: Request):
    session_id = request.query_params.get("session_id", "demo")
    db_helper.delete_expenses_for_date(expense_date, session_id)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes, session_id)
    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date, date_range.session_id)
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


@app.post("/analytics/monthly")
def get_monthly_analytics(date_range: DateRange):
    try:
        return db_helper.fetch_monthly_summary(date_range.start_date, date_range.end_date, date_range.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving monthly analytics: {str(e)}")


@app.delete("/delete-demo-data")
def delete_demo_data():
    try:
        db_helper.delete_all_demo_data()
        return {"message": "Demo data deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting demo data: {str(e)}")


@app.post("/reset-demo-data")
def reset_demo_data():
    try:
        db_helper.reset_demo_data()
        return {"message": "Demo data reset successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting demo data: {str(e)}")
