import pandas as pd
from xgboost import XGBRegressor
import click


# get training data
def get_train_data(path):
    return pd.read_csv(path)
    
def get_trained_xgboost(df_train, target_column, best_params):
    # target and features
    X = df_train.drop(columns = ['GasChange','DieselChange'])
    y = df_train[target_column]

    # Create an XGBoost regressor model
    xgb = XGBRegressor(
        objective ='reg:squarederror',
        n_estimators=int(best_params['n_estimators']),
        learning_rate=best_params['learning_rate'],
        alpha=best_params['alpha'],
        reg_lambda=best_params['reg_lambda'],
        colsample_bytree=best_params['colsample_bytree'],
        max_depth=int(best_params['max_depth'])
    )

    # train and return model
    xgb.fit(X,y)
    return xgb

params_gas = {'alpha': 2.021851869532555, 'colsample_bytree': 0.3356887204578178, 'learning_rate': 0.22354828682458217, 'max_depth': 1.5313928160873287, 'n_estimators': 639.4984109307318, 'reg_lambda': 31.731202615851384}
params_diesel = {'alpha': 0.9451594965588395, 'colsample_bytree': 0.6032657896492717, 'learning_rate': 0.03371559259538288, 'max_depth': 2.654342627535919, 'n_estimators': 517.879878690663, 'reg_lambda': 7.272143336321744}

# save model to filepath
@click.command()
@click.argument('train_data_filepath', type=click.Path(exists=True))
@click.argument('gas_output_model_filepath', type=click.Path())
@click.argument('diesel_output_model_filepath', type=click.Path())
def main(train_data_filepath, gas_output_model_filepath, diesel_output_model_filepath):
    df_train = get_train_data(train_data_filepath)
    model = get_trained_xgboost(df_train, 'GasChange', params_gas)
    model.save_model(gas_output_model_filepath)
    model = get_trained_xgboost(df_train, 'DieselChange', params_diesel)
    model.save_model(diesel_output_model_filepath)

# get python to run main
if __name__ == "__main__":
    main()