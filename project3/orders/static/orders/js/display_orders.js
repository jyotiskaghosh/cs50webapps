document.addEventListener('DOMContentLoaded', () => {

    var csrftoken = Cookies.get('csrftoken');

    document.addEventListener('click', event => {

        const element = event.target;
        var parent = element.parentElement.parentElement;
        var id = parent.getAttribute('id');
    
        if (element.className.includes('submit')) {

            var json = {
                'id': id,
                'status': 'completed'
            }
        
            var update_order = new XMLHttpRequest();
            update_order.open('POST', '/api/orders/update/');
            update_order.setRequestHeader("X-CSRFToken", csrftoken);
            update_order.onload = function() {
                if (this.readyState == 4 && this.status == '200') {
                    pop_order(parent);
                }
            };
            update_order.send(JSON.stringify(json));
        }

        if (element.parentElement.className.includes('close')) {

            var json = {
                'id': id,
                'status': 'cancelled'
            }
        
            var update_order = new XMLHttpRequest();
            update_order.open('POST', '/api/orders/update/');
            update_order.setRequestHeader("X-CSRFToken", csrftoken);
            update_order.onload = function() {
                if (this.readyState == 4 && this.status == '200') {
                    pop_order(parent);
                }
            };
            update_order.send(JSON.stringify(json));
        }
    })
    
})

function pop_order(element) {
    element.style.animationPlayState = 'running';
        element.addEventListener('animationend', () =>  {
            element.remove();
    });
}