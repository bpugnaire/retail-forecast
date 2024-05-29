from prophet.serialize import model_from_json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

    
def load_model():
    try:
        model_dict = {}
        # iterate over all json files in the models directory using pathlib Path
        for file_path in Path('models').glob('*.json'):
            with open(file_path, 'r') as f:
                model_dict[file_path.stem] = model_from_json(f.read())
        logger.info('Models loaded successfully')
        return model_dict
    except Exception as e:
        logger.error(f'Error loading models: {e}')
        return None
    

def get_predictions(model, periods=8):
    future = model.make_future_dataframe(periods=periods,freq='W')
    return model.predict(future)

def predict(periods=8):
    model_dict = load_model()
    if model_dict is None:
        return None
    predictions = {}
    for store_dep, model in model_dict.items():
        try:
            predictions[store_dep] = get_predictions(model,periods=periods)
        except Exception as e:
            logger.error(f'Error predicting for {store_dep}: {e}')
    return predictions
    
