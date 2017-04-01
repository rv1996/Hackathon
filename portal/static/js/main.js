/**
 * Created by rupanshu on 1/4/17.
 */

$(document).ready(function (event) {


    $('#recommend_button').click(function () {
        $.ajax({
            type: "GET",
            url: "recommendation/",
            success: function (data) {
                console.log("working");

                var names = '';
                console.log(data['recommend']);
                for (i = 0; i < data['recommend'].length; i++) {
                    names = names + data['recommend'][i] + ", ";

                }

                $('#recommend_response').html("<h3> you can take help of " + names + " department</h3>");

            }
        });
    });


    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


});