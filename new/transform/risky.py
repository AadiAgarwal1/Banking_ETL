import pandas as pd
from transform.merge_sources import merge_sources

def risky_customers(loans_sql, logins_sql, accounts_sql,
                    loans_excel=pd.DataFrame(),
                    logins_excel=pd.DataFrame(),
                    accounts_excel=pd.DataFrame()):

    loans_df = merge_sources(loans_sql, loans_excel, "loan_id")
    login_df = merge_sources(logins_sql, logins_excel, "login_id")
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")

    login_df['last_login'] = pd.to_datetime(login_df['last_login'], errors='coerce')
    inactive = login_df[login_df['last_login'] < pd.Timestamp.now() - pd.Timedelta(days=90)]

    high_value_loans = loans_df[loans_df['amount'] > 100000]

    risky = high_value_loans.merge(inactive, on='customer_id', how='inner')
    return risky.merge(accounts_df, on='customer_id', how='left')
