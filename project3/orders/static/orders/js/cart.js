document.addEventListener('DOMContentLoaded', () => {

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
        var reqitem = new XMLHttpRequest();
        reqitem.open('GET', '/api/item/'+item.id);
        reqitem.onload = () => {
            add_order(JSON.parse(reqitem.responseText));
        };
        reqitem.send()
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

        if (element.className.includes('submit')) {

            var parent = element.parentElement.parentElement.parentElement.parentElement;

            var name = parent.querySelector('.name').innerHTML;

            var variation = ''
            if (parent.querySelector('.variations')) 
                var variation = parent.querySelector('.variations').value.split(' ')[0];
            
            var topping_options = [];
            parent.querySelectorAll('.toppings').forEach(item => {
                topping_options.push({'name':item.value});
            });
        
            var quantity = parent.querySelector('.quantity').value;

            var json = {
                'name': name,
                'variation': variation,
                'toppings': topping_options,
                'quantity': quantity
            }
        
            var send_order = new XMLHttpRequest();
            send_order.open('POST', '/order/');
            send_order.onload = () => {
                let response = JSON.parse(send_order.responseText);
                if (response.success) {
                    cart.forEach( item => {
                            if (item.id == response.id) {
                                cart.splice(cart.indexOf(item), 1);
                            }
                        }
                    )
                    localStorage.setItem('cart', JSON.stringify(cart));
                    pop_order(parent);
                }
                else
                    alert(response.error);
            };
            send_order.send(JSON.stringify(json));
        }
        
        if (element.parentElement.className.includes('close')) {
            var parent = element.parentElement.parentElement.parentElement.parentElement;
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
    
    // change price according to variation
    if (element.className.includes('variations')) {
        parent = element.parentElement;
        value = element.value.split(' ')
        parent.querySelector('.price').innerHTML = value[1];
    }
})

function pop_order(element) {
    element.style.animationPlayState = 'running';
        element.addEventListener('animationend', () =>  {
            element.remove();
    });
}
