document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#submit').disabled = true;
    localStorage.setItem('last-visited', title);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port); 

    document.querySelector('#home').addEventListener('click', () => {
        localStorage.removeItem('last-visited');
    })

    document.querySelector('#logout').addEventListener('click', () => {
        localStorage.removeItem('last-visited');
    })

    // Enable button only if there is text in the input field
    document.querySelector('#text').onkeyup = () => {
        if (document.querySelector('#text').value.length > 0)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };

    // When connected, configure buttons
    socket.on('connect', () => {
        
        // button should emit a message event
        document.querySelector('#message-form').onsubmit = () => {

            var text = document.querySelector('#text').value;
            socket.emit('message', {'title': title, 'user': user, 'text': text});
            return false;
        };
    });

    // If delete button is clicked, delete the message, emit delete
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'delete') {
            let id = element.parentElement.getAttribute('data-id');
            pop_message(element.parentElement);
            socket.emit('delete', {'title': title, 'id': id}); 
        }
    });

    // When a message is received check if it's meant for this channel if yes add message
    socket.on('message', data => {

        if (data.title === title)
        {   
            add_message(data);

            if (document.querySelectorAll('.text-box').length > 100)
                pop_message(document.querySelector('.text-box'));
        }
    });

    // When a message is received check if it's meant for this channel if yes add message
    socket.on('delete', data => {

        if (data.title === title)
        {   
            element = document.querySelector(`[data-id="${data.id}"]`);
            pop_message(element);
        }
    });

    // Add a new post with given contents to DOM.
    const message_template = Handlebars.compile(document.querySelector('#message').innerHTML);

    // Add a new post with delete button with given contents to DOM.
    const my_message_template = Handlebars.compile(document.querySelector('#my-message').innerHTML);
    function add_message(contents) {
        
        if (user === contents.user)
            var message = my_message_template({'id':contents.id, 'user':contents.user, 'timestamp':contents.timestamp, 'text':contents.text});
        else
            var message = message_template({'id':contents.id, 'user':contents.user, 'timestamp':contents.timestamp, 'text':contents.text});

        // Add post to DOM.
        document.querySelector('#messages').innerHTML += message;
    }

    function pop_message(element) {
        element.style.animationPlayState = 'running';
            element.addEventListener('animationend', () =>  {
                element.remove();
        });
    }
});
