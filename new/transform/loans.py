import pandas as pd
from transform.merge_sources import merge_sources

def loan_approval_rate(loans_sql, loans_excel=pd.DataFrame()):
    loans_df = merge_sources(loans_sql, loans_excel, "loan_id")
    df = loans_df['status'].value_counts(normalize=True).reset_index()
    df.columns = ['Status', 'Rate']
    return df

def average_loan_duration(loans_sql, loans_excel=pd.DataFrame()):
    df = merge_sources(loans_sql, loans_excel, "loan_id")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['duration_days'] = (df['end_date'] - df['start_date']).dt.days
    
    if df.empty:
        return "0 days"

    total_days = int(df['duration_days'].mean())

    years = total_days // 365
    months = (total_days % 365) // 30
    days = (total_days % 365) % 30

    parts = []
    if years:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if months:
        parts.append(f"{months} month{'s' if months > 1 else ''}")
    if days or not parts:
        parts.append(f"{days} day{'s' if days != 1 else ''}")

    return " ".join(parts)

def loans_by_type(loans_sql, loans_excel=pd.DataFrame()):
    df = merge_sources(loans_sql, loans_excel, "loan_id")
    return df.groupby('loan_type')['amount'].sum().reset_index()
