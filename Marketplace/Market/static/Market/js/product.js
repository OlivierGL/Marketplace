$(document).ready(function () {
    bindMinusButton();
    bindPlusButton();
    setUpAddToCartButton();
    setAddToCartClickEvent();
});

let productPageSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/addProductToCart/');

productPageSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);

    let qtyInStock = data['qtyInStock'];
    $('#qtyInStock').text(qtyInStock);
    if (qtyInStock <= 0) {
        disableAddButton();
    }

    let qtyInCart = data['qtyInCart'];
    if (qtyInCart <= 0) {
        $("#addToCartButton").html('Add to cart');
    } else {
        $("#addToCartButton").html('Update quantity in cart');
    }
    setUpAddToCartButton();

    let message = data['message'];
    let type = data['type'];
    showModal(message, type);
};

productPageSocket.onclose = function () {
    console.error('Websocket closed unexpectedly');
};

function disableAddButton() {
    let addToCartButton = $('#addToCartButton');
    addToCartButton.prop("disabled", true);
    addToCartButton.removeClass("btn-primary");
}

function setUpAddToCartButton() {
    let qtyInStock = $('#qtyInStock').text();
    let qtyToAddInput = $("#qtyToAddInput");
    if (qtyInStock <= 0) {
        qtyToAddInput.attr({
            "max": 0,
            "min": 0
        });
        qtyToAddInput.val(0);
        disableAddButton();
        showModal('Quantity in stock insufficient.', 'Error');
    } else {
        let addToCartButton = $('#addToCartButton');
        if (!addToCartButton.data("qtytoadd")) {
            addToCartButton.data("qtytoadd", 1);
        }
        let qtyAlreadyInCart = addToCartButton.data("qtytoadd");
        qtyToAddInput.attr({
            "max": $('#qtyInStock').text(),
            "min": 0
        });
        qtyToAddInput.val(qtyAlreadyInCart);
    }
}

function bindMinusButton() {
    $('#minus').click(function () {
        this.parentNode.querySelector('#qtyToAddInput').stepDown();
        let newValue = this.parentNode.querySelector('#qtyToAddInput').value;
        $('#addToCartButton').data("qtytoadd", newValue)
    });
}

function bindPlusButton() {
    $('#plus').click(function () {
        this.parentNode.querySelector('#qtyToAddInput').stepUp();
        let newValue = this.parentNode.querySelector('#qtyToAddInput').value;
        $('#addToCartButton').data("qtytoadd", newValue)
    });
}

function setAddToCartClickEvent() {
    $('#addToCartButton').click(function () {
        let cartId = $('#addToCartButton').data("cartid");
        let productId = $('#addToCartButton').data("productid");
        let qty = $('#addToCartButton').data("qtytoadd");

        productPageSocket.send(JSON.stringify({
            'cartId': cartId,
            'productId': productId,
            'quantity': qty
        }));
    })
}
