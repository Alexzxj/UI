$(document).ready(function(){

    $("#myBtn").on('click', function (){
        var name = $(this).attr('dd');
        console.log(name);
        location.href=url;
    });

    $('#myBtn').on('click', function ulrHtml(name) {
             var toUrl = "target.html?param =" + param;
             window.open(toUrl);
         })
}

