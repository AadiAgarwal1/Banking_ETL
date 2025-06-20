import pandas as pd
from transform.merge_sources import merge_sources

def service_subscriptions(customerservices_sql, services_sql,customerservices_excel=pd.DataFrame(), services_excel=pd.DataFrame()):
    cs_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")
    s_df = merge_sources(services_sql, services_excel, "service_id")
    merged = cs_df.merge(s_df, on='service_id')
    return merged.groupby('service_name').size().reset_index(name='Subscribers')

def unused_services(services_sql, customerservices_sql,services_excel=pd.DataFrame(), customerservices_excel=pd.DataFrame()):
    s_df = merge_sources(services_sql, services_excel, "service_id")
    cs_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")
    used_service_ids = cs_df['service_id'].unique()
    return s_df[~s_df['service_id'].isin(used_service_ids)]

def multi_service_customers(customerservices_sql, customerservices_excel=pd.DataFrame(), min_services=2):
    cs_df = merge_sources(customerservices_sql, customerservices_excel, "service_id")
    usage = cs_df.groupby('customer_id').size().reset_index(name='Services_Used')
    return usage[usage['Services_Used'] >= min_services]
