//Functions
var getCookie;
var slider;
var changeImage;
var startCanvas;
var startEvents;
var drawShape;
var mouseOver, mouseOut, mouseDown, mouseMove, mouseUp;
var finishDraw;
var getShapeInfo;
var deleteShape, keyDown;
var moveShapes;
var activateShapes;
var saveShape;
var loadShapes;
var createRect;
var createEllipse;
var createIText;
var setMinSize;
var fabricDblClick;
var ungroup;
var changeName;
var createGroup;

//Canvas
var canvas;
var x = 0;
var y = 0;
var isMoving = false;
var isDrawing = false;
var urlCreate = 'new/';
var urlUpdate = '/update/';
var urlDelete = '/delete/';
var urlLoadShapes = 'shapes/';
var urlChangeName = '/change_name/';
var urlImageInfo = 'image/';
var activeImage;
var minWidth = 30;
var minHeight = 30;
var defaultName = 'AOI';

//Buttons
var btnEllipse = $('#btn-ellipse');
var btnRectangle = $('#btn-rectangle');
var btnDelete = $('#btn-delete');
var btnMove = $('#btn-move');

//Shape properties
var fill = 'white';
var stroke = 'black';
var strokeWidth = 1;
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

changeImage = function(idImg){
    $.get(urlImageInfo, {'image_id':idImg}).success(function(data){
        activeImage = data.id;
        canvas.clear();

        fabric.Image.fromURL(data.image, function(img) {
            canvas.setDimensions({'width':data.width, 'height':data.height});
            canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
        }, {'width':data.width, height:data.height});

        loadShapes(activeImage);
    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

startCanvas = function (idDivCanvas, idCanvas, idFirstImage){
    canvas = new fabric.Canvas(idCanvas);
    canvas.selection = false;

    //Set background image with the first image
    if (idFirstImage) {
        changeImage(idFirstImage);
    }

    //Events
    startEvents(idDivCanvas);
};

startEvents = function(idDivCanvas){
    //Change Image
    $('.img-slider').on('click', function(){ changeImage($(this).attr('id')) });

    //Hover
    canvas.on('mouse:over', function (e){ mouseOver(e) });
    canvas.on('mouse:out', function (e){ mouseOut(e) });

    //Draw
    btnEllipse.on('click', function(){ drawShape('ellipse') });
    btnRectangle.on('click', function(){ drawShape('rectangle') });

    //Delete
    btnDelete.on('click', function(){ deleteShape() });
    $('html').keydown(function(e){ keyDown(e) });

    //Move
    btnMove.on('click', function(){ moveShapes() });

    //Scroll
    $(idDivCanvas).onscroll = function(){ c2.calcOffset() };
};

drawShape = function (type){

    //Set crosshair cursor
    canvas.defaultCursor = 'crosshair';

    //If is selected the button to move
    if (isMoving){
        isMoving = false;

        //Hide tootip and set button active
        $(btnMove).tooltip('hide').removeClass('active');

        //Off update shape
        canvas.off('mouse:up');
    }

    //If is selected the button to draw
    if (isDrawing){
        $(btnRectangle).removeClass('active');
        $(btnEllipse).removeClass('active');

        canvas.off('mouse:down');
        canvas.off('mouse:move');
        canvas.off('mouse:up');
    }

    //Draw shape
    if (type == 'ellipse'){
        //Hide tootip and set button active
        $(btnEllipse).tooltip('hide').addClass('active');

        var shapeEllipse = new createEllipse({'width':0, 'height':0, 'left':x, 'top':y});

        canvas.on('mouse:down', function (e){ mouseDown(e, shapeEllipse)});
        canvas.on('mouse:move', function (e){ mouseMove(e, 'ellipse')});
        canvas.on('mouse:up', function (e){ mouseUp(e, 'ellipse')});
    }
    else if (type == 'rectangle'){
        //Hide tootip and set button active
        $(btnRectangle).tooltip('hide').addClass('active');

        var shapeRectangle = createRect({'width':0, 'height':0, 'left':x, 'top':y});

        canvas.on('mouse:down', function (e){ mouseDown(e, shapeRectangle)});
        canvas.on('mouse:move', function (e){ mouseMove(e, 'rectangle')});
        canvas.on('mouse:up', function (e){ mouseUp(e, 'rectangle')});
    }
};

mouseOver = function (e){
    e.target.item(0).setFill('dark');
    e.target.item(1).setColor('white');
    canvas.renderAll();
};

mouseOut = function (e){
    e.target.item(0).setFill('white');
    e.target.item(1).setColor('dark');
    canvas.renderAll();
};

mouseDown = function (e, shape) {
    var mouse = canvas.getPointer(e.e);
    isDrawing = true;
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
    if(!isDrawing) {
        return false;
    }

    var mouse = canvas.getPointer(e.e);
    var shape = canvas.getActiveObject();
    var width, height;

    if (type == 'ellipse'){
        width = Math.abs(mouse.x - x)/2;
        height = Math.abs(mouse.y - y)/2;

        if (!width || !height) {
            return false;
        }

        shape.set('rx', width).set('ry', height);
    }
    else if (type == 'rectangle'){
        width = Math.abs(mouse.x - x);
        height = Math.abs(mouse.y - y);

        if (!width || !height) {
            return false;
        }
        shape.set('width', width).set('height', height);
    }

    canvas.renderAll();
};

mouseUp = function (e, type) {
    var shape = canvas.getActiveObject();

    //Remove shape
    canvas.remove(shape);

    //If size is very small set minimum width and height
    setMinSize(shape);

    //Create label
    var text = createIText(defaultName, {
        'fontSize': 20,
        'left': shape.left + (shape.width/2),
        'top': shape.top + (shape.height/2),
        'originX': 'center',
        'originY': 'center'});

    //Create new group
    var group = createGroup([shape, text]);
    canvas.add(group);
    canvas.setActiveObject(group);

    //Get info and save
    dataShape = getShapeInfo();
    saveShape(urlCreate, dataShape, true);

    //Actions when finish to draw
    finishDraw(type);

    //After draw allow move the shapes
    moveShapes();
};

finishDraw = function(type){
    //Off events
    canvas.off('mouse:down');
    canvas.off('mouse:move');
    canvas.off('mouse:up');

    //Set default cursor
    canvas.defaultCursor = 'default';

    //Remove active button
    if (type == 'ellipse'){
        btnEllipse.removeClass('active');
    }
    else if (type == 'rectangle'){
        btnRectangle.removeClass('active');
    }

    if(isDrawing) {
        isDrawing = false;
    }
};

getShapeInfo = function(){
    var group = canvas.getActiveObject();
    var shape = group.item(0);
    var token = getCookie('csrftoken');
    var type = shape.get('type');
    var name = group.item(0).get('name');

    //Get width and height
    var width, height;
    if (type == 'rect'){
        width = group.getWidth().toFixed(2);
        height = group.getHeight().toFixed(2);
    }else if (type == 'ellipse'){
        width = (group.getWidth().toFixed(2))/2;
        height = (group.getHeight().toFixed(2))/2;
    }

    //Get top and left
    var top, left;
    top = group.get('top').toFixed(2);
    left = group.get('left').toFixed(2);

    var dataShape = {
        csrfmiddlewaretoken: token,
        image: activeImage,
        name: name,
        top: top,
        left: left,
        width: width,
        height: height,
        type: type
    };

    //If has id add to dataShape
    var id = shape.get('id');
    if (id !== 'undefined')
        dataShape['id'] = id;

    return dataShape;
};

deleteShape = function(){
    $(btnDelete).tooltip('hide');
    var group = canvas.getActiveObject();
    var shape = group.item(0);
    var shapeName = group.item(1).getText();

    if (typeof group !== 'undefined' && group != null){
         if (confirm('Are you sure you want to delete "'+ shapeName +'"?')){
             var token = getCookie('csrftoken');
             var id = shape.get('id');
             $.post(id + urlDelete, {csrfmiddlewaretoken: token}).success(function(e) {
                 canvas.remove(group);
             }).fail(function() {
                toastr.error('The request was unsuccessful', 'Error');
             });
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

    canvas.on('object:modified', function(){
        dataShape = getShapeInfo();
        saveShape(dataShape.id + urlUpdate, dataShape, true);
    });


    var shape = canvas.getActiveObject();
    if (shape)
        changeName();

    canvas.on('object:selected', function () {
        changeName();
    });


};

changeName = function(){
    var shape = canvas.getActiveObject();
    var type = shape.get('type');

    if (type == 'group') {

        shape.off('mousedown');
        shape.item(1).off('editing:exited');

        shape.on('mousedown', fabricDblClick(shape, function (obj) {
            ungroup(shape);
            canvas.setActiveObject(shape.item(1));
            shape.item(1).enterEditing();
            shape.item(1).selectAll();
        }));

        shape.item(1).on('editing:exited', function () {
            console.log('salio');
            name = shape.item(1).getText();
            a = canvas.getItemById(shape.item(1).get('id'));
            b = canvas.getItemById(shape.item(0).get('id'));

            canvas.remove(a);
            canvas.remove(b);

            var group = new fabric.Group([b, a]);
            canvas.add(group);

            var token = getCookie('csrftoken');
            saveShape(shape.item(0).get('id') + urlChangeName, {'name':name, 'csrfmiddlewaretoken': token}, false);

            shape.on('mousedown', fabricDblClick(shape, function (obj) {
                ungroup(shape);
                canvas.setActiveObject(shape.item(1));
                shape.item(1).enterEditing();
                shape.item(1).selectAll();
            }));
        });
    }
};

activateShapes = function(valueSelectable){
    canvas.getObjects().map(function(shape) {
        return shape.set('selectable', valueSelectable);
    });
};

saveShape = function(url, data, isNew){
    $.post(url, data).success(function(e) {
        if (isNew) {
            var shape = canvas.getActiveObject();
            shape.item(0).set('id', e.pk);
            shape.item(1).set('id', 'l' + e.pk);
        }
    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

loadShapes = function(idImage){
    $.getJSON(urlLoadShapes, {image_id:idImage})
    .done(function(e) {
        $.each(e, function( index, value ) {
            var type = value.fields.type;
            var id = value.pk;
            var name = value.fields.name;
            var width = parseFloat(value.fields.width);
            var height = parseFloat(value.fields.height);
            var top = parseFloat(value.fields.top);
            var left = parseFloat(value.fields.left);
            var data = {'id':id, 'name':name, 'width':width, 'height':height, 'top':top, 'left':left};
            var shape;

            if (type == 'rect'){
                shape = createRect(data);
                left += width/2;
                top += height/2;
            }
            else if (type == 'ellipse') {
                shape = createEllipse(data);
                left += width;
                top += height;
            }

            var text = createIText(name, {
                'id':'l' + id,
                'fontSize': 20,
                'left': left,
                'top': top,
                'originX': 'center',
                'originY': 'center'});

            var group = createGroup([shape, text]);

            canvas.add(group);
        });
        canvas.renderAll();
    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

createRect = function(data){
    var selectable = false;
    var name = defaultName;

    if (isMoving) {
        selectable = true;
    }

    if (data.name) {
        name = data.name;
    }

    return new fabric.Rect({
        id: data.id,
        name: name,
        width: parseFloat(data.width),
        height: parseFloat(data.height),
        left: parseFloat(data.left),
        top: parseFloat(data.top),
        fill : fill,
        stroke: stroke,
        strokeWidth: strokeWidth,
        opacity: opacity,
        cornerColor: cornerColor,
        cornerSize: cornerSize,
        hasRotatingPoint: hasRotatingPoint,
        hasBorders: hasBorders,
        selectable: selectable,
        minScaleLimit: minWidth/parseFloat(data.width)
    });
};

createEllipse = function(data){
    var selectable = false;
    var name = defaultName;

    if (isMoving) {
        selectable = true;
    }

    if (data.name) {
        name = data.name;
    }

    var ellipse =  new fabric.Ellipse({
        id: data.id,
        name: name,
        rx: parseFloat(data.width),
        ry: parseFloat(data.height),
        left: parseFloat(data.left),
        top: parseFloat(data.top),
        fill : fill,
        stroke: stroke,
        strokeWidth: strokeWidth,
        opacity: opacity,
        cornerColor: cornerColor,
        cornerSize: cornerSize,
        hasRotatingPoint: hasRotatingPoint,
        hasBorders: hasBorders,
        selectable: selectable
    });

    //Only you can set min scale limit after the instance
    ellipse.set('minScaleLimit', (minWidth/2)/parseFloat(data.width));

    return ellipse;
};

createIText = function(name, data){
    return new fabric.IText(name, {
        id: data.id,
        fontSize: data.fontSize,
        left: parseFloat(data.left),
        top: parseFloat(data.top),
        originX: data.originX,
        originY: data.originY
    });
};

createGroup = function(shapes){
    var selectable = false;

    if (isMoving) {
        selectable = true;
    }

    return new fabric.Group(shapes, {'selectable':selectable});
};

setMinSize = function(shape){
    var type = shape.get('type');
    var width, height;
    var isLower = false;

    if (type == 'rect') {
        width = shape.getWidth();
        height = shape.getHeight();
        if (width < minWidth) {
            shape.set('width', minWidth);
            isLower = true;
        }
        if (height < minHeight) {
            shape.set('height', minHeight);
            isLower = true;
        }
    } else if (type == 'ellipse') {
        width = shape.getRx();
        height = shape.getRy();
        var minWidthEllipse = minWidth / 2;
        var minHeightEllipse = minHeight / 2;
        if (width < minWidthEllipse) {
            shape.set('rx', minWidthEllipse);
            isLower = true;
        }
        if (height < minHeightEllipse) {
            shape.set('ry', minHeightEllipse);
            isLower = true;
        }
    }

    if (isLower) {
        shape.set('minScaleLimit', 1);
    } else {
        if (type == 'rect')
            shape.set('minScaleLimit', minWidth / width);
        else {
            shape.set('minScaleLimit', (minWidth / 2) / width);
        }
    }
};

fabricDblClick = function (obj, handler) {
    return function () {
        if (obj.clicked) {
            handler(obj);
        }
        else {
            obj.clicked = true;
            setTimeout(function () {
                obj.clicked = false;
            }, 500);
        }
    };
};

ungroup = function (group) {
    var items;
    items = group._objects;
    group._restoreObjectsState();
    canvas.remove(group);
    for (var i = 0; i < items.length; i++) {
        canvas.add(items[i]);
    }
};

fabric.Canvas.prototype.getItemById = function(id) {
    var object = null,
        objects = this.getObjects();

    for (var i = 0, len = this.size(); i < len; i++) {
        if (objects[i].id && objects[i].id === id) {
            object = objects[i];
            break;
        }
    }

    return object;
};