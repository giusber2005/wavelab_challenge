document.addEventListener('DOMContentLoaded', () => {

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

            const text2 = `${entry.machine}`;
            addMessage(text2, false);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

    const startChatForms =  document.querySelectorAll('startChatForm');

    startChatForms.forEach(startChatForm => {
        startChatForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
        
            // Show the spinner
            document.getElementById('loadingWheel').style.display = 'block';
            
            // Prepare the form data
            const formData = new FormData(this);
            let route = '';
    
            let value = document.getElementById('value');
            if (value.value === "1") {
                route = '/start_chat_page';
            } else if (value.value === "2") {
                route = '/chat_page';
            }
            // Create an AJAX request
            fetch(route, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                // Handle the server response
                return response.json(); // or response.text() if not JSON
            })
            .then(data => {
                // Process the response data
                console.log('Success:', data);
                if (data.redirect) {
                    // Redirect to the specified URL
                    window.location.href = data.redirect;
                }
            })
            .catch(error => {
                // Handle errors
                console.error('Error:', error);
            })
            .finally(() => {
                // Hide the spinner
                document.getElementById('loadingWheel').style.display = 'none';
            });
        });
    });
    

    //function to start recording audio
    let mediaRecorder;
    let audioChunks = [];

    let stopButton = document.getElementById('stopButton');

    //on blick of the recordButton:
    //ask permission for recording the audio
    //record the audio and store it in the file input inside the fileStorage input
    document.getElementById('recordButton').addEventListener('click', async () => {

        // Request microphone access
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            stopButton.style.display = 'block';
            document.getElementById('recordButton').disabled = true;
            document.getElementById('loadingWheel').style.display = 'block';

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                document.getElementById('audioForm').style.display = 'block';
                document.getElementById('loadingWheel').style.display = 'none';

                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('audioStorage').src = audioUrl;
            };

            mediaRecorder.start();
            console.log('Recording started');
        } catch (error) {
            console.error('Error accessing microphone:', error);
        }
    });

    document.getElementById('stopButton').addEventListener('click', () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
            console.log('Recording stopped');
        }
    });

});
