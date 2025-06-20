import pandas as pd
from transform.merge_sources import merge_sources

def customers_without_cards_loans(customers_sql, cards_sql, loans_sql,customers_excel=pd.DataFrame(), cards_excel=pd.DataFrame(), loans_excel=pd.DataFrame()):
    customers_df = merge_sources(customers_sql, customers_excel, "customer_id")
    cards_df = merge_sources(cards_sql, cards_excel, "card_id")
    loans_df = merge_sources(loans_sql, loans_excel, "loan_id")

    card_ids = set(cards_df['customer_id'])
    loan_ids = set(loans_df['customer_id'])
    no_cards_loans = customers_df[~customers_df['customer_id'].isin(card_ids.union(loan_ids))]
    return no_cards_loans
