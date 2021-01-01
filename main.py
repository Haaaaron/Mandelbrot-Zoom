from flask import Flask,render_template,jsonify
from mandelbrot_generate import generate
import json 
import numpy as np
import time

app = Flask(__name__)

@app.route('/')
def main():

    #return render_template('main.html',mandelbrot_data=mandelbrot_data)
    return render_template('main.html')

@app.route('/data/<coord>')
def generate_set(coord):
    
    min_x,max_x,min_y,max_y,n,iteration = np.array(coord.split("_")).astype(float)

    #generates mandelbrotset data
    mandelbrot_data = generate(min_x,max_x,min_y,max_y,n,iteration).T
    
    #normalize data between 0 and 255
    mandelbrot_data = mandelbrot_data*255/np.max(mandelbrot_data)

    #constants for drawing mandelbrot set
    dim = np.shape(mandelbrot_data)
    coord=[min_x,max_x,min_y,max_y]
    
    return jsonify(set=mandelbrot_data.tolist(),height=dim[0],width=dim[1],coord=coord)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
    
