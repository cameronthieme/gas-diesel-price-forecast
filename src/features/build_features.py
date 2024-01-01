'''
Take in .xls files for gas, diesel, crude oil time series
create larger time series with lags
export to .csv
'''

import pandas as pd
import click

# read excel files
# conveniently, all the info we want is on the same labelled page in each file
def read_data(data_path):
    return pd.read_excel(data_path, sheet_name='Data 1', header=2)

# rename inconveniently long columns
def col_rename(df, col_name_og, col_name_short):
    return df.rename(columns={col_name_og:col_name_short})

# shift date (for crude oile to align with others)
def date_shift(df, dayShift=3):
    df['Date'] = df['Date'] + pd.Timedelta(days=dayShift)

# inner joins on 'Date'
def inner_join(df1, df2):
    return pd.merge(df1, df2, on='Date', how='inner')

# add in lags
def lag_add(df, num_differences, colName):
    for i in range(num_differences):
        diffCol = colName + 'Diff' + str(i+1)
        df[diffCol] = df[colName].diff(i+1)

# add target to predict
def make_target(df, target_name, og_col):
    df[target_name] = -df[og_col].diff(-1)

# extract row for prediction of next week
def latest_week(df):
    df_latest_week = df.iloc[-1:].reset_index(drop=True)
    return df_latest_week.drop(['GasChange','DieselChange'], axis=1)

# drop date column
def drop_date(df):
    df.drop('Date', axis=1, inplace=True)


# drop rows which have NA after differencing
def no_NAnsense(df, num_differences):
    df.drop(df.index[:num_differences], inplace=True)
    df.drop(df.index[-1], inplace=True)
    df.reset_index(drop=True, inplace=True)

# save data
def save_data(df, output_path):
    df.to_csv(output_path, index=False)

# column names
# I'm sure there's a "better" way to input these with click arguments
# but this will work for now
bigNameGas = 'Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon)'
bigNameDiesel = 'Weekly U.S. No 2 Diesel Retail Prices  (Dollars per Gallon)'
bigNameCrude = 'Weekly Cushing, OK WTI Spot Price FOB  (Dollars per Barrel)'
lilNameGas = 'Gasoline'
lilNameDiesel = 'Diesel'
lilNameCrude = 'Crude'

# number of differences
num_differences=17

# save model to filepath
@click.command()
@click.argument('gas_input_path', type=click.Path(exists=True))
@click.argument('diesel_input_path', type=click.Path(exists=True))
@click.argument('crude_input_path', type=click.Path(exists=True))
@click.argument('train_output_path', type=click.Path())
@click.argument('test_output_path', type=click.Path())
def main(gas_input_path, 
         diesel_input_path, 
         crude_input_path,
         train_output_path,
         test_output_path):
    
    # read files, rename columns
    df_gas = read_data(gas_input_path)
    df_gas = col_rename(df_gas, bigNameGas, lilNameGas)
    df_diesel = read_data(diesel_input_path)
    df_diesel = col_rename(df_diesel, bigNameDiesel, lilNameDiesel)
    df_crude = read_data(crude_input_path)
    df_crude = col_rename(df_crude, bigNameCrude, lilNameCrude)

    # align crude dates with gas/diesel
    date_shift(df_crude)

    # inner joins
    df = inner_join(df_gas[['Date',lilNameGas]], df_diesel[['Date',lilNameDiesel]])
    df = inner_join(df, df_crude[['Date',lilNameCrude]])
    
    # add differences
    lag_add(df, num_differences, lilNameGas)
    lag_add(df, num_differences, lilNameDiesel)
    lag_add(df, num_differences, lilNameCrude)

    # add target variable
    make_target(df, 'GasChange', 'Gasoline')
    make_target(df, 'DieselChange', 'Diesel')

    # drop date
    drop_date(df)

    # get target variable
    df_latest_week = latest_week(df)

    # drop NA and reset index
    no_NAnsense(df, num_differences)

    # save dataframes as .csv
    save_data(df, train_output_path)
    save_data(df_latest_week, test_output_path)

# get python to run main
if __name__ == "__main__":
    main()

