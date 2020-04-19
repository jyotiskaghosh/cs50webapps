document.addEventListener('DOMContentLoaded', () => {

    var csrftoken = Cookies.get('csrftoken');

    var cart = []

    if (!localStorage.getItem('cart')) {
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    else
        cart = JSON.parse(localStorage.getItem('cart'));

    var toppings = [];

    var toppingsreq = new XMLHttpRequest();
    toppingsreq.open('GET', '/api/toppings');
    toppingsreq.onload = () => {
        toppings = JSON.parse(toppingsreq.responseText);
    };
    toppingsreq.send()

    cart.forEach( item => {

        if (item.user == user) {
            var reqitem = new XMLHttpRequest();
            reqitem.open('GET', '/api/item/'+item.id);
            reqitem.onload = () => {
                add_order(JSON.parse(reqitem.responseText));
            };
            reqitem.send()
        }
    })

    const order_template = Handlebars.compile(document.querySelector('#order').innerHTML);
    const toppings_template = Handlebars.compile(document.querySelector('#toppings').innerHTML);

    function add_order(contents) {

        var toppings_html = toppings_template({'toppings':toppings.toppings})

        var topping_select = '';

        contents.more_features.forEach( element => {
            if ('num_of_toppings' in element) {
                for (var i=0; i < element.num_of_toppings; i++){
                    topping_select += toppings_html;
                }
            }
        })

        var order = order_template({'id': contents.id, 'name':contents.name, 'img':contents.img, 'price':contents.price,
            'variations':contents.variations, 'topping_select':topping_select});
        
        // Add post to DOM.
        document.querySelector('#cart').innerHTML += order;
    }
     
    document.addEventListener('click', event => {

        const element = event.target;
        var parent = element.parentElement.parentElement.parentElement.parentElement;

        if (element.className.includes('submit')) {

            var id = parent.getAttribute('id');

            var variation = ''
            if (parent.querySelector('.variations')) 
                var variation = parent.querySelector('.variations').value.split(' ')[0];
            
            var topping_options = [];
            parent.querySelectorAll('.toppings').forEach(item => {
                topping_options.push({'name':item.value});
            });
        
            var quantity = parent.querySelector('.quantity').value;

            var json = {
                'id': id,
                'variation': variation,
                'toppings': topping_options,
                'quantity': quantity
            }
        
            var send_order = new XMLHttpRequest();
            send_order.open('POST', '/api/order');
            send_order.setRequestHeader("X-CSRFToken", csrftoken);
            send_order.onload = function() {
                let response = JSON.parse(this.responseText);
                if (this.readyState == 4 && this.status == '200') {
                    cart.forEach( item => {
                            if (item.id == id) {
                                cart.splice(cart.indexOf(item), 1);
                            }
                        }
                    )
                    localStorage.setItem('cart', JSON.stringify(cart));
                    pop_order(parent);
                }
            };
            send_order.send(JSON.stringify(json));
        }
        
        if (element.parentElement.className.includes('close')) {
            cart.forEach( item => {
                    if (item.id == parent.getAttribute('id')) {
                        cart.splice(cart.indexOf(item), 1);
                    }
                }
            )
            localStorage.setItem('cart', JSON.stringify(cart));
            pop_order(parent);
        }
    })
})

// listen for change event
document.addEventListener('change', event => {
    const element = event.target;
    
    // change price according to variation and quantity
    parent = element.parentElement;
    value = element.value.split(' ');
    
    var quantity = parent.querySelector('.quantity').value;

    if (parent.querySelector('.variations')) {
        var var_price = parent.querySelector('.variations').value.split(' ')[1];
        var price = var_price * quantity;
    }
    else {
        var price = parseInt(parent.querySelector('.price').innerHTML) * quantity
    }
    
    parent.querySelector('.price').innerHTML = price.toFixed(2);

})

function pop_order(element) {
    element.style.animationPlayState = 'running';
        element.addEventListener('animationend', () =>  {
            element.remove();
    });
}
