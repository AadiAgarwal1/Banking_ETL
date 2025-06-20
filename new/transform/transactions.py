import pandas as pd
from transform.merge_sources import merge_sources

def transaction_volume_monthly(transactions_sql, transactions_excel=pd.DataFrame()):
    df = merge_sources(transactions_sql, transactions_excel, "transaction_id")
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    summary = df.groupby(df['transaction_date'].dt.to_period('M')).size().reset_index(name='Transactions')
    summary['transaction_date'] = summary['transaction_date'].astype(str)
    return summary

def avg_transaction_by_type(transactions_sql, accounts_sql, transactions_excel=pd.DataFrame(), accounts_excel=pd.DataFrame()):
    txn_df = merge_sources(transactions_sql, transactions_excel, "transaction_id")
    acc_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    merged = txn_df.merge(acc_df, on='account_id')
    return merged.groupby('account_type')['amount'].mean().reset_index()

def high_value_transactions(transactions_sql, transactions_excel=pd.DataFrame(), threshold=100000):
    df = merge_sources(transactions_sql, transactions_excel, "transaction_id")
    return df[df['amount'] > threshold]
