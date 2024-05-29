from preprocessing import preprocessing, load_data
from train import train
from evaluate import evaluate
from predict import predict
import logging


logger = logging.getLogger(__name__)

def launch_prediction_pipeline(train_data_path, test_data_path, training=True, evaluation=True):
    print('Prediction pipeline launched')
    df_train = preprocessing(train_data_path)
    print("Preprocessing done")
    if df_train is None:
        return None
    if training:
        train(df_train)
        print("Training done")
    predictions = predict()
    if evaluation:
        df_test = load_data(test_data_path)
        df_test['store-dep'] = df_test['but_num_business_unit'].astype(str) + '-' + df_test['dpt_num_department'].astype(str)
        if df_test is None:
            return None
        mse = evaluate(predictions, df_test)
        logger.info(f'Mean Squared Error: {mse}')
    print("Prediction pipeline completed")
    return predictions

if __name__ == '__main__':
    launch_prediction_pipeline('data/train.csv', 'data/test.csv', training=False)