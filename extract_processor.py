import xml.dom.minidom as parser
import pandas as pd

def extract_csv_sources(csv_source_list, source_map, rows_read) :
    for idx,csv_source in  enumerate(csv_source_list) : 
        sourceId = csv_source.getAttribute("sourceId")
        #source_map[sourceId] = pd.Dataframe()
        window_size = int(csv_source.getElementsByTagName('windowsize')[0].firstChild.nodeValue)
        file_path = csv_source.getElementsByTagName('file-path')[0].firstChild.nodeValue
        df = pd.read_csv(file_path, nrows=window_size, skiprows=range(1,rows_read[idx]+1))
        #if df.shape[0] > 0 :
        source_map[sourceId] = df
        rows_read[idx] = rows_read[idx]+df.shape[0]
    return source_map, rows_read

def extract_db_sources(db_source_list, source_map, rows_read) :
    for db_source in  db_source_list : 
        sourceId = db_source.getAttribute("sourceId")
        #rest needs to be code as per requirement
    return source_map, rows_read

def extract_data(sources, rows_read) : 

    source_map = dict()

    csv_source_list = sources.getElementsByTagName('csv-extract')
    if(rows_read['csv'] == None) : 
        rows_read['csv'] = [0 for i in csv_source_list]
    source_map, csv_rows_read = extract_csv_sources(csv_source_list, source_map, rows_read['csv'])

    db_source_list = sources.getElementsByTagName('db-extract')
    if(rows_read['db'] == None) : 
        rows_read['db'] = [0 for i in db_source_list]
    source_map, db_rows_read = extract_db_sources(db_source_list, source_map, rows_read['db'])

    rows_read['csv'] = csv_rows_read
    rows_read['db'] = db_rows_read

    return source_map, rows_read

    
