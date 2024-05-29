import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def load_data(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f'Error loading data from {path}: {e}')
        return None

def format_dataframe(df_train):
    try:
        df_train['day_id'] = pd.to_datetime(df_train['day_id'], format='%Y-%m-%d')
        df_train['year'] = df_train['day_id'].dt.year
        df_train['month'] = df_train['day_id'].dt.month
        df_train['day'] = df_train['day_id'].dt.day
        df_train['week_nb'] = df_train['day_id'].dt.isocalendar().week
        df_train['store-dep'] = df_train['but_num_business_unit'].astype(str) + '-' + df_train['dpt_num_department'].astype(str)
        df_train.sort_values(by=['store-dep','day_id'], inplace=True)
        return df_train
    except Exception as e:
        logger.error(f'Error formatting dataframe: {e}')
        return None
    

def remove_outliers(df_train):
    try:
        df_train['is_outlier'] = False
        for store_dep in df_train['store-dep'].unique():
            # check for outliers in the turnover column
            df_store_dep = df_train[df_train['store-dep'] == store_dep]
            Q1 = df_store_dep['turnover'].quantile(0.25)
            Q3 = df_store_dep['turnover'].quantile(0.75)
            IQR = Q3 - Q1
            df_outliers = df_store_dep[(df_store_dep['turnover'] < (Q1 - 5 * IQR)) | (df_store_dep['turnover'] > (Q3 + 5 * IQR))]
            df_train.loc[df_outliers.index, 'is_outlier'] = True

        df_train.loc[df_train[df_train['is_outlier']].index, 'turnover'] = np.nan

        for store_dep in df_train['store-dep'].unique():
            df_store_dep = df_train[df_train['store-dep'] == store_dep]
            df_store_dep.loc[:,'turnover'] = df_store_dep['turnover'].interpolate() # interpolate missing values
            df_store_dep.loc[:, 'turnover'] = df_store_dep['turnover'].fillna(df_store_dep['turnover'].mean()) # fill remaining missing values with the mean
            df_train.loc[df_store_dep.index, 'turnover'] = df_store_dep['turnover']
        
        return df_train
    except Exception as e:
        logger.error(f'Error removing outliers: {e}')
        return None

def preprocessing(path):
    df_train = load_data(path)
    df_train = format_dataframe(df_train)
    df_train = remove_outliers(df_train)
    return df_train
