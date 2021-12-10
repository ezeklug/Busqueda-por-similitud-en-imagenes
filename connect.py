#!/usr/bin/python
import psycopg2
from config import config
from PIL import Image
import json
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')

        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        
        print('Reading json file')
        query = f"INSERT INTO public.imagenes(path, vector, id_hoja, web_path) VALUES"
        with open('data.txt') as json_file:
            data = json.load(json_file)
            for p in data['imagenes']:
                path = p['path']
                vector = p['vector']
                web_path = p['web_path']
                query+=f"('{path}', ARRAY{vector}, null, '{web_path}'),"
            query = query[:-1] + ';'
            print('json file read successfully')
        print('Executing Insert query')
        cur.execute(query)
        print('Commiting')
        conn.commit()

        
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()