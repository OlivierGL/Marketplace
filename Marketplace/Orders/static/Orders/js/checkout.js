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
        let message = "An error has occurred and your order could not be processed. Please try again later.";
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
            let totalAmount = $("#totalAmount").text();
            let subtotalAmount = $("#subtotalAmount").text();
            let provTaxes = $("#provTaxes").text();
            let fedTaxes = $("#fedTaxes").text();
            checkoutPageSocket.send(JSON.stringify({
                'buyerId': buyerId,
                'paypalInvoice': paypalInvoice,
                'totalAmount': totalAmount,
                'subtotalAmount': subtotalAmount,
                'provTaxes': provTaxes,
                'fedTaxes': fedTaxes,
            }));
        }
    });
}