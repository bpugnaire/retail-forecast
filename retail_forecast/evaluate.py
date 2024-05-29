from sklearn.metrics import mean_squared_error

def dataframe_to_dict(df_test):
    test_data = df_test.groupby(['store-dep', 'day_id'])['turnover'].sum().reset_index()
    df_dict = {}
    for store_dep in test_data['store-dep'].unique():
        df_dict[store_dep] = test_data[test_data['store-dep'] == store_dep]
        df_dict = df_dict[['day_id', 'turnover']]
        df_dict.columns = ['ds', 'y']
    return df_dict

def evaluate(predictions, df_test):
    df_dict_test = dataframe_to_dict(df_test)
    global_mse = 0
    for store_dep in df_dict_test:
        y = df_dict_test[store_dep]
        mse = mean_squared_error(y['y'], predictions[store_dep]['yhat'])
        global_mse += mse
    global_mse /= len(df_dict_test)
    return global_mse