import numpy as np
from typing import Dict, List, Tuple
from psycopg2.extras import RealDictCursor
from app_cliente import diez_vecinos_mas_cercanos, connect, disconnect
from img2vec_pytorch import Img2Vec
from img_utils import modify_imgs, img_2_arr_str
import random
import os
import shutil
from PIL import Image
import sys

# CREATE TYPE vecino AS(
# id integer,
# path VARCHAR(255),
# id_hoja bigint,
# web_path VARCHAR(3086),
# distancia double precision
# );


class Vecino:
    def from_dic(d: Dict) -> 'Vecino':
        vec = Vecino()
        vec.id = d['id']
        vec.path = d['path']
        vec.id_hoja = d['id_hoja'],
        vec.web_path = d['web_path'],
        vec.distancia = d['distancia']
        return vec


def get_file_names() -> List[str]:
    file_name = sys.argv[1]
    names = []
    with open(file_name, 'r') as f:
        for line in f:
            names.append(line.replace('\n', ''))
    return names


def ten_closest_neighbors(vec, radius: float, conn) -> List[Vecino]:
    data = diez_vecinos_mas_cercanos(vec, radius, conn)
    vecinos = []
    for d in data:
        vecinos.append(Vecino.from_dic(d))
    return vecinos


def print_hits_ret_accuracy(orig: List[Vecino], mod: List[Vecino]) -> float:
    """Print how many hit a query had.
    Returns the accuracy"""
    n = 5
    i = 0
    for i in range(n):
        if orig[i].id == mod[i].id:
            i += 1

    print(f"Hit {i} of {n}")
    print("Accuracy %.2f" % ((i/n) * 100))


def print_first_assertion(orig: List[Vecino], mod: List[Vecino]):
    print("First assertion: ", end='')
    if orig[0].id == mod[0].id:
        print("✅")
    else:
        print("❌")


def print_metrics(neighbors: Dict[str, Dict[str, List]]):
    accuracy = []
    for key, d in neighbors.items():
        orig = d['or']
        mod = d['md']

        print(key)
        print_first_assertion(orig, mod)
        acc = print_hits_ret_accuracy(orig, mod)
        accuracy.append(acc)
        print()
    accs = np.array(accuracy)
    print("Global accuracy: %.2f std: %.2f" % (accs.mean(), accs.std()))


def main():
    if len(sys.argv) != 2:
        print("Only one argument requiered: file name of file text with name of pictures to compare")
        exit()

    radius = 0.3
    folder_name = 'tmp_modified_imgs'
    file_names = get_file_names()
    neighbors = {}
    print('OBTUVE LOS NOMBRES')
    conn = connect()

    # Calculate the signature array of each original image
    for file_name in file_names:
        neighbors[file_name] = {'or': ten_closest_neighbors(
            img_2_arr_str(file_name), radius, conn)}
    print('CREE LOS ARRAYS')
    try:
        # Creates the folder to store modified images
        os.mkdir(folder_name)
    except FileExistsError:
        pass

    modify_imgs(file_names)
    print('MODIFIQUE LAS IMAGENES')
    # calculate the signature array of each modified image
    for mod_img in os.listdir(folder_name):
        neighbors[mod_img]['md'] = ten_closest_neighbors(
            img_2_arr_str(f'{folder_name}/{mod_img}'), radius, conn)

    print_metrics(neighbors)

    disconnect(conn)


if __name__ == '__main__':
    main()
