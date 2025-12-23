// API Configuration
const API_BASE_URL = window.location.origin;
const API_CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;
const API_CLEAR_CHAT_ENDPOINT = `${API_BASE_URL}/api/clear-chat`;

// DOM Elements - will be initialized after DOM loads
let chatForm, userInput, chatMessages, sendButton, loadingIndicator, welcomeSection;

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    chatForm = document.getElementById('chat-form');
    userInput = document.getElementById('user-input');
    chatMessages = document.getElementById('chat-messages');
    sendButton = document.getElementById('send-button');
    loadingIndicator = document.getElementById('loading-indicator');
    welcomeSection = document.querySelector('.welcome-section');
    
    // Validate all required elements exist
    if (!chatForm || !userInput || !chatMessages || !sendButton || !loadingIndicator) {
        console.error('Error: Required DOM elements not found. Please check the HTML structure.');
        return;
    }
    
    // Initialize UI
    userInput.focus();
    adjustTextareaHeight();
    
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        adjustTextareaHeight();
        updateSendButton();
    });
    
    // Update send button state
    userInput.addEventListener('input', updateSendButton);
    
    // Setup form handler
    chatForm.addEventListener('submit', handleFormSubmit);
    
    // Handle Enter key (send) and Shift+Enter (new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (userInput.value.trim() && !sendButton.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // New chat button functionality
    const newChatBtn = document.querySelector('.new-chat-btn');
    if (newChatBtn) {
        newChatBtn.addEventListener('click', handleNewChat);
    }
    
    console.log('Frontend initialized successfully');
    console.log('API endpoint:', API_CHAT_ENDPOINT);
});

// Adjust textarea height based on content
function adjustTextareaHeight() {
    userInput.style.height = 'auto';
    const scrollHeight = userInput.scrollHeight;
    const maxHeight = 200;
    userInput.style.height = Math.min(scrollHeight, maxHeight) + 'px';
}

// Update send button state
function updateSendButton() {
    const hasText = userInput.value.trim().length > 0;
    sendButton.disabled = !hasText;
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;

    // Remove welcome section on first message
    if (welcomeSection && welcomeSection.parentElement) {
        welcomeSection.remove();
    }

    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';
    adjustTextareaHeight();
    updateSendButton();
    
    // Disable input while processing
    setInputDisabled(true);
    showLoading(true);

    try {
        // Send message to API
        console.log('Sending message to:', API_CHAT_ENDPOINT);
        console.log('Message:', message);
        
        const response = await fetch(API_CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);

        if (!response.ok) {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
                console.error('Error response:', errorData);
            } catch (e) {
                const errorText = await response.text();
                console.error('Error response text:', errorText);
                errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();
        console.log('Response data:', data);
        
        // Validate response structure
        if (!data || !data.response) {
            throw new Error('Invalid response format from server');
        }
        
        // Add bot response to chat
        addMessage(data.response, 'bot');
        
    } catch (error) {
        console.error('Error details:', error);
        let errorMessage = error.message || 'An unknown error occurred';
        
        // Handle network errors
        if (error instanceof TypeError && error.message.includes('fetch')) {
            errorMessage = 'Unable to connect to the server. Please check if the backend is running.';
        }
        
        addMessage(
            `Sorry, I encountered an error: ${errorMessage}. Please try again.`,
            'bot',
            true
        );
    } finally {
        showLoading(false);
        setInputDisabled(false);
        userInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Create message group wrapper
    const messageGroup = document.createElement('div');
    messageGroup.className = 'message-group';
    
    // Create avatar
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    if (sender === 'user') {
        avatar.textContent = 'U';
    } else {
        avatar.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
    }
    
    // Create content wrapper
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content-wrapper';
    
    // Create message content
    const contentDiv = document.createElement('div');
    contentDiv.className = `message-content ${isError ? 'error-message' : ''}`;
    
    // Split text by newlines and create paragraphs
    const paragraphs = text.split('\n\n');
    paragraphs.forEach((para) => {
        if (para.trim()) {
            const textParagraph = document.createElement('p');
            textParagraph.textContent = para.trim();
            contentDiv.appendChild(textParagraph);
        }
    });
    
    // If no paragraphs were created, add the text directly
    if (contentDiv.children.length === 0) {
        const textParagraph = document.createElement('p');
        textParagraph.textContent = text;
        contentDiv.appendChild(textParagraph);
    }
    
    // Assemble structure
    contentWrapper.appendChild(contentDiv);
    
    messageGroup.appendChild(avatar);
    messageGroup.appendChild(contentWrapper);
    
    messageDiv.appendChild(messageGroup);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom smoothly
    setTimeout(() => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

// Show/hide loading indicator
function showLoading(show) {
    loadingIndicator.style.display = show ? 'block' : 'none';
    
    if (show) {
        // Scroll to show loading indicator
        setTimeout(() => {
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }
}

// Enable/disable input
function setInputDisabled(disabled) {
    userInput.disabled = disabled;
    sendButton.disabled = disabled || userInput.value.trim().length === 0;
}

// New chat button handler
async function handleNewChat() {
    try {
        // Clear chat history on backend
        const response = await fetch(API_CLEAR_CHAT_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            console.log('Chat history cleared on server');
        }
    } catch (error) {
        console.error('Error clearing chat history:', error);
    }
    
    // Clear all messages from UI
    const messages = chatMessages.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());
    
    // Hide loading indicator
    loadingIndicator.style.display = 'none';
    
    // Restore welcome section
    const existingWelcome = chatMessages.querySelector('.welcome-section');
    if (!existingWelcome && welcomeSection) {
        chatMessages.insertBefore(welcomeSection, chatMessages.firstChild);
    }
    
    // Clear input
    userInput.value = '';
    adjustTextareaHeight();
    updateSendButton();
    userInput.focus();
}

