# Use the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /

# Copy the project files to the working directory
COPY . .

# Install dependencies using requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade flask jinja2
# Install gfortran
RUN apt-get update \
    && apt-get install -y gfortran make \
    && rm -rf /var/lib/apt/lists/*

# Navigate to the mandelbrot directory
WORKDIR /webapp/mandelbrot

# Compile Fortran to Python executable using makefile
RUN make

# Navigate back to the main working directory
WORKDIR /

# Set environment variables
ENV FLASK_APP='./webapp/app.py'

# Expose the default Flask port
EXPOSE 5000

# Run Flask in production mode
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
