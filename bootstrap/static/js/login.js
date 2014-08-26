$('#login').click(function(e) {
    e.preventDefault();
    $.post(
        "/",
        {
            username: $("#id_username").val(),
            password: $("#id_password").val(),
            csrfmiddlewaretoken: $.cookie("csrftoken"),
            next: $("#id_next").val(),
        }
    )
    .done(function(){
        window.location = '/';
    })
    .fail(function(response) {
        $("input#id_username").removeClass("red-border");
        $("input#id_password").removeClass("red-border");
        var failure = null;
        if (response) {
            var json = JSON.parse(response.responseText);
            for (var field in json) {
                if (field == "username") {
                    $("input#id_username")
                        .attr("placeholder", json[field])
                        .addClass("red-border");
                }
                else if (field == "password") {
                    $("input#id_password")
                        .attr("placeholder", json[field])
                        .addClass("red-border");
                }
                else {
                    failure = "<p class=login_failed>" + json[field] + "</p>";
                }
            }
        }
        else {
            failure = "<p class=login_failed>Probably server connection problem!</p>";
        }

        if (failure) {
            $("div#login_failed").html(failure);
            $("div#login_failed").show();
        }
    });
});


$(".login_failed").click(function(e) {
    $(this).hide();
});
