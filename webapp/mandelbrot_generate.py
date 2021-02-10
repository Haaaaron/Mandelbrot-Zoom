import numpy as np 

try:
    from . import mandelbrot  
except ImportError:
    import mandelbrot

def generate(min_x=-2,max_x=1,min_y=-1,max_y=1, resolution=400,iteration=50):
    """
    Calls fortran to generate mandelbrot set based on:

    coordinates: Re: [min_x,max_x]
                 Im: [min_y,max_y], 
    Resolution: determines the heigth and with for the canvas
    Iteration: limit for calculating the convergence of a point in the complex plain
    """

    abs_x = abs(max_x-min_x)
    abs_y = abs(max_y-min_y)
    ratio_x = abs_x/(abs_x+abs_y)
    ratio_y = abs_y/(abs_x+abs_y)
    i_n = int(ratio_x*resolution)
    j_n = int(ratio_y*resolution)
    data = mandelbrot.calculate_mandelbrot_set(min_x,max_y,i_n,j_n,abs_x,abs_y,iteration).astype('float64')

    return data

if __name__ == '__main__':
    """
    Used for generating snapshot
    """
    data = generate()
    np.savetxt('../tests/snapshots/example_data.txt',data)