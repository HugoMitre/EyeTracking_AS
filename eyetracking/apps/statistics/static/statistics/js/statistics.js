//Functions
var slider;
var createTable;
var createBarChart;
var createPieChart;
var changeFeature;
var startStatistics;

//AOI
var activeImage;
var urlGetDataShapes = 'feature';
var idTable = 'table-features';
var shapesNames;


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

createTable = function(headers, body){
    //Head
    strHead = '<thead> <tr>';

    for (var i=0; i < headers.length; i++){
        strHead+= '<th>' + headers[i] + '</th>';
    }

    strHead += '</thead> </tr>';

    //Body
    strBody = '<tbody>';

    for (b in body){
        strBody+= '<tr>';

        strBody += '<td>' + body[b]['name'] + '</td>';
        strBody += '<td>' + body[b]['visit_count'] + '</td>';

        strBody+= '<tr>';
    }

    strBody += '</body>';

    $('#'+idTable).empty().append(strHead).append(strBody);

};

createBarChart = function(columns){
    c3.generate({
        data: {
            x : 'x',
            columns: columns,
            type: 'bar',
            names: {
                time: 'Areas of Interest'
            }
        },
        axis: {
            x: {
                type: 'category' // this needed to load string x value
            }
        }
    });
};

createPieChart = function(){

};

changeFeature = function(){

};

changeImage = function(idImg){
    $.get(urlGetDataShapes, {'image_id':idImg}).success(function(data){
        activeImage = idImg;

        shapes = data['shapes'];
        shapesNames = ['x'];
        visitCount = ['time'];

        for(key in shapes){
            shapesNames.push(shapes[key]['name']);
            visitCount.push(shapes[key]['visit_count']);
        }

        columns = [shapesNames, visitCount];

        console.log(shapes);

        createBarChart(columns);
        createTable(['Name', 'Times'], shapes);

    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

startStatistics = function(){
    //Change Image
    $('.img-slider').on('click', function(){ changeImage($(this).attr('id')); });

};