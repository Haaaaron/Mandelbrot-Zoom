let mandelbrotInitial;
let mandelbrot;
let mandelbrotPrevious;
let jsonCall = false;
let loading = document.getElementById("load");

let box = null;

class MandelbrotConditions {
  constructor() {
    this.coord = {
      minX: -2,
      maxX: 1,
      minY: -1,
      maxY: 1,
    };
    this.density = 1000;
    this.iteration = 100;
  }
  url() {
    return `/data?minX=${this.coord.minX}&maxX=${this.coord.maxX}&minY=${this.coord.minY}&maxY=${this.coord.maxY}&density=${this.density}&iter=${this.iteration}`;
  }
  reset() {
    this.coord = {
      minX: -2,
      maxX: 1,
      minY: -1,
      maxY: 1,
    };
    this.density = 1500;
    this.iteration = 100;
  }
}

let mandelbrotConst = new MandelbrotConditions();

let ccanvas = document.getElementById("canvasControls");
ccanvas.width = window.innerWidth;
ccanvas.height = window.innerHeight;

function preload() {
  // mandelbrotInitial = loadJSON(mandelbrotConst.url());
  // mandelbrot = mandelbrotInitial;
  loading.style.display = "block";
  mandelbrotInitial = loadJSON(mandelbrotConst.url());
  mandelbrot = mandelbrotInitial;
}

function setup() {
  let myCanvas = createCanvas(mandelbrot.width, mandelbrot.height);
  myCanvas.parent("mandelbrotSet");
  let ccanvas = document.getElementById("canvasControls");
  const setWidth = document.getElementById("mandelbrotSet").clientWidth;
  const setHeight = document.getElementById("mandelbrotSet").clientHeight;
  ccanvas.width = setWidth;
  ccanvas.height = setHeight;
  drawMandelbrot(mandelbrot);
}

function reloadMandelbrot() {
  mandelbrotPrevious = mandelbrot;
  loading.style.display = "block";
  mandelbrot = loadJSON(mandelbrotConst.url(), drawMandelbrot, error());
}

function error() {
  console.log("fuc");
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
}

function saveSVG() {
  save("mySVG.svg");
}

$(window).ready(function () {
  let ccanvas = $("#canvasControls");
  let c = ccanvas[0].getContext("2d");

  ccanvas.mousedown(function (e) {
    console.log(e.pageX, e.pageY, mandelbrot.width, mandelbrot.height);
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
      //coord=[min_x,max_x,min_y,max_y]
      let coord = mandelbrot.coord;
      let width = mandelbrot.width;
      let lenx = abs(coord[1] - coord[0]);
      let leny = abs(coord[3] - coord[2]);
      let height = mandelbrot.height;
      let ReCoord = null;
      let ImCoord = null;

      // clear box
      c.clearRect(0, 0, ccanvas[0].width, ccanvas[0].height);

      //convert pixels to complex coordinates
      ReCoord = [
        (box[0] / width) * lenx + coord[0],
        (box[2] / width) * lenx + coord[0],
      ].sort(function (a, b) {
        return a - b;
      });
      ImCoord = [
        (-box[1] / height) * leny + coord[3],
        (-box[3] / height) * leny + coord[3],
      ].sort(function (a, b) {
        return a - b;
      });
      box = null;
      console.log(mandelbrotConst.coord, ReCoord.concat(ImCoord));
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
    mandelbrotConst.iteration = constants[0].value;
    mandelbrotConst.density = constants[1].value;
    reloadMandelbrot();
  });
  $("#save").click(function () {
    saveSVG();
  });
});

$(window).resize(function () {
  let ccanvas = document.getElementById("canvasControls");
  const setWidth = document.getElementById("mandelbrotSet").clientWidth;
  const setHeight = document.getElementById("mandelbrotSet").clientHeight;
  ccanvas.width = setWidth;
  ccanvas.height = setHeight;
});
