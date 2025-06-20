import pandas as pd
from sqlalchemy import create_engine

# Update these credentials as per your setup
DB_URI = "mysql+pymysql://root:passworrd-SQLpassword@localhost:3306/playbox"
engine = create_engine(DB_URI)

def load_table_as_df(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

def write_to_sql(df, table_name, mode='replace'):
    df.to_sql(name=table_name, con=engine, if_exists=mode, index=False)
