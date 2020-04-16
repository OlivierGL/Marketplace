$(document).ready(function () {
    setPayPalForm();
});

let checkoutPageSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/validateProductsOnStock/');

checkoutPageSocket.onmessage = function (e) {
    debugger;
    let data = JSON.parse(e.data);
    let errors = data['errors'];
    if (errors) {

    }
    else{
        $("#paypalFormDiv").children().trigger('submit', [{'shouldCallPayPal': true}]);
    }
};

checkoutPageSocket.onclose = function () {
    console.error('Websocket closed unexpectedly');
};

function setPayPalForm() {
    let paypalDiv = $("#paypalFormDiv");
    paypalDiv.children().on("submit", function (e, shouldCallPayPal) {
        debugger;
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