import pandas as pd
from transform.merge_sources import merge_sources

def card_preference(cards_sql, cards_excel=pd.DataFrame()):
    df = merge_sources(cards_sql, cards_excel, "card_id")
    result = df['card_type'].value_counts().reset_index()
    result.columns = ['Card Type', 'Count']
    return result

def card_issuance_rate(cards_sql, customers_sql, cards_excel=pd.DataFrame(), customers_excel=pd.DataFrame()):
    cards_df = merge_sources(cards_sql, cards_excel, "card_id")
    customers_df = merge_sources(customers_sql, customers_excel, "customer_id")
    issued = cards_df['customer_id'].nunique()
    total = customers_df['customer_id'].nunique()
    return round((issued / total) * 100, 2)
