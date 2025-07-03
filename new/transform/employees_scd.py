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

                duplicate = history_df[
                    (history_df['employee_id'] == new_entry['employee_id']) &
                    (history_df['designation'] == new_entry['designation']) &
                    (history_df['branch_id'] == new_entry['branch_id']) &
                    (history_df['start_date'] == today)
                ]
                if duplicate.empty:
                    updated_rows.append(new_entry)

        elif emp_id not in history_df['employee_id'].values:
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
    import datetime as dt

    incoming_df['branch_id'] = pd.to_numeric(incoming_df['branch_id'], errors='coerce')
    incoming_df = incoming_df.dropna(subset=['branch_id'])
    incoming_df['branch_id'] = incoming_df['branch_id'].astype(int)

    today = pd.to_datetime(dt.date.today())

    current_df = current_df.copy()
    history_df = history_df.copy()

    for _, row in incoming_df.iterrows():
        emp_id = row['employee_id']
        match = current_df[current_df['employee_id'] == emp_id]

        if match.empty:
            new_record = row.copy()
            new_record['start_date'] = today
            new_record['end_date'] = pd.NaT
            new_record['is_current'] = True
            current_df = pd.concat([current_df, pd.DataFrame([new_record])], ignore_index=True)
            history_df = pd.concat([history_df, pd.DataFrame([new_record])], ignore_index=True)

        else:
            current_row = match.iloc[0]

            if row['designation'] != current_row['designation'] or row['branch_id'] != current_row['branch_id']:
                current_df.loc[current_df['employee_id'] == emp_id, 'is_current'] = False
                current_df.loc[current_df['employee_id'] == emp_id, 'end_date'] = today

                new_row = row.copy()
                new_row['start_date'] = today
                new_row['end_date'] = pd.NaT
                new_row['is_current'] = True

                duplicate = history_df[
                    (history_df['employee_id'] == new_row['employee_id']) &
                    (history_df['designation'] == new_row['designation']) &
                    (history_df['branch_id'] == new_row['branch_id']) &
                    (history_df['start_date'] == today)
                ]
                if duplicate.empty:
                    current_df = pd.concat([current_df, pd.DataFrame([new_row])], ignore_index=True)
                    history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)

            elif row['email'] != current_row['email']:
                current_df.loc[current_df['employee_id'] == emp_id, 'email'] = row['email']

    return current_df, history_df