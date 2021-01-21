import numpy as np 
import mandelbrot
import time


def generate(min_x=-2,max_x=1,min_y=-1,max_y=1, n=1500,iteration=255):

    abs_x = abs(max_x-min_x)
    abs_y = abs(max_y-min_y)
    norm_x = abs_x/(abs_x+abs_y)
    norm_y = abs_y/(abs_x+abs_y)
    i_n = int(norm_x*n)
    j_n = int(norm_y*n)
    data = mandelbrot.generate_heat_map(min_x,max_y,i_n,j_n,abs_x,abs_y,iteration).astype('float64')

    return data
