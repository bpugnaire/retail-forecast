# Retail Forecast

Welcome to the Retail Forecast project. This project is designed to predict the turnover of retail data and visualize the results. The codebase is structured into three main parts: Jupyter notebooks for data exploration and answering preliminary questions, a prediction pipeline for training and evaluating the model, and a Dash app for data visualization.

## Installation

Use the package manager [poetry](https://python-poetry.org/docs/) to install the necessary dependencies.

```bash
poetry install
poetry shell
```

## Exploring the Data with Notebooks

data_exploration.ipynb: This is where I started understanding the dataset.
partie2_preliminary_questions.ipynb: This notebook contains part 2 questions and their answers.
partie3_multi-step_forecasting.ipynb: This notebook is used for multi-step forecasting and asnwering the first 2 questions of part 3.

## Launching the Prediction Pipeline
To start the prediction pipeline:
```bash
python retail_forecast/pipeline.py 
```
As is, it will start the pipeline, create the model files and train on the full train.csv data.

## Visualizing the Data with Dash
Finally, you can visualize the data using the Dash app located in the `dataviz/` directory. 
The `app.py` file contains a Dash application that loads the model and displays a simple turnover timeseries visualization.

To run the Dash app, execute the following command:
```bash
python dataviz/app.py
```
This will start the Dash app, which you can access by navigating to http://localhost:8050 in your web browser.
