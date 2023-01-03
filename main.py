import tkinter as tk
import tkcalendar
import pandas as pd
import pyodbc
from datetime import datetime as dt
import warnings

warnings.filterwarnings("ignore")

root = tk.Tk()
root.geometry('1600x800')


def button_command():
    startdate = str(cal1.get_date())
    enddate = str(cal2.get_date())
    print(startdate)
    startdate = dt.strptime(startdate, '%Y-%m-%d')
    enddate = dt.strptime(enddate, '%Y-%m-%d')
    print(startdate)
    min_dep = min_deposit.get()
    max_dep = max_deposit.get()
    cnxn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DWH;"
        "Database=dwOper;"
        "Trusted_Connection=yes;"
    )
    if max_dep:
        max_dep_part = f'AND p.Amount <= {max_dep}'
    else:
        max_dep_part = ''
    query = f"""
    SELECT u.Base_UserID,
        p.Amount as DepositAmount,
        p.create_date as Date
    FROM Payment p
        INNER JOIN VIEW_PlatformPartnerUsers_TotogamingAm u 
            ON u.UserID = p.UserID
        INNER JOIN C_PaymentSystem sp
            ON sp.PaymentSystemId = p.PaymentSystemID
    WHERE p.modify_date >= CAST('{startdate}' AS DATE)
        AND p.modify_date <= CAST('{enddate}' AS DATE)
        AND u.PartnerID = 237
        AND p.SourceID = 2
        AND p.PaymentTypeID = 2
        AND p.PaymentStatusID = 8
        AND sp.PaymentSystemName NOT LIKE '%transfer%'
        AND p.EmployeeUserID IS NULL
        AND p.Amount >= {min_dep}
        {max_dep_part}
    ORDER BY u.Base_UserID,
        p.create_date
    """
    df = pd.read_sql(query, cnxn, index_col='Base_UserID', parse_dates='Date')
    cnxn.close()
    print(df.head())
    df.to_csv(f'test.csv', date_format='%Y/%m/%d')


tk.Label(root, text='StartDate', width=10).grid(row=0, column=0)
cal1 = tkcalendar.DateEntry(root, selectmode='day', year=2023, month=1)
cal1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text='EndDate', width=10).grid(row=1, column=0, padx=5, pady=5)
cal2 = tkcalendar.DateEntry(root, selectmode='day', year=2023, month=1)
cal2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text='Min Deposit', width=10).grid(row=0, column=2, padx=5, pady=5)
min_deposit = tk.Entry(root, width=10)
min_deposit.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text='Max Deposit', width=10).grid(row=1, column=2, padx=5, pady=5)
max_deposit = tk.Entry(root, width=10)
max_deposit.grid(row=1, column=3, padx=5, pady=5)

OPTIONS = [
    "Dep",
    "Bet",
    "GGR"
]

variable = tk.StringVar(root)
variable.set(OPTIONS[0])

tk.Label(root, text='Type', width=10).grid(row=0, column=4, padx=5, pady=5)

w = tk.OptionMenu(root, variable, *OPTIONS)
w.grid(row=0, column=5, padx=5, pady=5)

tk.Button(root, text='Button', command=button_command).grid(row=2, column=0)

root.mainloop()
