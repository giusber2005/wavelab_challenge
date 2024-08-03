document.addEventListener('DOMContentLoaded', () => {

    //with the data from the database
    //populate like in the function addMessage the chatMessages div with messages from the history of the chat
    //we want to create x messages were x is the lenght of the chatData
    //for each data index create two messages: 1 for the user and 1 for the machine

    //updating the chat with new messages
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    function addMessage(text, user = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${user ? 'user' : 'other'}`;
        messageDiv.innerHTML = `<div class="message-text">${text}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }

    fetch('/check-database')
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }

        // Create an array of objects with keys id, user, and machine
        const chatDataArray = data.map(item => ({
            id: item.id || 'N/A',        // Handle missing data
            user: item.user || 'N/A',    // Handle missing data
            machine: item.machine || 'N/A' // Handle missing data
        }));

        // Populate chatMessages with entries from chatDataArray
        chatDataArray.forEach(entry => {
            const text = `${entry.user}`;
            // Assuming user flag can be determined based on some logic, for now set as true for all
            addMessage(text, true);

            const text2 = `${entry.user}`;
            addMessage(text2, false);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

    sendButton.addEventListener('click', () => {
        const messageText = messageInput.value.trim();
        if (messageText) {
            addMessage(messageText);
            messageInput.value = ''; // Clear input field
        }
    });

    // Optional: Allow pressing "Enter" to send a message
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendButton.click();
        }
    });
});
