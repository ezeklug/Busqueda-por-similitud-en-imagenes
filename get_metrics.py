from typing import Dict, List, Tuple
from psycopg2.extras import RealDictCursor
from app_cliente import diez_vecinos_mas_cercanos
from img2vec_pytorch import Img2Vec
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
    def from_tuple(t: Tuple) -> 'Vecino':
        vec = Vecino()
        vec.id = t['id']
        vec.path = t['path']
        vec.id_hoja = t['id_hoja'],
        vec.web_path = t['web_path'],
        vec.distancia = t['distancia']
        return vec


def get_file_names() -> List[str]:
    file_name = sys.argv[1]
    names = []
    with open(file_name, 'r') as f:
        for line in f:
            names.append(line.replace('\n', ''))
    return names


def rotate_image(file_name: str, save_folder='tmp_modified_imgs'):
    """
    Rotates an image by 90 deg
    Stores the result image with the same name inside save_folder'
    """
    name, extension = file_name.rsplit('.', 1)
    try:
        colorImage = Image.open(file_name)
        # Rotate it by 90 degrees
        modified = colorImage.transpose(Image.ROTATE_90)
        modified.save(f'{save_folder}/{name}.{extension}')
    except FileNotFoundError as err:
        print(f"File {err.filename} does not exists")


def modify_pixels_random(file_name: str, pixels_to_modify: int, save_folder='tmp_modified_imgs'):
    """
    Modifies random pixels in an image by random values
    Stores the result image with the same name inside save_folder'
    """
    name, extension = file_name.rsplit('.', 1)
    try:
        im = Image.open(file_name)
        pixelMap = im.load()

        img = Image.new(im.mode, im.size)
        pixelsNew = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixelsNew[i, j] = pixelMap[i, j]

        def rd(): return random.randint(0, 255)
        for _ in range(pixels_to_modify):
            x = random.randrange(0, im.size[0])
            y = random.randrange(0, im.size[1])
            pixelsNew[x, y] = (rd(), rd(), rd(), rd())
        img.save(f'{save_folder}/{name}.{extension}')
    except FileNotFoundError as err:
        print(f"File {err.filename} does not exists")


def modify_imgs(imgs_path: List[str]):
    """
    Modifies and store a list of images. Half of them will be rotated and other half with noise.
    """
    i = 0
    for img in imgs_path:
        if i == 0:
            modify_pixels_random(img, 50_000)
            i += 1
        else:
            rotate_image(img)
            i -= 1


def ten_closest_neighbors(vec, radius: float) -> List[Vecino]:
    data = diez_vecinos_mas_cercanos(vec, radius)
    vecinos = []
    for t in data:
        vecinos.append(Vecino.from_tuple(t))
    return vecinos


def img_2_arr_str(img_name: str) -> str:
    """
    Returns the array signatura of an image in SQL format
    i.e ARRAY[1,2,3,...,4,5,3]
    """
    img2vec = Img2Vec(cuda=False)
    vec = str(img2vec.get_vec(Image.open(img_name), tensor=True))
    vec = vec.replace('tensor', 'ARRAY')
    vec = vec.replace('(', '')
    vec = vec.replace(')', '')
    return vec


def count_hits(orig: List[Vecino], mod: List[Vecino]) -> int:
    i = 0
    for m in mod:
        if m.id in [o.id for o in orig]:
            i += 1
    return i


def print_metrics(neighbors: Dict[str, Dict[str, List]]):
    print("Name, Hits")
    for key, d in neighbors.items():
        orig = d['or']
        mod = d['md']
        print(f"{key}, {count_hits(orig,mod)}")


def main():
    if len(sys.argv) != 2:
        print("Only one argument requiered: file name of file text with name of pictures to compare")
        exit()

    radius = 10
    folder_name = 'tmp_modified_imgs'
    file_names = get_file_names()
    neighbors = {}

    # Calculate the signature array of each original image
    for file_name in file_names:
        neighbors[file_name] = {'or': ten_closest_neighbors(
            img_2_arr_str(file_name), radius)}

    try:
        # Creates the folder to store modified images
        os.mkdir(folder_name)
    except FileExistsError:
        # If already exists, remove the folder and re-creates it
        shutil.rmtree(folder_name)
        os.mkdir(folder_name)

    modify_imgs(file_names)

    # calculate the signature array of each modified image
    for mod_img in os.listdir(folder_name):
        neighbors[mod_img]['md'] = ten_closest_neighbors(
            img_2_arr_str(f'{folder_name}/{mod_img}'), radius)

    print_metrics(neighbors)


if __name__ == '__main__':
    main()
