import pandas as pd
from transform.merge_sources import merge_sources

def total_deposits_by_type(accounts_sql, accounts_excel=pd.DataFrame()):
    df = merge_sources(accounts_sql, accounts_excel, "account_id")
    return df.groupby('account_type')['balance'].sum().reset_index()

def low_balance_accounts(accounts_sql, accounts_excel=pd.DataFrame(), threshold=5000):
    df = merge_sources(accounts_sql, accounts_excel, "account_id")
    return df[df['balance'] < threshold]

def dormant_accounts(accounts_sql, transactions_sql, accounts_excel=pd.DataFrame(), transactions_excel=pd.DataFrame(), inactive_days=180):
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    transactions_df = merge_sources(transactions_sql, transactions_excel, "transaction_id")

    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
    recent_cutoff = transactions_df['transaction_date'].max() - pd.Timedelta(days=inactive_days)
    active_ids = transactions_df[transactions_df['transaction_date'] > recent_cutoff]['account_id'].unique()
    return accounts_df[~accounts_df['account_id'].isin(active_ids)]
