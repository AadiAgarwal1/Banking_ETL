from datetime import date
import pandas as pd

IMMUTABLE_COLUMNS = ['employee_id']

def apply_scd_type_1(current_df, incoming_df, cols_to_check=['email']):
    merged = current_df.merge(incoming_df, on='employee_id', suffixes=('_curr', '_new'))
    for col in cols_to_check:
        changed = merged[f'{col}_curr'] != merged[f'{col}_new']
        current_df.loc[merged[changed].index, col] = merged.loc[changed, f'{col}_new'].values
    return current_df

def apply_scd_type_2(history_df, incoming_df):
    today = date.today()
    updated_rows = []

    for _, new_row in incoming_df.iterrows():
        emp_id = new_row['employee_id']
        existing = history_df[(history_df['employee_id'] == emp_id) & (history_df['is_current'])]

        if not existing.empty:
            existing_row = existing.iloc[0]
            scd_cols = ['designation', 'branch_id']

            if any(existing_row[col] != new_row[col] for col in scd_cols):
                history_df.loc[existing.index, 'is_current'] = False
                history_df.loc[existing.index, 'end_date'] = today

                new_entry = new_row.to_dict()
                new_entry.update({'start_date': today, 'end_date': None, 'is_current': True})
                updated_rows.append(new_entry)

        elif emp_id not in history_df['employee_id'].values:
            # New employee, insert fresh
            new_entry = new_row.to_dict()
            new_entry.update({'start_date': today, 'end_date': None, 'is_current': True})
            updated_rows.append(new_entry)

    if updated_rows:
        history_df = pd.concat([history_df, pd.DataFrame(updated_rows)], ignore_index=True)

    return history_df

def apply_scd_type_3(current_df, incoming_df):
    merged = current_df.merge(incoming_df, on='employee_id', suffixes=('_curr', '_new'))

    for _, row in merged.iterrows():
        idx = current_df[current_df['employee_id'] == row['employee_id']].index[0]

        if row['designation_curr'] != row['designation_new']:
            current_df.loc[idx, 'previous_designation'] = row['designation_curr']
            current_df.loc[idx, 'designation'] = row['designation_new']

        if row['branch_id_curr'] != row['branch_id_new']:
            current_df.loc[idx, 'previous_branch_id'] = row['branch_id_curr']
            current_df.loc[idx, 'branch_id'] = row['branch_id_new']

    return current_df

def transform_employees(current_df, incoming_df, history_df):
    # Apply Type 1
    current_df = apply_scd_type_1(current_df, incoming_df, ['email'])

    # Apply Type 2
    history_df = apply_scd_type_2(history_df, incoming_df)

    # Apply Type 3
    current_df = apply_scd_type_3(current_df, incoming_df)

    return current_df, history_df
