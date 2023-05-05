import pandas as pd
import sqlite3
from tsworks import *
from flask import Flask, request
from datetime import datetime


# Create the Flask app
app = Flask(__name__)

# Define the database connection
conn = sqlite3.connect('finance_data.db')

# API to get all companies' stock data for a particular day
@app.route('/stocks/<date>')
def get_stocks_by_date(Date):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d')
    
    # Query the database for the data
    df = pd.read_sql_query(f"SELECT * FROM finance_data WHERE date = '{date}'", conn)
    
    # Convert the DataFrame to a JSON object and return it
    return df.to_json(orient='records')

# API to get all stock data for a particular company for a particular day
# API to get all stock data for a particular company
@app.route('/stocks/<company>')
def get_company_stocks(company):
    # Query the database for the data
    df = pd.read_sql_query(f"SELECT * FROM finance_data WHERE symbol = '{company}'", conn)
    
    # Convert the DataFrame to a JSON object and return it
    return df.to_json(orient='records')
# POST/Patch API to update stock data for a company by date
@app.route('/stocks/<company>/<date>', methods=['POST', 'PATCH'])
def update_stocks_by_date(company, date):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d')
    
    # Get the data from the request
    data = request.get_json()
    
    # Construct the update query
    query = f"UPDATE finance_data SET "
    for key, value in data.items():
        query += f"{key} = '{value}', "
    query = query[:-2] + f" WHERE symbol = '{company}' AND date = '{date}'"
    
    # Execute the query
    conn.execute(query)
    conn.commit()
    
    # Return a success message
    return {'message': 'Data updated successfully'}
if __name__=='__main__':
    app.run(debug=True)