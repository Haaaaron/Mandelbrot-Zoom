from flask import Flask,render_template,jsonify,request,make_response
from mandelbrot_generate import generate
import json 
import numpy as np
import time
import gzip

app = Flask(__name__)

@app.route('/')
def main():

    #return render_template('main.html',mandelbrot_data=mandelbrot_data)
    return render_template('main.html')

@app.route('/data/')
def generate_set():
    
    #get values to calculate mandelbrot set
    min_x = float(request.args.get('minX'))
    max_x = float(request.args.get('maxX'))
    min_y = float(request.args.get('minY'))
    max_y = float(request.args.get('maxY'))
    n = float(request.args.get('density'))
    iteration = float(request.args.get('iter'))
    
    
    #generates mandelbrotset data
    mandelbrot_data = generate(min_x,max_x,min_y,max_y,n,iteration).T
    
    #normalize data between 0 and 255
    mandelbrot_data = mandelbrot_data*255/np.max(mandelbrot_data)

    #constants for drawing mandelbrot set
    dim = np.shape(mandelbrot_data)
    coord=[min_x,max_x,min_y,max_y]

    print(mandelbrot_data)

    data = {
        "set": mandelbrot_data.tolist(),
        "height": dim[0],
        "width": dim[1],
        "coord": coord
    }

    json_data= json.dumps(data)
    encoded = json_data.encode('utf-8')
    compressed = gzip.compress(encoded)
    response = make_response(compressed)
    response.headers['Content-length'] = len(compressed)
    response.headers['Content-Encoding'] = 'gzip'

    return response
    #return jsonify(set=mandelbrot_data.tolist(),height=dim[0],width=dim[1],coord=coord)

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
    
