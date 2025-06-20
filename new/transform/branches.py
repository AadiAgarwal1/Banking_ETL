import pandas as pd
from transform.merge_sources import merge_sources

def customers_per_branch(accounts_sql, branches_sql, accounts_excel=pd.DataFrame(), branches_excel=pd.DataFrame()):
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    branches_df = merge_sources(branches_sql, branches_excel, "branch_id")
    branch_summary = accounts_df.groupby('branch_id')['customer_id'].nunique().reset_index(name='customer_count')
    return branch_summary.merge(branches_df, on='branch_id', how='left')

def employees_per_branch(employees_sql, branches_sql, employees_excel=pd.DataFrame(), branches_excel=pd.DataFrame()):
    employees_df = merge_sources(employees_sql, employees_excel, "employee_id")
    branches_df = merge_sources(branches_sql, branches_excel, "branch_id")
    branch_employees = employees_df.groupby('branch_id').size().reset_index(name='employee_count')
    return branch_employees.merge(branches_df, on='branch_id', how='left')
