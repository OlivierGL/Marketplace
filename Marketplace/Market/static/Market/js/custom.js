$(document).ready(function () {
    addShadowOnHover();
});

function addShadowOnHover() {
    $(".card").hover(
        function () {
            $(this).addClass('shadow-lg').css('cursor', 'pointer');
        }, function () {
            $(this).removeClass('shadow-lg');
        }
    );
}