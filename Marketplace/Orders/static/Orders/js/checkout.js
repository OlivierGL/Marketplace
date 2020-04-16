$(document).ready(function () {
    setPayPalForm();
});

let checkoutPageSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/validateProductsOnStock/');

checkoutPageSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let errors = data['errors'];
    if (errors) {
        let message = "The following products are not available in stock anymore. Your cart has been updated. " + errors.join(', ');
        let type = "Error";
        showModal(message, type);
        $("#modalWsMessage").on('hidden.bs.modal', function () {
            // Go to cart page just when modal closes
            document.location.href = $("#paypalFormDiv").data("cartpageurl")
        });
    } else {
        $("#paypalFormDiv").children().trigger('submit', [{'shouldCallPayPal': true}]);
    }
};

checkoutPageSocket.onclose = function () {
    console.error('Websocket closed unexpectedly');
};

function setPayPalForm() {
    let paypalDiv = $("#paypalFormDiv");
    paypalDiv.children().on("submit", function (e, shouldCallPayPal) {
        if (!shouldCallPayPal) {
            e.preventDefault();
            let buyerId = paypalDiv.data("buyerid");
            let paypalInvoice = paypalDiv.data("paypalinvoice");
            checkoutPageSocket.send(JSON.stringify({
                'buyerId': buyerId,
                'paypalInvoice': paypalInvoice
            }));
        }
    });
}