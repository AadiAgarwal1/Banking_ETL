import pandas as pd
from transform.merge_sources import merge_sources

def inactive_logins(login_sql, login_excel=pd.DataFrame(), inactive_days=60):
    df = merge_sources(login_sql, login_excel, "login_id")
    df['last_login'] = pd.to_datetime(df['last_login'])
    cutoff = df['last_login'].max() - pd.Timedelta(days=inactive_days)
    return df[df['last_login'] < cutoff]

def active_logins(login_sql, login_excel=pd.DataFrame()):
    df = merge_sources(login_sql, login_excel, "login_id")
    df['last_login'] = pd.to_datetime(df['last_login'])
    return df.sort_values('last_login', ascending=False)

def login_distribution(login_sql, login_excel=pd.DataFrame()):
    df = merge_sources(login_sql, login_excel, "login_id")
    df['last_login'] = pd.to_datetime(df['last_login'])
    result = df['last_login'].dt.to_period('M').value_counts().sort_index().reset_index()
    result.columns = ['Month', 'Login Count']
    return result
