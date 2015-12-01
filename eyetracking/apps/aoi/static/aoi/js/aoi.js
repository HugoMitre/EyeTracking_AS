//Functions
var getCookie;
var slider;
var changeImage;
var startCanvas;
var startEvents;
var drawShape;
var mouseOver, mouseOut, mouseDown, mouseMove, mouseUp;
var updateShape;
var getShapeInfo;
var deleteShape, keyDown;
var moveShapes;
var activateShapes;
var saveShape;
var setUrls;

//Canvas
var canvas;
var started = false;
var x = 0;
var y = 0;
var isMoving = false;

//Buttons
var btnEllipse = $('#btn-ellipse');
var btnRectangle = $('#btn-rectangle');
var btnDelete = $('#btn-delete');
var btnMove = $('#btn-move');

//Shapes
var fill = 'white';
var stroke = 'grey';
var strokeWidth = 1.5;
var opacity = 0.5;
var cornerColor = 'white';
var cornerSize = 10;
var hasRotatingPoint = false;
var hasBorders = false;
var urlCreate, urlUpdate;

//Shape name
var ungroup, items;
var name_left=0;
var name_top=0;


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

startCanvas = function (idDivCanvas, idCanvas, firstImage, urlCreate, urlUpdate){
    canvas = new fabric.Canvas(idCanvas);

    //Set background image with the first image
    if (firstImage)
        canvas.setBackgroundImage(firstImage, canvas.renderAll.bind(canvas));

    //Dimensions
    var widthCanvas = $(idDivCanvas).width();
    canvas.setDimensions({'width':widthCanvas, 'height':800});

    //Events
    startEvents();

    //Set urls for create and update shapes
    setUrls(urlCreate, urlUpdate);
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
    $('html').keydown(function(e){ keyDown(e);});

    //Move
    btnMove.on('click', function(){ moveShapes();});
};

drawShape = function (type){

    //Set crosshair cursor
    canvas.defaultCursor = 'crosshair';

    //Remove active move button
    if (isMoving){
        isMoving = false;

        //Hide tootip and set button active
        $(btnMove).tooltip('hide').removeClass('active');

        //Off update shape (mouseUpMoveShape)
        canvas.off('mouse:up');
    }

    if (type == 'ellipse'){
        //Hide tootip and set button active
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
        //Hide tootip and set button active
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

    //Set mouse coordinates
    shape.set({
        'left': x,
        'top': y});
    canvas.add(shape);
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

    //Remove old shape
    canvas.remove(shape);

    //Set new shape
    canvas.add(shape);
    canvas.setActiveObject(shape);

    //Get info and save
    dataShape = getShapeInfo(shape);
    saveShape(urlCreate, dataShape, true);

    /*
    var name = new fabric.IText('AOI name (Tap and Type)', {
        fontFamily: 'arial black',
        left: shape.left,
        top: shape.top + shape.height,
        fontSize: 20
    });

    group = new fabric.Group([ shape, name ], {
    });

    canvas.remove(shape);
    canvas.add(group);
    canvas.renderAll();

    group.on('mousedown', fabricDblClick(group, function (obj) {
            ungroup(group);
            canvas.setActiveObject(items[1]);
            items[1].enterEditing();
            items[1].selectAll();
            }));
    */

    //Off events
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

    //After draw allow move the shapes
    moveShapes();

    //Save changes of shapes
    canvas.on('mouse:up', function(e){ updateShape(e); });
};

updateShape = function(e){
    if (typeof e.target !== "undefined"){
        var token = getCookie('csrftoken');
        var dataShape = {
            csrfmiddlewaretoken:token,
            image: 1,
            name:'test',
            top: e.target.get('top').toFixed(2),
            left: e.target.get('left').toFixed(2),
            width:e.target.getWidth().toFixed(2),
            height:e.target.getHeight().toFixed(2),
            type: e.target.get('type')
        };

        saveShape(e.target.get('id')+ urlUpdate, dataShape, false);
    }
};

getShapeInfo = function(shape){
    var token = getCookie('csrftoken');
    var data = shape.toJSON();

    return dataShape = {
        csrfmiddlewaretoken:token,
        image: 1,
        name:'test',
        top:data.top,
        left: data.left,
        width:data.width,
        height:data.height,
        type:data.type
    };
};

deleteShape = function(){
    $(btnDelete).tooltip('hide');
    var activeShape = canvas.getActiveObject();

    if (typeof activeShape !== 'undefined' && activeShape != null){
         if (confirm('Are you sure you want to delete the aoi selected?')){
            activeShape.remove();
            $(btnDelete).removeClass('active');
        }
    }
};

keyDown = function (e){
    if(e.keyCode == 8)
    {
        e.preventDefault();
        deleteShape();
    }
};

moveShapes = function (){
    $(btnMove).tooltip('hide');
    if (isMoving){
        isMoving = false;
        $(btnMove).removeClass('active');
        canvas.discardActiveObject();
        activateShapes(false);
    }
    else{
        isMoving = true;
        $(btnMove).addClass('active');
        activateShapes(true);
    }
};

activateShapes = function(valueSelectable){
    canvas.getObjects().map(function(shape) {
        console.log(shape);
        return shape.set('selectable', valueSelectable);
    });
};

saveShape = function(url, data, isNew){
    $.post(url, data).done(function(e) {
        var shape = canvas.getActiveObject();
        if (isNew) {
            shape.set('id', e.pk);
        }
    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

setUrls = function(urlNew, urlModify){
    urlCreate = urlNew;
    urlUpdate = urlModify;
};

//// Double-click event handler
//    var fabricDblClick = function (obj, handler) {
//        return function () {
//            if (obj.clicked) {
//                handler(obj);
//            }
//            else {
//                obj.clicked = true;
//                setTimeout(function () {
//                    obj.clicked = false;
//                }, 500);
//            }
//        };
//    };
//
//// ungroup objects in group
//    ungroup = function (group) {
//        items = group._objects;
//        group._restoreObjectsState();
//        canvas.remove(group);
//        for (var i = 0; i < items.length; i++) {
//            canvas.add(items[i]);
//        }
//        // if you have disabled render on addition
//        canvas.renderAll();
//    };
//
//
//// Re-group when text editing finishes
//    var name = new fabric.IText('AOI name (Tap and Type)', {
//        fontFamily: 'arial black',
//        left: name_left,
//        top: name_top,
//        fontSize: 20
//    });
//
//    name.on('editing:exited', function () {
//        console.log('editing finished')
//        //var items = [];
//        //canvas2.forEachObject(function (obj) {
//        //    items.push(obj);
//        //    canvas2.remove(obj);
//        //});
//        //var grp = new fabric.Group(items.reverse(), {});
//        //canvas2.add(grp);
//        //grp.on('mousedown', fabricDblClick(grp, function (obj) {
//        //    ungroup(grp);
//        //    canvas2.setActiveObject(name);
//        //    name.enterEditing();
//        //    name.selectAll();
//        //}));
//    });

