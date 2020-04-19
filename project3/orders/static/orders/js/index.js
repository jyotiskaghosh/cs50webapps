document.addEventListener('DOMContentLoaded', () => {

    var cart = []

    if (!localStorage.getItem('cart')) {
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    else
        cart = JSON.parse(localStorage.getItem('cart'));

    // listen for click events
    document.querySelectorAll('.cart-add').forEach(item => {
        item.addEventListener('click', function(e) {
            const element = e.target;

            // add item to cart in local storage
            
            var parent = element.parentElement.parentElement.parentElement.parentElement;

            var id = parent.getAttribute('id');
           
            variation = ''
            if (parent.querySelector('.variations') != null) {
                var value = parent.querySelector('.variations').value.split(' ');
                variation = value[0]
            }
             
            item = {'user': user, 'id': id, 'variation': variation};
            
            cart.push(item);
            localStorage.setItem('cart', JSON.stringify(cart));
        })
    })  
})

// listen for change event
document.addEventListener('change', event => {
    const element = event.target;
    
    // change price according to variation
    if (element.className.includes('variations')) {
        parent = element.parentElement;
        value = element.value.split(' ');
        parent.querySelector('.price').innerHTML = value[1];
    }
})