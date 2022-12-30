import tkinter as tk
from tkcalendar import Calendar
import pandas as pd
import pyodbc
from datetime import datetime as dt

root = tk.Tk()
root.geometry('1600x800')


def button_command():
    startdate = cal.get_date()
    enddate = cal2.get_date()
    print(startdate)
    startdate = dt.strptime(startdate, '%m/%d/%y')
    enddate = dt.strptime(enddate, '%m/%d/%y')
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



tk.Label(root, text='StartDate', width=20).grid(row=0, column=0)
cal = Calendar(root, selectmode='day', year=2022)
cal.grid(row=0, column=1)
# entry1 = tk.Entry(root, width=30)
# entry1.grid(row=0, column=1)

tk.Label(root, text='EndDate', width=20).grid(row=1, column=0, padx=0, pady=0)
cal2 = Calendar(root, selectmode='day', year=2022)
cal2.grid(row=1, column=1, padx=0, pady=0)

tk.Label(root, text='Minimum Deposit', width=20).grid(row=0, column=2, padx=0, pady=0)
min_deposit = tk.Entry(root, width=20)
min_deposit.grid(row=0, column=3, padx=0, pady=0)

tk.Label(root, text='Maximal Deposit', width=20).grid(row=1, column=2, padx=0, pady=0)
max_deposit = tk.Entry(root, width=20)
max_deposit.grid(row=1, column=3, padx=0, pady=0)

tk.Button(root, text='Button', command=button_command).grid(row=2, column=0)

root.mainloop()
