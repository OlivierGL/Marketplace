$(document).ready(function () {
    bindMinusButton();
    bindPlusButton();
    setUpAddToCartButton();
});

let productPageSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/addProductToCart/');

productPageSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let message = data['message'];
    let type = data['type'];
    let qtyInStock = data['qtyInStock'];

    $('#qtyInStock').text(qtyInStock);
    if (qtyInStock <= 0) {
        disableAddButton();
    }
    setUpAddToCartButton();
    showModal(message, type);
};

productPageSocket.onclose = function () {
    console.error('Websocket closed unexpectedly');
};

function showModal(message, type) {
    $('#ws_message').text(message);
    $('#modalWsMessageTitle').text(type);
    $('#modalWsMessage').modal('show');
}

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
        $('#qtyToAddToCart').text(0);
        disableAddButton();
        showModal('Quantity in stock insufficient.', 'Error');
    } else {
        qtyToAddInput.attr({
            "max": $('#qtyInStock').text(),
            "min": 1
        });
        qtyToAddInput.val(1);
        $('#qtyToAddToCart').text(1);
        $('#addToCartButton').click(function () {
            debugger;
            let cartId = $('#addToCartButton').data("cartid");
            let productId = $('#addToCartButton').data("productid");
            let qty = $('#qtyToAddInput').val();

            productPageSocket.send(JSON.stringify({
                'cartId': cartId,
                'productId': productId,
                'quantity': qty
            }));
        })
    }
}

function bindMinusButton() {
    $('#minus').click(function () {
        this.parentNode.querySelector('#qtyToAddInput').stepDown();
        $('#qtyToAddToCart').text(this.parentNode.querySelector('#qtyToAddInput').value);
    });
}

function bindPlusButton() {
    $('#plus').click(function () {
        this.parentNode.querySelector('#qtyToAddInput').stepUp();
        $('#qtyToAddToCart').text(this.parentNode.querySelector('#qtyToAddInput').value);
    });
}