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
    select
    species_id,
    species_name,
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
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

    