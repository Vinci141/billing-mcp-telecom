from fastapi import FastAPI
import pandas as pd

app = FastAPI()
df =  pd.read_csv("billing.csv",na_values=[''],parse_dates=['payment_date','bill_date','due_date'])

@app.get("/bills")
def get_bills():
    return df.fillna('None').to_dict('records')

@app.get("/overdue")
def get_overdue():
    return df[df['payment_status']=='Overdue'].to_dict('records')


@app.get("/revenue")
def get_revenue():
    return {
        "total_revenue":df['total_amount'].sum(),
        "average_bill":df['total_amount'].mean()
        }


@app.get("/revenue-per-user")
def get_revenue_per_user():
        return df[["customer_name","total_amount"]].fillna('None').to_dict('records')

    
