# Endpoins 

GET /data query params:

    - min_x: Lowe bound of real axis (float)
    - max_x: Upper bound of real axis float
    - min_y: Lowe bound of imaginary axis (float)
    - max_y: Upper bound of real axis (float)
    - resolution: Determines the heigth and with for the canvas (integer)
    - iteration : Iteration limit for convergence (integer)

### Example:

Get
   
    curl --compressed "http://127.0.0.1:5000/data/?minX=-2&maxX=1&minY=-1&maxY=1&resolution=1000&iter=100"

Response

    {
        "set": [
            [
            2.55,
            2.55,
            .
            .
            .
            5.1,
            5.1
            ]
        ],
        "height": 400,
        "width": 600
    }
 

### Example error:

Get

    curl --compressed "http://127.0.0.1:5000/data/?minX=-2&maxX=1&minY=-1&maxY=1&resolution=1000&iter="

Response

    {
        "error": "Query parameter unspecified", 
        "Query parameters": {
            "min_x": -2.0, 
            "max_x": 1.0, 
            "min_y": -1.0, 
            "max_y": 1.0, 
            "resolution": 1000, 
            "iteration": null
        }
    }
