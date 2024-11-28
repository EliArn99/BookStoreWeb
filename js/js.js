var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;

        console.log('productId:', productId, 'Action:', action);

        if (user === 'AnonymousUser') {
            console.log('User is not authenticated');
            addCookieItem(productId, action); // Handle cart using cookies
        } else {
            updateUserOrder(productId, action); // Update cart in the database
        }
    });
}

function addCookieItem(productId, action) {
    console.log('Unauthenticated user - updating cart with cookies');

    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    if (action === 'add') {
        if (!cart[productId]) {
            cart[productId] = { quantity: 0 };
        }
        cart[productId]['quantity'] += 1;
    }

    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    localStorage.setItem('cart', JSON.stringify(cart));
    location.reload(); // Reload page to update cart
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    const url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Data:', data);
            location.reload();
        })
        .catch((error) => console.error('Error:', error));
}
