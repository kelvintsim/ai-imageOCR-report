import os
from PIL import Image
import numpy as np
from collections import defaultdict

def average_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # returns a tuple (width, height)

def average_dimensions_directory(directory_path):
    width_list = []
    height_list = []

    for file_name in os.listdir(directory_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(directory_path, file_name)
            width, height = average_dimensions(image_path)
            width_list.append(width)
            height_list.append(height)

    avg_width = sum(width_list) / len(width_list) if width_list else 0
    avg_height = sum(height_list) / len(height_list) if height_list else 0
    
    return avg_width, avg_height

if __name__ == '__main__':
    directory_path = './images'  # Replace with the path to your directory containing images
    avg_width, avg_height = average_dimensions_directory(directory_path)
    print(f'The average width for images is: {avg_width}')
    print(f'The average height for images is: {avg_height}')