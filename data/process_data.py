import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    '''
        load in messages and categories data, output merged dataset

    :param messages_filepath: file path for message data
    :param categories_filepath: file path for categories data
    '''
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    # merge datasets
    df = pd.merge(messages, categories, how = 'inner' , on = 'id')

    return df


def clean_data(df):
    '''
        - Split the values in the `categories` column on the `;`.
        - Use the first row of categories dataframe to create '\
        'column names for the categories data.
        - Rename columns of `categories` with new column names.
        - Convert category values to just numbers 0 or 1
        - Replace categories column in df with new category
        - Remove duplicates
    '''
    # create a dataframe of the 36 individual category columns
    categories = pd.DataFrame(df.categories.str.split(';',expand=True))
    # select the first row of the categories dataframe
    row = categories.iloc[0,:]
    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything
    # up to the second to last character of each string with slicing
    category_colnames = row.str.split('-').apply(lambda x:x[0])
    # rename the columns of `categories`
    categories.columns = category_colnames
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1:])

        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
    # drop the original categories column from 'df'
    df.drop('categories', axis=1)

    # concatenate the original dataframe with the new 'categories' dataframe
    df = pd.concat([df, categories], axis=1)

    # drop duplicates
    df.drop_duplicates(inplace=True)
    filtered = df[df['related']==2]
    df = df.drop(filtered.index)

    return df

def save_data(df, database_filename):
    '''
        Save data into database
    :param df: input data
    :param database_filename: database file name
    '''
    # save the clean dataset into an sqlite database
    engine = create_engine('sqlite:///database_filename.db')
    df.to_sql('database_response', engine, if_exists='replace', index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
