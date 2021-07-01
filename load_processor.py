import xml.dom.minidom as parser
import pandas as pd
#import sqlalchemy
from sqlalchemy import create_engine

def get_data_frame(feilds_list, data_source_map, intermediate_data) :
    df = pd.DataFrame()
    for feild in feilds_list : 
        feild_name = feild.getElementsByTagName('field-name')[0].childNodes[0].data
        feild_source = feild.getElementsByTagName('field-source')[0].childNodes[0].data 
        feild_source_id = feild.getAttribute('sourceId')
        if feild_source_id == '' : 
            df[feild_name] = intermediate_data[feild_source]
        else :
            df[feild_name] = data_source_map[feild_source_id][feild_source]
    return df

def load_csv(destinations,  data_source_map, intermediate_data) :

    for destination in destinations : 
        file_name = destination.getElementsByTagName('file-name')[0].childNodes[0].data
        delemeter = destination.getElementsByTagName('separator')[0].childNodes[0].data
        output_feilds = destination.getElementsByTagName('output')[0].childNodes
        feilds_list = []
        for feild in  output_feilds : 
            if isinstance(feild, parser.Element) : 
                feilds_list.append(feild)
        dataframe = get_data_frame(feilds_list, data_source_map, intermediate_data)
        dataframe.to_csv(file_name,sep=delemeter, index=False)

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        #print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def load_db(destinations,  data_source_map, intermediate_data) :
    for destination in destinations :         
        host_name = destination.getElementsByTagName('hostname')[0].childNodes[0].data
        user_name = destination.getElementsByTagName('username')[0].childNodes[0].data
        user_password = destination.getElementsByTagName('password')[0].childNodes[0].data
        database = destination.getElementsByTagName('database')[0].childNodes[0].data
        database_name = destination.getElementsByTagName('database-name')[0].childNodes[0].data
        table_name = destination.getElementsByTagName('table-name')[0].childNodes[0].data
        output_feilds = destination.getElementsByTagName('output')[0].childNodes
        feilds_list = []
        for feild in  output_feilds : 
            if isinstance(feild, parser.Element) : 
                feilds_list.append(feild)

        #print("{};{}:{}:{}:{}".format(host_name, user_name, user_password, database, table_name))
        dataframe = get_data_frame(feilds_list, data_source_map, intermediate_data)
        engine = None
        if database == 'MYSQL' : 
            engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                    .format(host=host_name, db=database_name, user=user_name, pw=user_password))
        
        dataframe.to_sql(table_name, engine, index=False, if_exists='append')

def load_data(destinations,  data_source_map, intermediate_data) :

    csv_destinations = destinations.getElementsByTagName('csv-load')
    load_csv(csv_destinations,  data_source_map, intermediate_data)

    db_destinations = destinations.getElementsByTagName('db-load')
    load_db(db_destinations,  data_source_map, intermediate_data)