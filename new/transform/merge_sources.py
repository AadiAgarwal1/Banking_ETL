import pandas as pd

def merge_sources(sql_df: pd.DataFrame, excel_df: pd.DataFrame, id_col: str, track_source: bool = True, prefix_excel_ids: bool = False) -> pd.DataFrame:
    """
    Merges SQL and Excel dataframes safely by renaming overlapping IDs in the Excel data.

    Args:
        sql_df (pd.DataFrame): Data from SQL.
        excel_df (pd.DataFrame): Data from Excel.
        id_col (str): The name of the ID column to ensure uniqueness.
        track_source (bool): Whether to add a 'source' column.
        prefix_excel_ids (bool): If True, prefix Excel IDs instead of shifting numerically.

    Returns:
        pd.DataFrame: Combined dataframe with unique IDs and optional source column.
    """
    if sql_df.empty and excel_df.empty:
        return pd.DataFrame()

    if sql_df.empty:
        df = excel_df.copy()
        if track_source:
            df['source'] = 'excel'
        return df
    
    if excel_df.empty:
        df = sql_df.copy()
        if track_source:
            df['source'] = 'sql'
        return df

    sql_df = sql_df.copy()
    excel_df = excel_df.copy()

    if id_col not in sql_df.columns or id_col not in excel_df.columns:
        raise ValueError(f"'{id_col}' must exist in both SQL and Excel DataFrames.")

    if track_source:
        sql_df["source"] = "sql"
        excel_df["source"] = "excel"

    if prefix_excel_ids:
        excel_df[id_col] = "EX" + excel_df[id_col].astype(str)
    else:
        if not pd.api.types.is_numeric_dtype(sql_df[id_col]):
            raise TypeError(f"'{id_col}' must be numeric for ID shifting.")
        max_id = sql_df[id_col].max()
        excel_df[id_col] = excel_df[id_col] + max_id + 1

    return pd.concat([sql_df, excel_df], ignore_index=True)
