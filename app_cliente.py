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
        query ='INSERT INTO public.imagenes(path, vector, id_hoja, web_path) VALUES' + value
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

def place(elem):
    '''
    Places element provided into a Column element so that its placement in the layout is retained.
    :param elem: the element to put into the layout
    :return: A column element containing the provided element
    '''
    return sg.Column([[elem]], pad=(0,0))

def main():
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
            place(sg.Text(key='vecino1_id', visible = False)),
            place(sg.Text(key='vecino1_id_hoja', visible = False)),
            place(sg.Text(key='vecino1_distancia', visible = False)),
            place(sg.Text(key='vecino1_path', visible = False)),
            place(sg.Input(key='vecino1_web_path', visible = False)),
            place(sg.Button('Open', key='Open1', visible = False))
        ],
        [
            place(sg.Text(key='vecino2_id', visible = False)),
            place(sg.Text(key='vecino2_id_hoja', visible = False)),
            place(sg.Text(key='vecino2_distancia', visible = False)),
            place(sg.Text(key='vecino2_path', visible = False)),
            place(sg.Input(key='vecino2_web_path', visible = False)),
            place(sg.Button('Open', key='Open2', visible = False))
        ],
        [
            place(sg.Text(key='vecino3_id', visible = False)),
            place(sg.Text(key='vecino3_id_hoja', visible = False)),
            place(sg.Text(key='vecino3_distancia', visible = False)),
            place(sg.Text(key='vecino3_path', visible = False)),
            place(sg.Input(key='vecino3_web_path', visible = False)),
            place(sg.Button('Open', key='Open3', visible = False))
        ],
        [
            place(sg.Text(key='vecino4_id', visible = False)),
            place(sg.Text(key='vecino4_id_hoja', visible = False)),
            place(sg.Text(key='vecino4_distancia', visible = False)),
            place(sg.Text(key='vecino4_path', visible = False)),
            place(sg.Input(key='vecino4_web_path', visible = False)),
            place(sg.Button('Open', key='Open4', visible = False))
        ],
        [
            place(sg.Text(key='vecino5_id', visible=False)),
            place(sg.Text(key='vecino5_id_hoja', visible=False)),
            place(sg.Text(key='vecino5_distancia', visible=False)),
            place(sg.Text(key='vecino5_path', visible=False)),
            place(sg.Input(key='vecino5_web_path', visible = False)),
            place(sg.Button('Open', key='Open5', visible=False))   
        ],
        [
            place(sg.Text(key='vecino6_id', visible = False)),
            place(sg.Text(key='vecino6_id_hoja', visible = False)),
            place(sg.Text(key='vecino6_distancia', visible = False)),
            place(sg.Text(key='vecino6_path', visible = False)),
            place(sg.Input(key='vecino6_web_path', visible = False)),
            place(sg.Button('Open', key='Open6', visible = False)) 
        ],
        [
            place(sg.Text(key='vecino7_id', visible = False)),
            place(sg.Text(key='vecino7_id_hoja', visible = False)),
            place(sg.Text(key='vecino7_distancia', visible = False)),
            place(sg.Text(key='vecino7_path', visible = False)),
            place(sg.Input(key='vecino7_web_path', visible = False)),
            place(sg.Button('Open', key='Open7', visible = False))
        ],
        [
            place(sg.Text(key='vecino8_id', visible = False)),
            place(sg.Text(key='vecino8_id_hoja', visible = False)),
            place(sg.Text(key='vecino8_distancia', visible = False)),
            place(sg.Text(key='vecino8_path', visible = False)),
            place(sg.Input(key='vecino8_web_path', visible = False)),
            place(sg.Button('Open', key='Open8', visible = False))
        ],
        [
            place(sg.Text(key='vecino9_id', visible = False)),
            place(sg.Text(key='vecino9_id_hoja', visible = False)),
            place(sg.Text(key='vecino9_distancia', visible = False)),
            place(sg.Text(key='vecino9_path', visible = False)),
            place(sg.Input(key='vecino9_web_path', visible = False)),
            place(sg.Button('Open', key='Open9', visible = False))
        ],
        [
            place(sg.Text(key='vecino10_id', visible = False)),
            place(sg.Text(key='vecino10_id_hoja', visible = False)),
            place(sg.Text(key='vecino10_distancia', visible = False)),
            place(sg.Text(key='vecino10_path', visible = False)),
            place(sg.Input(key='vecino10_web_path', visible = False)),
            place(sg.Button('Open', key='Open10', visible = False))  
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
            data =f"""('{filename}', {vec}, null, null)"""
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
                window[f'vecino{count}_id'].update(v['id'], visible = True)
                window[f'vecino{count}_id_hoja'].update(v['id_hoja'], visible = True)
                window[f'vecino{count}_distancia'].update(v['distancia'], visible = True)
                window[f'vecino{count}_path'].update(v['path'], visible = True) 
                window[f'vecino{count}_web_path'].update(v['web_path'], visible = True) 
                window[f'Open{count}'].update(visible=True)           
                count+=1
            if (len(vecinos) < 10):
                for x in range(len(vecinos)+1, 11):
                    window[f'vecino{x}_id'].update(visible = False)
                    window[f'vecino{x}_id_hoja'].update(visible = False)
                    window[f'vecino{x}_distancia'].update(visible = False)
                    window[f'vecino{x}_path'].update(visible = False) 
                    window[f'vecino{x}_web_path'].update(visible = False) 
                    window[f'Open{x}'].update(visible=False)  
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

if __name__ == '__main__':
    main()
    