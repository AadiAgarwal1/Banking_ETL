import streamlit as st
import pandas as pd
import mysql.connector
import os

st.set_page_config(page_title="Extract", layout="wide")
st.title("📤 Extract Data from Database and Local Files")

# ✅ Step 1: Reconnect using stored credentials
conn = None
if "db_credentials" in st.session_state:
    creds = st.session_state["db_credentials"]
    try:
        conn = mysql.connector.connect(**creds)
    except Exception as e:
        st.error(f"❌ Failed to reconnect to database: {e}")
else:
    st.warning("⚠️ Connect to the database first in the 'Connect' tab.")

# ✅ Step 2: Extract all SQL tables dynamically
if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        table_list = [t[0] for t in cursor.fetchall()]
        st.success(f"🔍 Found {len(table_list)} tables in `{creds['database']}`")

        for table in table_list:
            try:
                df = pd.read_sql(f"SELECT * FROM {table}", conn)
                key = f"{table.lower()}_df"
                st.session_state[key] = df

                with st.expander(f"📊 `{table}` ({len(df)} rows)", expanded=False):
                    st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.warning(f"⚠️ Could not load `{table}`: {e}")

        conn.close()

    except Exception as e:
        st.error(f"❌ Failed to fetch tables: {e}")
else:
    st.info("ℹ️ Database connection not established.")

# ✅ Step 3: Extract from local Excel or JSON files
st.markdown("---")
st.markdown("### 📁 Extract from Local File")

if not os.path.exists("source"):
    os.makedirs("source")

files = os.listdir("source")
valid_files = [f for f in files if f.endswith(('.xlsx', '.json'))]

if valid_files:
    file = st.selectbox("Choose file", valid_files)

    try:
        if file.endswith(".xlsx"):
            excel_data = pd.read_excel(f"source/{file}", sheet_name=None)
            st.session_state["local_excel_sheets"] = excel_data  # optional for listing all later

            st.subheader(f"📑 Extracted Worksheets from `{file}`")
            for sheet_name, df_sheet in excel_data.items():
                key = f"{sheet_name.strip().lower().replace(' ', '_')}_excel_df"
                st.session_state[key] = df_sheet

                st.markdown(f"#### 📝 Sheet: `{sheet_name}` ({len(df_sheet)} rows)")
                st.dataframe(df_sheet)

        elif file.endswith(".json"):
            df_local = pd.read_json(f"source/{file}")
            st.session_state["local_file_df"] = df_local

            st.subheader(f"Preview: `{file}`")
            st.dataframe(df_local)

        else:
            st.warning("Unsupported file type.")

    except Exception as e:
        st.error(f"❌ Error loading file `{file}`: {e}")
else:
    st.info("📁 Place your `.xlsx` or `.json` files in the `source/` folder.")
