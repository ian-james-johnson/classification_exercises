import numpy as np
import pandas as pd
import os
from env import host, user, password

def get_connection(db, user=user, host=host, password=password):
    '''
    This function creates a connection to the Codeup db.
    It takes db argument as a string name.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_titanic_data():
    '''
    This function reads titanic table from db, converts it into a df, and then exports it as a csv.
    Finally, the function returns a df
    '''
    sql_query='select * from passengers'
    df=pd.read_sql(sql_query, get_connection('titanic_db'))
    return df

def get_titanic_data():
    '''
    This function writes from Codeup db if csv file does not exit, and returns a df
    '''
    if os.path.isfile('titanic_df.csv'):
        # if this csv exists, then read it
        df=pd.read_csv('titanic_df.csv', index_col=0)

    else:
        # read the data from Codeup db
        df = new_titanic_data()
        df.to_csv('titanic_df.csv')
    return df

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def new_iris_data():
    '''
    This function reads the Iris data from the Codeup db into a df
    '''
    sql_query= """
    select *
    from measurements
    join species using(species_id)
    """
    df=pd.read_sql(sql_query, get_connection('iris_db'))
    return df

def get_iris_data():
    if os.path.isfile('iris_df.csv'):
        df=pd.read_csv('iris_df.csv', index_col=0)
    else:
        df=new_iris_data()
        df.to_csv('iris_df.csv')
    return df

def prep_iris(df):
    iris_df = df.drop(columns = ['species_id', 'measurement_id'])
    iris_df = iris_df.rename(columns= {'species_name':'species'})
    dummy_df= pd.get_dummies(iris_df['species'], dummy_na = False, drop_first=False)
    iris_df= pd.concat([iris_df, dummy_df], axis=1)
    train, test = train_test_split(iris_df, test_size=0.2, random_state=1349, stratify=iris_df.species)
    train, validate = train_test_split(train, train_size=0.7, random_state=1349, stratify=train.species)
    return train, validate, test