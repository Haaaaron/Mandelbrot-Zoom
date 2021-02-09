# Mandelbrot set zoom

https://mandelbrotzoom.pythonanywhere.com/

Tool to explore the mandelbrot set. Calculated with fortran and displayed with javascript. Framework is made with python.

# Getting started
All commands will be excecuted in the ./backend directory of the project
  
## Setting up environment with python virtualenv:

Create python3 environment:

    python3 -m venv env

Activate environment:

    source env/bin/activate

Install dependencies using requirements.txt:

    pip install -r requirements.txt

## Creating Fortran to python excecutable:

Note that you will need a fortran compiler to create the excecutable.
(Tested with gfortran https://gcc.gnu.org/wiki/GFortran)

Run makefile:
  
  `make`
  
Or the command directly:

  `f2py -c -m mandelbrot mandelbrot.f90 --f90flags="-fopenmp" -lgomp`
    
## Running Flask in production mode: 

Export app and run:

    export FLASK_APP='index.py'
    flask run

Open the given url in your browser (default):

    http://127.0.0.1:5000/
    
Zoom away!

## Environment variables:

Environment variables can be set with flask run:

    flask run --host=0.0.0.0 --port=80

