all: output compile

output:
	@echo "Compilation of mandelbrot.f90"

compile:
	f2py -c -m mandelbrot mandelbrot.f90 --f90flags="-fopenmp" -lgomp