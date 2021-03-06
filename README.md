# Disaster Response Pipeline Project

In this project, disaster messages data were collected from Figure Eight. I built a data pipeline that cleaned and trained the machine learning model that categorizes emergency messages based on the needs communicated by sender. This data pipeline is connected to a web portal through API that can display the classification results. 

1. [Table of Contents](#Table_of_Contents)
2. [File Descriptions](#File_Descriptions)
3. [Instructions](#Instructions)
4. [Licensing, Authors, and Acknowledgements](#Licensing,_Authors,_and_Acknowledgements)

### File Descriptions:
`process_data.py`: A ETL Pipeline that

- loads the messages and categories datasets
- merges the two datasets
- cleans the data
- stores it in a SQLite database

`train_classifier.py`: A Machine Learning Pipeline that

- loads data from the SQLite database
- splits the dataset into training and test sets
- builds a text processing and machine learning pipeline
- trains and tunes a model using GridSearchCV
- outputs results on the test set
- exports the final model as a pickle file

`run.py`: A Flask Web App that visualizes the results

### Instructions:
Run the following commands in the project's root directory to set up your database and model.

To run ETL pipeline that cleans data and stores in database `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`

To run ML pipeline that trains classifier and saves `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

Run the following command in the app's directory to run your web app. `python run.py`

Go to http://0.0.0.0:3001/

### Licensing, Authors, Acknowledgements
Dataset was collected through Figure Eight.
