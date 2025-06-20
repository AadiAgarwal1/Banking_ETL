import pandas as pd
from transform.merge_sources import merge_sources

def high_value_customers(accounts_sql, login_sql, customerservices_sql, accounts_excel=pd.DataFrame(), login_excel=pd.DataFrame(), customerservices_excel=pd.DataFrame(),min_balance=50000, recent_days=30, min_services=2):
    
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    login_df = merge_sources(login_sql, login_excel, "login_id")
    services_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")

    avg_bal = accounts_df.groupby('customer_id')['balance'].mean().reset_index()
    
    login_df['last_login'] = pd.to_datetime(login_df['last_login'])
    recent_cutoff = login_df['last_login'].max() - pd.Timedelta(days=recent_days)
    recent_login = login_df[login_df['last_login'] > recent_cutoff]

    service_count = services_df.groupby('customer_id').size().reset_index(name='service_count')

    merged = avg_bal.merge(recent_login, on='customer_id', how='inner')
    merged = merged.merge(service_count, on='customer_id', how='inner')

    return merged[(merged['balance'] > min_balance) & (merged['service_count'] >= min_services)]
