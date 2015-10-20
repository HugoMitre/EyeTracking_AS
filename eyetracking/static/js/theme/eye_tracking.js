var delete_record;
var ready_tables;
var ready_detail;

delete_record = function (token, url_redirect){
    $(".delete-link").on("click", function() {
        if(confirm('Are you sure you want to delete this item?')){
            var delete_url = $(this).attr('data-delete-url');
            $.ajax({
                url: delete_url,
                type: 'POST',
                data: { csrfmiddlewaretoken: token },
                success: function() {
                    window.location = url_redirect;
                },
                error: function() {
                    toastr.error('The request was unsuccessful', 'Error');
                }
            });
        }
        return false;
    });
};

ready_tables = function (token, url_redirect){
    $('.tooltip-btn').tooltip();
    delete_record(token, url_redirect);
};

ready_detail = function (token, url_redirect){
    delete_record(token, url_redirect);
};


