import PySimpleGUI as sg
import psycopg2
from config import config
from PIL import Image
from img2vec_pytorch import Img2Vec
from psycopg2.extras import RealDictCursor
from pathlib import Path


def insert(value):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query ='INSERT INTO public.imagenes(path, vector, id_hoja) VALUES' + value
        cur.execute(query)
        conn.commit()
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def diez_vecinos_mas_cercanos(vec, radio):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query=f'SELECT * FROM diez_vecinos_mas_cercanos({vec}, {radio})'
        cur.execute(query)
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')    

img2vec = Img2Vec(cuda=False)
sg.theme("DarkBlue3")
sg.set_options(font=("Microsoft JhengHei", 16))

layout = [
    [sg.Text('Insertar Nueva Imagen')],
    [
        sg.Input(key='-INPUT-'),
        sg.FileBrowse(file_types=(("JPG Files", "*.jpg"), ("ALL Files", "*.*"))),
        sg.Button("Insert"),
    ],
    [sg.Text('Encontrar 10 vecinos más cercanos')],
    [
        sg.Text('Radio'),
        sg.Input(key='-RADIO-')
    ],
    [
        sg.Text('Imagen'),
        sg.Input(key='-IMAGEN-'),
        sg.FileBrowse(file_types=(("JPG Files", "*.jpg"), ("ALL Files", "*.*"))),
        sg.Button('Open', key='OpenConsulta')
    ],
    [
        sg.Button("Obtener Vecinos")
    ],
     [
        sg.Text(key='id'),
        sg.Text(key='id_hoja'),
        sg.Text(key='distancia'),
        sg.Text(key='path'),

    ],
    [
        sg.Text(key='vecino1_id'),
        sg.Text(key='vecino1_id_hoja'),
        sg.Text(key='vecino1_distancia'),
        sg.Input(key='vecino1_path'),
        sg.Button('Open', key='Open1')
    ],
    [
        sg.Text(key='vecino2_id'),
        sg.Text(key='vecino2_id_hoja'),
        sg.Text(key='vecino2_distancia'),
        sg.Input(key='vecino2_path'),
        sg.Button('Open', key='Open2')
    ],
    [
        sg.Text(key='vecino3_id'),
        sg.Text(key='vecino3_id_hoja'),
        sg.Text(key='vecino3_distancia'),
        sg.Input(key='vecino3_path'),
        sg.Button('Open', key='Open3')
    ],
    [
        sg.Text(key='vecino4_id'),
        sg.Text(key='vecino4_id_hoja'),
        sg.Text(key='vecino4_distancia'),
        sg.Input(key='vecino4_path'),
        sg.Button('Open', key='Open4')
    ],
    [
        sg.Text(key='vecino5_id'),
        sg.Text(key='vecino5_id_hoja'),
        sg.Text(key='vecino5_distancia'),
        sg.Input(key='vecino5_path'),
        sg.Button('Open', key='Open5')   
    ],
    [
        sg.Text(key='vecino6_id'),
        sg.Text(key='vecino6_id_hoja'),
        sg.Text(key='vecino6_distancia'),
        sg.Input(key='vecino6_path'),
        sg.Button('Open', key='Open6') 
    ],
    [
        sg.Text(key='vecino7_id'),
        sg.Text(key='vecino7_id_hoja'),
        sg.Text(key='vecino7_distancia'),
        sg.Input(key='vecino7_path'),
        sg.Button('Open', key='Open7')
    ],
    [
        sg.Text(key='vecino8_id'),
        sg.Text(key='vecino8_id_hoja'),
        sg.Text(key='vecino8_distancia'),
        sg.Input(key='vecino8_path'),
        sg.Button('Open', key='Open8') 
    ],
    [
        sg.Text(key='vecino9_id'),
        sg.Text(key='vecino9_id_hoja'),
        sg.Text(key='vecino9_distancia'),
        sg.Input(key='vecino9_path'),
        sg.Button('Open', key='Open9')
    ],
    [
        sg.Text(key='vecino10_id'),
        sg.Text(key='vecino10_id_hoja'),
        sg.Text(key='vecino10_distancia'),
        sg.Input(key='vecino10_path'),
        sg.Button('Open', key='Open10')  
    ]
]

window = sg.Window('Busqueda por Similitud Imagenes del Espacio', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Insert':
        filename = values['-INPUT-']
        vec = str(img2vec.get_vec(Image.open(filename), tensor=True))
        vec = vec.replace('tensor','ARRAY')
        vec = vec.replace('(','')
        vec = vec.replace(')','')
        data =f"""('{filename}', {vec}, null)"""
        insert(data)
    elif event == 'Obtener Vecinos':
        filename = values['-IMAGEN-']
        radio = values['-RADIO-']
        vec = str(img2vec.get_vec(Image.open(filename), tensor=True))
        vec = vec.replace('tensor','ARRAY')
        vec = vec.replace('(','')
        vec = vec.replace(')','')
        vecinos = diez_vecinos_mas_cercanos(vec, radio)
        count=1
        window['id'].update('id')
        window['id_hoja'].update('id hoja')
        window['distancia'].update('distancia')
        for v in vecinos:
            window[f'vecino{count}_id'].update(v['id'])
            window[f'vecino{count}_id_hoja'].update(v['id_hoja'])
            window[f'vecino{count}_distancia'].update(v['distancia'])
            window[f'vecino{count}_path'].update(v['path'])            
            count+=1
    elif event == 'OpenConsulta':
        filename = values['-IMAGEN-']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open1':
        filename = values['vecino1_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open2':
        filename = values['vecino2_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open3':
        filename = values['vecino3_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open4':
        filename = values['vecino4_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open5':
        filename = values['vecino5_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open6':
        filename = values['vecino6_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open7':
        filename = values['vecino7_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open8':
        filename = values['vecino8_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open9':
        filename = values['vecino9_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    elif event == 'Open10':
        filename = values['vecino10_path']
        if Path(filename).is_file():
            try:
                img = Image.open(filename)
                img.show() 
            except Exception as e:
                print("Error: ", e)
    
window.close()


    