import streamlit as st
import mysql.connector

st.title("🔌 Connect to MySQL")

# Step 1: Enter credentials and fetch databases
with st.form("db_credential_form", clear_on_submit=False):
    host = st.text_input("Host", value="localhost")
    port = st.number_input("Port", value=3306)
    user = st.text_input("Username", value="root")
    password = st.text_input("Password", type="password")
    fetch_btn = st.form_submit_button("Fetch Databases")

if fetch_btn:
    try:
        temp_conn = mysql.connector.connect(
            host=host, port=port, user=user, password=password
        )
        cursor = temp_conn.cursor()
        cursor.execute("SHOW DATABASES;")
        db_list = [db[0] for db in cursor.fetchall()]
        temp_conn.close()

        # ✅ Store creds and database list in session_state
        st.session_state["db_creds"] = {
            "host": host, "port": port, "user": user, "password": password
        }
        st.session_state["available_dbs"] = db_list

        st.success("✅ Databases fetched! Now select one below.")
    except Exception as e:
        st.error(f"❌ Connection failed while fetching databases: {e}")

# Step 2: Select a database and connect
if "db_creds" in st.session_state and "available_dbs" in st.session_state:
    with st.form("db_select_form"):
        db = st.selectbox("Select a database", st.session_state["available_dbs"])
        connect_btn = st.form_submit_button("Connect to Database")

    if connect_btn:
        creds = st.session_state["db_creds"]
        try:
            conn = mysql.connector.connect(
                host=creds["host"],
                port=creds["port"],
                user=creds["user"],
                password=creds["password"],
                database=db
            )

            # ✅ Save full credentials to session state for use in Extract page
            st.session_state["db_credentials"] = {
                "host": creds["host"],
                "port": creds["port"],
                "user": creds["user"],
                "password": creds["password"],
                "database": db
            }

            st.success(f"✅ Connected to `{db}` successfully!")
        except Exception as e:
            st.error(f"❌ Failed to connect to selected DB: {e}")
