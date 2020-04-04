$(document).ready(function () {
    addShadowOnHover();
    setUpAddToCartButton();
    $('#qtyToAddToCart').text(1);
    bindMinusButton();
    bindPlusButton();
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

function setUpAddToCartButton() {
    $('#addToCartButton').click(function () {
        let cartId = $(this).attr("data-cartId");
        let productId = $(this).attr("data-productId");
        let qty = $('#quantityToAdd').val();
        let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "POST",
            url: "/addtocart/",
            data: {
                'cartId': cartId,
                'productId': productId,
                'quantity': qty,
                'csrfmiddlewaretoken': csrfToken
            }
        });
    })
}

function bindMinusButton() {
    $('#minus').click(function () {
        this.parentNode.querySelector('#quantityToAdd').stepDown();
        $('#qtyToAddToCart').text(this.parentNode.querySelector('#quantityToAdd').value);
    });
}

function bindPlusButton() {
    $('#plus').click(function () {
        this.parentNode.querySelector('#quantityToAdd').stepUp();
        $('#qtyToAddToCart').text(this.parentNode.querySelector('#quantityToAdd').value);
    });
}