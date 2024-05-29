from prophet import Prophet
from prophet.serialize import model_to_json
import logging

logger = logging.getLogger(__name__)

def save_model(model_dict):
    try:
        for store_dep, model in model_dict.items():
            with open(f'models/{store_dep}.json', 'w') as f:
                f.write(model_to_json(model))
        logger.info('Models saved successfully')
    except Exception as e:
        logger.error(f'Error saving models: {e}')
        

def train(df_train):
    train_data = df_train.groupby(['store-dep', 'day_id'])['turnover'].sum().reset_index()
    model_dict = {}
    for store_dep in train_data['store-dep'].unique():
        try :
            train_dpt = train_data[train_data['store-dep'] == store_dep]
            train_dpt = train_dpt[['day_id', 'turnover']]
            train_dpt.columns = ['ds', 'y']
            model = Prophet()
            model.fit(train_dpt)
            model_dict[store_dep] = model
        except Exception as e:
            logger.error(f'{e} in training model for {store_dep}')
    logger.info('Models trained successfully')
    save_model(model_dict)

          