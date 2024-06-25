document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    
    const websocket = new WebSocket('ws://localhost:6789/');
    
    websocket.onmessage = function(event) {
        let messageElement = document.createElement('div');
        messageElement.textContent = event.data;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    sendButton.addEventListener("click", () => {
        let message = messageInput.value;
        if (message) {
            websocket.send(message);
            messageInput.value = '';
        }
    });
});
