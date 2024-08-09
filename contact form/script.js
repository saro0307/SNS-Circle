document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    // Gather form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Basic validation
    if (name === '' || email === '' || message === '') {
        document.getElementById('formMessage').textContent = 'Please fill out all fields.';
        return;
    }

    // Normally, here you'd send the data to the server via fetch or XMLHttpRequest
    // For example:
    /*
    fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('formMessage').textContent = 'Message sent successfully!';
    })
    .catch(error => {
        document.getElementById('formMessage').textContent = 'An error occurred.';
    });
    */

    // For demonstration purposes, we'll just show a success message
    document.getElementById('formMessage').textContent = 'Message sent successfully!';
});
