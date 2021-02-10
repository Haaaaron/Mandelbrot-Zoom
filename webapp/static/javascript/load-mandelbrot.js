let mandelbrotInitial;
let mandelbrot;
let mandelbrotPrevious;
let jsonCall = false;
let loading = document.getElementById("load");
let box = null;
let cCanvas = document.getElementById("canvasControls");

class MandelbrotConditions {
  constructor() {
    this.coord = {
      minX: -2,
      maxX: 1,
      minY: -1,
      maxY: 1,
    };
    this.resolution = 1000;
    this.iteration = 100;
  }
  url() {
    return `/data?minX=${this.coord.minX}&maxX=${this.coord.maxX}&minY=${this.coord.minY}&maxY=${this.coord.maxY}&resolution=${this.resolution}&iteration=${this.iteration}`;
  }
  reset() {
    this.coord = {
      minX: -2,
      maxX: 1,
      minY: -1,
      maxY: 1,
    };
    this.resolution = 1500;
    this.iteration = 100;
  }
}

let mandelbrotConst = new MandelbrotConditions();

function preload() {
  loading.style.display = "block";
  mandelbrotInitial = loadJSON(mandelbrotConst.url());
  mandelbrot = mandelbrotInitial;
}

function setup() {
  let myCanvas = createCanvas(mandelbrot.width, mandelbrot.height);
  myCanvas.parent("mandelbrotSet");
  drawMandelbrot(mandelbrot);
}

function reloadMandelbrot() {
  mandelbrotPrevious = mandelbrot;
  loading.style.display = "block";
  mandelbrot = loadJSON(mandelbrotConst.url(), drawMandelbrot);
}

function drawMandelbrot(data) {
  resizeCanvas(data.width, data.height);
  pixelDensity(1);
  loadPixels();

  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let p = (x + y * width) * 4;
      pixels[p] = data.set[y][x];
      pixels[p + 1] = data.set[y][x];
      pixels[p + 2] = data.set[y][x];
      pixels[p + 3] = 255;
    }
  }

  updatePixels();
  loading.style.display = "none";
  cCanvas.width = document.getElementById("mandelbrotSet").clientWidth;
  cCanvas.height = document.getElementById("mandelbrotSet").clientHeight;
}

function saveSVG() {
  save("mySVG.svg");
}

$(window).ready(function () {
  let ccanvas = $("#canvasControls");
  let c = ccanvas[0].getContext("2d");

  ccanvas.mousedown(function (e) {
    if (
      box == null &&
      e.pageX <= mandelbrot.width &&
      e.pageY <= mandelbrot.height
    )
      box = [e.pageX, e.pageY, 0, 0];
  });

  ccanvas.mousemove(function (e) {
    if (box != null) {
      c.lineWidth = 1;
      // clear out old box first
      c.clearRect(0, 0, ccanvas[0].width, ccanvas[0].height);

      if (e.pageX >= mandelbrot.width || e.pageY >= mandelbrot.height) {
        box = null;
      }
      // draw new box
      c.strokeStyle = "#ED6410";
      box[2] = e.pageX;
      box[3] = e.pageY;
      c.strokeRect(box[0], box[1], box[2] - box[0], box[3] - box[1]);
    }
  });

  ccanvas.mouseup(function () {
    if (box != null) {
      //coord:[min_x,max_x,min_y,max_y]
      let width = mandelbrot.width;
      let height = mandelbrot.height;
      let lenx = abs(mandelbrotConst.coord.maxX - mandelbrotConst.coord.minX);
      let leny = abs(mandelbrotConst.coord.maxY - mandelbrotConst.coord.minY);
      let ReCoord = null;
      let ImCoord = null;

      // clear box
      c.clearRect(0, 0, ccanvas[0].width, ccanvas[0].height);

      //convert pixels to complex coordinates
      ReCoord = [
        (box[0] / width) * lenx + mandelbrotConst.coord.minX,
        (box[2] / width) * lenx + mandelbrotConst.coord.minX,
      ].sort(function (a, b) {
        return a - b;
      });
      ImCoord = [
        (-box[1] / height) * leny + mandelbrotConst.coord.maxY,
        (-box[3] / height) * leny + mandelbrotConst.coord.maxY,
      ].sort(function (a, b) {
        return a - b;
      });
      box = null;
      mandelbrotConst.coord = {
        minX: ReCoord[0],
        maxX: ReCoord[1],
        minY: ImCoord[0],
        maxY: ImCoord[1],
      };

      reloadMandelbrot();
    }
  });

  $("#reset").click(function () {
    mandelbrot = mandelbrotInitial;
    mandelbrotConst.reset();
    drawMandelbrot(mandelbrot);
  });

  $("#undo").click(function () {
    mandelbrot = mandelbrotPrevious;
    drawMandelbrot(mandelbrot);
  });

  $("#recalculate").click(function () {
    var constants = $("#constants").serializeArray();
    let iteration = parseInt(constants[0].value);
    let resolution = parseInt(constants[1].value);

    if (iteration && resolution) {
      mandelbrotConst.iteration = iteration;
      mandelbrotConst.resolution = resolution;
      reloadMandelbrot();
    }
  });

  $("#save").click(function () {
    saveSVG();
  });
});

$(window).resize(function () {
  let setWidth = document.getElementById("mandelbrotSet").clientWidth;
  let setHeight = document.getElementById("mandelbrotSet").clientHeight;
  cCanvas.width = setWidth;
  cCanvas.height = setHeight;
});
