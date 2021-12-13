import random
from img2vec_pytorch import Img2Vec
from typing import List
from PIL import Image


def rotate_image(file_name: str, save_folder='tmp_modified_imgs'):
    """
    Rotates an image by 90 deg
    Stores the result image with the same name inside save_folder'
    """
    name, extension = file_name.split('.')
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
    name, extension = file_name.split('.')
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


def img_2_arr_str(img_name: str) -> str:
    """
    Returns the array signature of an image in SQL format
    i.e ARRAY[1,2,3,...,4,5,3]
    """
    img2vec = Img2Vec(cuda=False)
    vec = str(img2vec.get_vec(Image.open(img_name), tensor=True))
    vec = vec.replace('tensor', 'ARRAY')
    vec = vec.replace('(', '')
    vec = vec.replace(')', '')
    return vec
