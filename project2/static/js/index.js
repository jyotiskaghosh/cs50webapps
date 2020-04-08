document.addEventListener('DOMContentLoaded', () => {

    if (localStorage.getItem('last-visited')) {
        // Redirect to last channel
        let channel = localStorage.getItem('last-visited');   
        window.location.replace('/channel/' + channel);   
    }
    
    document.querySelector('#logout').addEventListener('click', () => {
        localStorage.removeItem('last-visited');
    })

    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#text').onkeyup = () => {
        if (document.querySelector('#text').value.length == 0 || document.querySelector('#text').value.indexOf(' ') >= 0)
            document.querySelector('#submit').disabled = true;
        else
            document.querySelector('#submit').disabled = false;

    };
});
