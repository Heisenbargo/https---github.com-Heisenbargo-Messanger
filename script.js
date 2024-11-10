function sendMessage() {
    const messageContent = document.getElementById("messageInput").value;
    fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: messageContent, receiver_id: 2 }) // Замените на ID получателя
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            loadMessages();
            document.getElementById("messageInput").value = "";  // Очистить поле ввода
        }
    });
}

function loadMessages() {
    fetch("/get_messages?receiver_id=2") // Замените на ID получателя
        .then(response => response.json())
        .then(messages => {
            const messagesContainer = document.getElementById("messages");
            messagesContainer.innerHTML = "";  // Очистить старые сообщения
            messages.forEach(msg => {
                const messageElement = document.createElement("p");
                messageElement.textContent = `${msg.sender}: ${msg.content}`;
                messagesContainer.appendChild(messageElement);
            });
        });
}

// Автоматическое обновление сообщений каждые 3 секунды
setInterval(loadMessages, 3000);
