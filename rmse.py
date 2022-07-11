import math
from math import sqrt
from sklearn.metrics import mean_squared_error

def count_rmse(orginal_image, generated_image):
    height = orginal_image.shape[0]
    width = orginal_image.shape[1]
    diagonal = math.sqrt(height ** 2 + width ** 2)
    padding_height = math.ceil(diagonal - height) + 2
    padding_width = math.ceil(diagonal - width) + 2

    generated_image = generated_image[math.ceil(padding_height/2):(math.ceil(padding_height/2)+height), 
                        math.ceil(padding_width/2):math.ceil(padding_width/2)+width]

    return math.sqrt(mean_squared_error(orginal_image, generated_image))