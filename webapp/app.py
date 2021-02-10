"""
Flask endpoint to render and generate mandelbrot set webapp
"""
import os
import os.path
from flask import Flask,render_template,jsonify,request,make_response

try:
    from mandelbrot_generate import generate
except ImportError:
    from .mandelbrot_generate import generate

import json 
import numpy as np
import time
import gzip

app = Flask(__name__,instance_relative_config=True)
app.config['JSON_SORT_KEYS'] = False

def compress_json(data):
    """
    Compresses large json data that in this case would be the Mandelbrot set matrix
    """
    json_data = json.dumps(data)
    encoded = json_data.encode('utf-8')
    compressed = gzip.compress(encoded)
    response = make_response(compressed)
    response.headers['Content-length'] = len(compressed)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/')
def main():
    """
    Renders index
    """
    return render_template('index.html')

@app.route('/data/')
def generate_set():
    """
    Endpoint to return mandelbrot set with given query params:

    min_x,max_x: Real axis coordinates
    min_y,max_y: Imaginary axis coordinates
    n: resolution of image
    iteration: Iteration limit for calculating the convergence of a point in the complex plain
    """

    try:
        query_params = {
            "min_x": request.args.get('minX'),
            "max_x": request.args.get('maxX'),
            "min_y": request.args.get('minY'),
            "max_y": request.args.get('maxY'),
            "resolution": request.args.get('resolution'),
            "iteration": request.args.get('iteration'),
        }

        for key in query_params:
            if len(query_params[key]) == 0 or query_params[key] == "NaN" or query_params[key] == "undefined":
                raise TypeError
            query_params[key] = float(query_params[key])

    except TypeError as err:
        error = {
            "error": "Query parameter unspecified".format(key),
            "Query parameters": query_params
        }

        return jsonify(error), 400

    except ValueError as err:
        error = {
            "error": "Query parameter '{}' must be a number".format(key),
            "Query parameters": query_params
        }
        return jsonify(error), 400
    
    mandelbrot_data = generate(query_params['min_x'],
                               query_params['max_x'], 
                               query_params['min_y'],
                               query_params['max_y'],
                               query_params['resolution'],
                               query_params['iteration']).T
    
    #normalize data between 0 and 255
    mandelbrot_data = mandelbrot_data*255/np.max(mandelbrot_data)

    #Parameters for drawing mandelbrot set on client side
    dim = np.shape(mandelbrot_data)
    response = {
        "set": mandelbrot_data.tolist(),
        "height": dim[0],
        "width": dim[1],
    }

    return compress_json(response), 200

if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
    
