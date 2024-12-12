// Select DOM elements
const userInput = document.getElementById("user-input");
const messagesContainer = document.getElementById("chat-messages");

// Function to handle sending messages
async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (!userMessage) return; // Ignore empty input

    // Display the user's message in the chat
    addMessage(userMessage, "user");

    // Clear the input field
    userInput.value = "";

    try {
        // Send the user's message to the backend
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }), // Pass user message to the backend
        });

        // Parse the response from the backend
        const data = await response.json();

        // Display the bot's response in the chat
        addMessage(data.response, "bot");
    } catch (error) {
        // Handle errors (e.g., backend not reachable)
        addMessage("Error connecting to the server. Please try again later.", "bot");
    }
}

// Function to add a message to the chat container
function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`; // Apply user/bot styling
    messageDiv.textContent = text; // Set the message text
    messagesContainer.appendChild(messageDiv); // Add message to chat container
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to the latest message
}

// Attach event listener for the "Enter" key
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage(); // Send message on pressing Enter
    }
});
