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

function showModal(message, type) {
    $('#ws_message').text(message);
    $('#modalWsMessageTitle').text(type);
    $('#modalWsMessage').modal('show');
}