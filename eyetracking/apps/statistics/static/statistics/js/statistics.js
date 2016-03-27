//Functions
var slider;
var startStatistics;
var changeImage;

//AOI
var activeImage;
var urlGetDataShapes = 'image';
var divImage = '.photo';
var imgSlider = '.img-slider';

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

changeImage = function(element){
    $.get(urlGetDataShapes, {'image_id':element.attr('id')}).success(function(data){
        activeImage = element.attr('id');

        //Set background for selected image
        $(divImage).css('background-color', '');
        element.parent().css('background-color', '#CCC');

        console.log(data);
        $('#td_baseline').html(data['features']['baseline']);
        $('#td_apcps').html(data['features']['apcps']);
        $('#td_mpd').html(data['features']['mpd']);
        $('#td_mpdc').html(data['features']['mpdc']);



    }).fail(function() {
        toastr.error('The request was unsuccessful', 'Error');
    });
};

startStatistics = function(){
    //Change Image
    $(imgSlider).on('click', function(){ changeImage($(this)); });


};