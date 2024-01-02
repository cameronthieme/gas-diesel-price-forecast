'''
Importing pre-built model
Predicting values of test data
'''

from xgboost import XGBRegressor
import numpy as np
import pandas as pd
import click

def get_model(model_path):
    xgb = XGBRegressor() # initialize model
    xgb.load_model(model_path)  # load data
    return xgb

# get testing data
def get_test_data(test_path):
    return pd.read_csv(test_path)

# function that predicts
def pred_target(df_test, xgb, which_pred):
    return xgb.predict(df_test)[0] + df_test[which_pred][0]

# Print the latest date and prices.
def latest_info_printer(df_test, date_path):
    # read .txt file
    with open(date_path, 'r') as file:
        content = file.read()
    # Split the content at the space character and take the first part
    date_time_str = content.split()[0]
    # Extract the date part
    date_str = date_time_str.split()[0]
    # print Latest Date and prices
    print('****************************************')
    print('Gasoline and Diesel Prediction information:')
    print('The most recent date for price information is ' + date_str)
    # print prices
    print('Current price of Gasoline is $' + str(df_test.iloc[-1]['Gasoline']))
    print('Current price of Diesel is $' + str(df_test.iloc[-1]['Diesel']))


# save prediction to filepath
@click.command()
@click.argument('test_data_path', type=click.Path(exists=True))
@click.argument('gas_model_path', type=click.Path(exists=True))
@click.argument('diesel_model_path', type=click.Path(exists=True))
@click.argument('date_path', type=click.Path(exists=True))
def main(test_data_path, gas_model_path, diesel_model_path, date_path):
    df_test = get_test_data(test_data_path)
    latest_info_printer(df_test, date_path)
    model_gas = get_model(gas_model_path)
    print('Predicted Price of Gasoline Next Week: $' + str(pred_target(df_test,model_gas, 'Gasoline')))
    model_diesel = get_model(diesel_model_path)
    print('Predicted Price of Diesel Next Week: $' + str(pred_target(df_test, model_diesel, 'Diesel')))

# # save model to filepath
# @click.command()
# @click.argument('test_data_path', type=click.Path(exists=True))
# @click.argument('model_path', type=click.Path(exists=True))
# @click.argument('output_pred_path', type=click.Path())
# def main(test_data_path, model_path, output_pred_path):
#     df_test = get_test_data(test_data_path)
#     df_features = get_test_features(df_test)
#     model = get_model(model_path)
#     y_pred = pred_target(df_features, model)
#     save_data(y_pred, output_pred_path)

# get python to run main
if __name__ == "__main__":
    main()
