import pandas as pd
from transform.merge_sources import merge_sources

def new_customer_growth(customers_sql, customers_excel=pd.DataFrame()):
    df = merge_sources(customers_sql, customers_excel, "customer_id")
    df['created_at'] = pd.to_datetime(df['created_at'])
    grouped = df.groupby(df['created_at'].dt.to_period('M')).size().reset_index(name='New_Customers')
    grouped['created_at'] = grouped['created_at'].astype(str)
    return grouped

def multi_product_customers(accounts_sql, loans_sql, cards_sql, customerservices_sql,accounts_excel=pd.DataFrame(), loans_excel=pd.DataFrame(),cards_excel=pd.DataFrame(), customerservices_excel=pd.DataFrame(),min_products=2):
    accounts_df = merge_sources(accounts_sql, accounts_excel, "account_id")
    loans_df = merge_sources(loans_sql, loans_excel, "loan_id")
    cards_df = merge_sources(cards_sql, cards_excel, "card_id")
    services_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")

    combined = pd.concat([
        accounts_df[['customer_id']],
        loans_df[['customer_id']],
        cards_df[['customer_id']],
        services_df[['customer_id']]
    ])
    product_count = combined.groupby('customer_id').size().reset_index(name='products_used')
    return product_count[product_count['products_used'] >= min_products]
