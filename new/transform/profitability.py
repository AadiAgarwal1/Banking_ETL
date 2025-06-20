import pandas as pd
from transform.merge_sources import merge_sources

def branch_profitability(accounts_sql, loans_sql, customerservices_sql, branches_sql,accounts_excel=pd.DataFrame(), loans_excel=pd.DataFrame(),customerservices_excel=pd.DataFrame(), branches_excel=pd.DataFrame()):
    
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    loans_df = merge_sources(loans_sql, loans_excel, "loan_id")
    services_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")
    branches_df = merge_sources(branches_sql, branches_excel, "branch_id")

    acc_sum = accounts_df.groupby('branch_id')['balance'].sum().reset_index(name='total_balance')
    loan_sum = loans_df.groupby('branch_id')['amount'].sum().reset_index(name='total_loans')
    service_counts = services_df.groupby('customer_id').size().reset_index(name='services')

    profitability = acc_sum.merge(loan_sum, on='branch_id', how='outer')
    profitability = profitability.merge(branches_df, on='branch_id', how='left')

    return profitability
