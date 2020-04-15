$(document).ready(function () {
    addShadowOnHover();
    setActiveNavBar();
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

function setActiveNavBar() {
    $(document).on('click', '.nav-item a', function () {
        $(this).parent().addClass('active').siblings().removeClass('active');
    });
}