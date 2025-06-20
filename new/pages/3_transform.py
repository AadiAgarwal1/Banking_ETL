import streamlit as st
import pandas as pd

# Load transformation functions
from transform.accounts import total_deposits_by_type, low_balance_accounts, dormant_accounts
from transform.customers import new_customer_growth, multi_product_customers
from transform.transactions import transaction_volume_monthly, avg_transaction_by_type, high_value_transactions
from transform.loans import loan_approval_rate, average_loan_duration, loans_by_type
from transform.logins import inactive_logins, login_distribution
from transform.services import service_subscriptions, unused_services, multi_service_customers
from transform.strategy import high_value_customers
from transform.cards import card_preference, card_issuance_rate
from transform.branches import customers_per_branch, employees_per_branch
from transform.risky import risky_customers
from transform.profitability import branch_profitability
from transform.cross_sell import customers_without_cards_loans
from transform.employees_scd import transform_employees
from transform.sql_helpers import load_table_as_df, write_to_sql

st.set_page_config(page_title="Transform", layout="wide")
st.title("🧠 Transformation & Insights Dashboard")

# Load SQL and Excel DataFrames from session state
get_df = lambda name: st.session_state.get(name, pd.DataFrame())

# SQL
customers = get_df("customers_df")
accounts = get_df("accounts_df")
transactions = get_df("transactions_df")
loans = get_df("loans_df")
cards = get_df("cards_df")
logins = get_df("logincredentials_df")
services = get_df("services_df")
customerservices = get_df("customerservices_df")
employees = get_df("employees_df")
branches = get_df("branches_df")

# Excel
customers_excel = get_df("customers_excel_df")
accounts_excel = get_df("accounts_excel_df")
transactions_excel = get_df("transactions_excel_df")
loans_excel = get_df("loans_excel_df")
cards_excel = get_df("cards_excel_df")
logins_excel = get_df("logincredentials_excel_df")
services_excel = get_df("services_excel_df")
customerservices_excel = get_df("customerservices_excel_df")
employees_excel = get_df("employees_excel_df")
branches_excel = get_df("branches_excel_df")

# Helper to layout buttons
def show_button(label, state_key, fn, *args, chart=False, metric=False, index=None):
    if st.button(label):
        result = fn(*args)
        st.session_state[state_key] = result

        if metric:
            st.metric(label, result)
        elif chart:
            if index in result.columns:
                st.bar_chart(result.set_index(index))
            else:
                st.warning(f"\U0001f4db Index '{index}' not found in: {result.columns.tolist()}")
                st.dataframe(result)
        else:
            st.dataframe(result)

# -----------------------------------------
st.subheader("🧍 Customer Insights")
show_button("\U0001f4c5 New Customer Growth", "transformed_customer_growth", new_customer_growth,customers, customers_excel, chart=True, index="created_at")
show_button("\U0001f4e6 Multi-Product Customers", "transformed_multi_product", multi_product_customers,accounts, loans, cards, customerservices,accounts_excel, loans_excel, cards_excel, customerservices_excel)

# -----------------------------------------
st.subheader("💰 Account Insights")
show_button("🏦 Total Deposits by Type", "transformed_total_deposits", total_deposits_by_type,accounts, accounts_excel, chart=True, index="account_type")
show_button("📉 Low Balance Accounts", "transformed_low_balance", low_balance_accounts,accounts, accounts_excel)
show_button("🕵️ Dormant Accounts (180 days)", "transformed_dormant_accounts", dormant_accounts,accounts, transactions, accounts_excel, transactions_excel)

# -----------------------------------------
st.subheader("📈 Transaction Insights")
show_button("📊 Transaction Volume Monthly", "transformed_txn_volume", transaction_volume_monthly,transactions, transactions_excel, chart=True, index="transaction_date")
show_button("💸 Avg Transaction by Account Type", "transformed_avg_txn", avg_transaction_by_type,transactions, accounts, transactions_excel, accounts_excel, chart=True, index="account_type")
show_button("💰 High Value Transactions", "transformed_high_value_txn", high_value_transactions,transactions, transactions_excel, 100000)

# -----------------------------------------
st.subheader("💳 Loans & Cards")
show_button("✅ Loan Approval Rate", "transformed_loan_approval", loan_approval_rate,loans, loans_excel, chart=True, index="Status")
show_button("🗖 Avg Loan Duration", "transformed_loan_duration", average_loan_duration, loans, loans_excel, metric=True)
show_button("📾 Loan Amount by Type", "transformed_loan_type_sum", loans_by_type, loans, loans_excel, chart=True, index="loan_type")
show_button("📊 Card Preference", "transformed_card_preference", card_preference, cards, cards_excel, chart=True, index="Card Type")
show_button("💳 Card Issuance Rate (%)", "transformed_card_rate", card_issuance_rate,cards, customers, cards_excel, customers_excel, metric=True)

# -----------------------------------------
st.subheader("🔐 Login Insights")
show_button("🛑 Inactive Logins > 60 Days", "transformed_inactive_logins", inactive_logins, logins, logins_excel)
show_button("📈 Login Distribution (Monthly)", "transformed_login_distribution", login_distribution, logins, logins_excel, chart=True, index="Month")

# -----------------------------------------
st.subheader("🛠️ Service Analytics")
show_button("📦 Service Subscriptions", "transformed_service_subs", service_subscriptions, customerservices, services, customerservices_excel, services_excel, chart=True, index="service_name")
show_button("❌ Unused Services", "transformed_unused_services", unused_services, services, customerservices, services_excel, customerservices_excel)
show_button("👥 Multi-Service Customers", "transformed_multi_service_customers", multi_service_customers,customerservices, customerservices_excel)

# -----------------------------------------
st.subheader("🏢 Branch & Employee Insights")
show_button("🏦 Customers Per Branch", "transformed_customers_per_branch", customers_per_branch,accounts, branches, accounts_excel, branches_excel)
show_button("👨‍💼 Employees Per Branch", "transformed_employees_per_branch", employees_per_branch,employees, branches, employees_excel, branches_excel)

# SCD Integration Section
with st.expander("🔁 Apply SCD to Employees Table"):
    if st.button("Run Employee SCD Transformation"):
        try:
            current_df = employees
            incoming_df = employees_excel  # From Excel
            history_df = load_table_as_df('employees_history')

            current_df_updated, history_df_updated = transform_employees(current_df, incoming_df, history_df)

            st.success("SCD Applied Successfully!")
            st.subheader("✅ Updated Current Employees")
            st.dataframe(current_df_updated)

            st.subheader("📜 Employees History Table (SCD Type 2)")
            st.dataframe(history_df_updated)

            if st.button("💾 Save SCD Output to Database"):
                write_to_sql(current_df_updated, 'Employees', mode='replace')
                write_to_sql(history_df_updated, 'employees_history', mode='replace')
                st.success("SCD changes saved to database.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# -----------------------------------------
st.subheader("⚠️ Risk & Profitability")
show_button("🛯 Risky Customers (High Loan + Inactive)", "transformed_risky_customers", risky_customers,loans, logins, accounts, loans_excel, logins_excel, accounts_excel)
show_button("📈 Branch Profitability Summary", "transformed_branch_profitability", branch_profitability,accounts, loans, customerservices, branches,accounts_excel, loans_excel, customerservices_excel, branches_excel)
