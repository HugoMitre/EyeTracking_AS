//Functions
var getCookie;
var slider;
var changeImage;
var startCanvas;
var startEvents;
var drawShape;
var mouseDown, mouseMove, mouseUp, mouseOver, mouseOut;
var deleteShape, keydown;

//Canvas
var canvas;
var started = false;
var x = 0;
var y = 0;

//Buttons
var btnEllipse = $('#btn-ellipse');
var btnRectangle = $('#btn-rectangle');
var btnDelete = $('#btn-delete');
var btnSelect = $('#btn-select');

//Shapes
var fill = 'white';
var stroke = 'grey';
var strokeWidth = 1.5;
var opacity = 0.5;
var cornerColor = 'white';
var cornerSize = 10;
var hasRotatingPoint = false;
var hasBorders = false;


getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

slider = function(idSlider){
    $(idSlider).slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 4,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
};

changeImage = function(idImg, urlImage){
    $(idImg).on('click', function(){
        var id = $(this).attr('id');
        var token = getCookie('csrftoken');
        $.get(urlImage, {'id':id, 'csrfmiddlewaretoken':token}).done(function( data ) {
            canvas.setBackgroundImage(data.urlPhoto, canvas.renderAll.bind(canvas));
        }).fail(function() {
            toastr.error('The request was unsuccessful', 'Error');
        });
    });
};

startCanvas = function (idDivCanvas, idCanvas, firstImage){
    canvas = new fabric.Canvas(idCanvas);

    //Set background image with the first image
    if (firstImage)
        canvas.setBackgroundImage(firstImage, canvas.renderAll.bind(canvas));

    //Dimensions
    var widthCanvas = $(idDivCanvas).width();
    canvas.setDimensions({'width':widthCanvas, 'height':800});

    //Events
    startEvents();
};

startEvents = function(){
    //Hover
    canvas.on('mouse:over', function (e){ mouseOver(e);});
    canvas.on('mouse:out', function (e){ mouseOut(e);});

    //Draw
    btnEllipse.on('click', function(){ drawShape('ellipse');});
    btnRectangle.on('click', function(){ drawShape('rectangle');});

    //Delete
    btnDelete.on('click', function(){ deleteShape();});
    $('html').keydown(function(e){ keydown(e);});
};

drawShape = function (type){

    canvas.defaultCursor = 'crosshair';

    if (type == 'ellipse'){
        $(btnEllipse).tooltip('hide').addClass('active');

        var shapeEllipse = new fabric.Ellipse({
            rx: 0,
            ry: 0,
            left: x,
            top: y,
            fill : fill,
            stroke: stroke,
            strokeWidth: strokeWidth,
            opacity: opacity,
            cornerColor: cornerColor,
            cornerSize: cornerSize,
            hasRotatingPoint: hasRotatingPoint,
            hasBorders: hasBorders
        });

        canvas.on('mouse:down', function (e){ mouseDown(e, shapeEllipse)});
        canvas.on('mouse:move', function (e){ mouseMove(e, 'ellipse')});
        canvas.on('mouse:up', function (e){ mouseUp(e, 'ellipse')});
    }
    else if (type == 'rectangle'){
        $(btnRectangle).tooltip('hide').addClass('active');

        var shapeRectangle = new fabric.Rect({
            width: 0,
            height: 0,
            left: x,
            top: y,
            fill : fill,
            stroke: stroke,
            strokeWidth: strokeWidth,
            opacity: opacity,
            cornerColor: cornerColor,
            cornerSize: cornerSize,
            hasRotatingPoint: hasRotatingPoint,
            hasBorders: hasBorders
        });

        canvas.on('mouse:down', function (e){ mouseDown(e, shapeRectangle)});
        canvas.on('mouse:move', function (e){ mouseMove(e, 'rectangle')});
        canvas.on('mouse:up', function (e){ mouseUp(e, 'rectangle')});
    }
};

mouseOver = function (e){
    e.target.setFill('dark');
    canvas.renderAll();
};

mouseOut = function (e){
    e.target.setFill('white');
    canvas.renderAll();
};

mouseDown = function (e, shape) {
    var mouse = canvas.getPointer(e.e);
    started = true;
    x = mouse.x;
    y = mouse.y;

    shape.set('left', x).set('top', y);
    canvas.renderAll();
    canvas.setActiveObject(shape);

};

mouseMove = function (e, type) {
    if(!started) {
        return false;
    }

    var mouse = canvas.getPointer(e.e);
    var shape = canvas.getActiveObject();
    var w, h;

    if (type == 'ellipse'){
        w = Math.abs(mouse.x - x)/2;
        h = Math.abs(mouse.y - y)/2;

        if (!w || !h) {
            return false;
        }

        shape.set('rx', w).set('ry', h);
    }
    else if (type == 'rectangle'){
        w = Math.abs(mouse.x - x);
        h = Math.abs(mouse.y - y);

        if (!w || !h) {
            return false;
        }
        shape.set('width', w).set('height', h);
    }

    canvas.renderAll();
};

mouseUp = function (e, type) {
    if(started) {
        started = false;
    }

    var shape = canvas.getActiveObject();
    canvas.add(shape);
    canvas.renderAll();

    canvas.off('mouse:down');
    canvas.off('mouse:move');
    canvas.off('mouse:up');

    canvas.defaultCursor = 'default';

    if (type == 'ellipse'){
        btnEllipse.removeClass('active');
    }
    else if (type == 'rectangle'){
        btnRectangle.removeClass('active');
    }
};

deleteShape = function(){
    $(btnDelete).tooltip('hide');
    activeShape = canvas.getActiveObject();

    if (typeof activeShape !== 'undefined' && activeShape != null){
         if (confirm('Are you sure you want to delete the aoi selected?')){
            activeShape.remove();
            $(btnDelete).removeClass('active');
        }
    }
};

keydown = function (e){
    if(e.keyCode == 8)
    {
        e.preventDefault();
        deleteShape();
    }
};