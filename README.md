gas-diesel-price-forecast
==============================

Welcome to my gas/diesel price forecasting repository! This project predicts the average prices of gas and diesel in the United States for the coming week.

A major motivation in setting up this project was to develop skills in CI/CD technology. The <a target="_blank" href="https://www.eia.gov">US Energy Information Administration</a> updates information on the average prices of gasoline, diesel, and crude oil every week, and this project automatically incorporates this updated data in order to make a forecast for the coming week.  

Once the current data is downloaded, it is organized into a dataframe with lagged variables.  Then two XGBoost models (one for gas and one for diesel) are trained on this information and predictions for the coming week are made.  The parameters for the XGBoost models were selected using Bayesian Optimization in the notebook 'diesel-price-prediction.ipynb'.  

There are lots of different pieces of software utilized in this project: Docker, Makefile, virtual environments, git, and several AWS technologies (ECR & EC2, both of which included dealing with navigating AWS frameworks and permissions).  I've tried to keep this project well organized at every level, from the folder structure down to the individual python files.

I'm placing instructions here for running this project in two different ways. You can either run the project by cloning this repo, or by pulling a docker image hosted on AWS. These instructions are designed for use with a Linux EC2 instance that has been initialized with 29Gb of memory (just under the free limit).  

## Method 1: Cloning this Repo and Download from Kaggle

This method is super simple. All you need to do is clone this repo, enter that directory, and run one make command:
```
make full-process
```
The model predictions will print after that.

For those using an EC2 instance, you will need to install a few dependencies before running 'make full-process'.
```
sudo yum install -y git
sudo yum groupinstall "Development Tools"
```
You may also want to activate a virtual environment before running 'make full-process', as it will install several packages, and may cause dependency issues for other projects.  

## Method 2: Elastic Container Registry (ECR)

Start out by installing and initializing docker in your EC2 instance:
```
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```
Pull the image from my ECR:
```
sudo docker image pull public.ecr.aws/g1s9w1h5/gas-diesel:latest
```
Run the forecast:
'''
sudo docker run public.ecr.aws/g1s9w1h5/gas-diesel:latest
'''

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. 
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    |
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
