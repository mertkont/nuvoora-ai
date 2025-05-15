// DOM Elements
const menuItems = document.querySelectorAll('.menu-item');
const sections = document.querySelectorAll('.section');
const aiChatButton = document.getElementById('aiChatButton');
const aiChatContainer = document.getElementById('aiChatContainer');
const aiCloseButton = document.getElementById('aiCloseButton');
const aiChatMessages = document.getElementById('aiChatMessages');
const aiChatForm = document.getElementById('aiChatForm');
const aiChatInput = document.getElementById('aiChatInput');
const charCount = document.getElementById('char-count');
const aiSendButton = document.getElementById('aiSendButton');
const loginButton = document.getElementById('loginButton');
const logoutButton = document.getElementById('logoutButton');
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const quickReplies = document.getElementById('quickReplies');
const aiNotification = document.getElementById('aiNotification');
const notificationText = document.getElementById('notificationText');
const notificationOpen = document.getElementById('notificationOpen');
const notificationDismiss = document.getElementById('notificationDismiss');
const aiChatHeader = document.getElementById('aiChatHeader');

// State
let currentSection = 'home';
let isChatOpen = false;
let isLoggedIn = false;
let isTyping = false;
const userData = {
    firstName: '',
    lastName: '',
    apiKey: ''
};

// Quick reply messages by section
const quickRepliesBySection = {
    home: ['Hello', 'Help', 'How does it work?'],
    services: ['What services do you offer?', 'What are the prices?', 'More information'],
    about: ['About the company', 'Who is your team?', 'How long have you been active?'],
    contact: ['Contact information', 'Office location', 'Feedback']
};

// Welcome messages by section
const welcomeMessagesBySection = {
    home: 'I am Nuvoora, your AI assistant. You are on the home page. How can I help you?',
    services: 'You are on the services page. Which service would you like to know more about?',
    about: 'You are on the about page. What would you like to know about our company or team?',
    contact: 'You are on the contact page. You can use our contact information to reach us or you can ask me.'
};

// Notification messages by section
const notificationMessagesBySection = {
    home: 'You are on the home page! Can I help you?',
    services: 'Would you like to know more about our services?',
    about: 'Would you like to learn more about us?',
    contact: 'Would you like to contact me?'
};

// Check if user is logged in from cookies
function checkLoginStatus() {
    const firstName = getCookie('firstName');
    const lastName = getCookie('lastName');
    const apiKey = getCookie('apiKey');

    if (firstName && lastName && apiKey) {
        userData.firstName = firstName;
        userData.lastName = lastName;
        userData.apiKey = apiKey;
        isLoggedIn = true;
        updateLoginUI();
        return true;
    }
    return false;
}

// Update UI based on login status
function updateLoginUI() {
    if (isLoggedIn) {
        loginButton.style.display = 'none';
        logoutButton.style.display = 'block';
    } else {
        loginButton.style.display = 'block';
        logoutButton.style.display = 'none';
    }
}

// Set cookies
function setCookie(name, value, days = 30) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Get cookie
function getCookie(name) {
    const cookieName = name + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return "";
}

// Delete cookies
function deleteCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}


// Add a message to the chat
function addMessage(message, isUser = false) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'ai-message');

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');

    if (!isUser) {
        message = message.replace(/<\|file_separator\|>/g, '').replace(/<\|im_end\|>/g, '');
        message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        message = message.replace(/\n+$/, '');

        const lines = message.split('\n');
        let formattedLines = [];
        let currentListItems = [];
        let inList = false;
        let listType = null;

        for (let line of lines) {
            const orderedMatch = line.match(/^(\d+)\.\s+(.*)$/);
            const unorderedMatchStar = line.match(/^\*\s+(.*)$/);
            const unorderedMatchDash = line.match(/^-\s+(.*)$/);

            if (orderedMatch) {
                if (listType === 'ul' && currentListItems.length > 0) {
                    formattedLines.push(`<ul style="margin-left: 20px;">${currentListItems.join('')}</ul>`);
                    currentListItems = [];
                }
                listType = 'ol';
                currentListItems.push(`<li>${orderedMatch[2]}</li>`);
                inList = true;
            } else if (unorderedMatchStar || unorderedMatchDash) {
                if (listType === 'ol' && currentListItems.length > 0) {
                    formattedLines.push(`<ol style="margin-left: 20px;">${currentListItems.join('')}</ol>`);
                    currentListItems = [];
                }
                listType = 'ul';
                const listItemContent = unorderedMatchStar ? unorderedMatchStar[1] : unorderedMatchDash[1];
                currentListItems.push(`<li>${listItemContent}</li>`);
                inList = true;
            } else {
                if (inList && currentListItems.length > 0) {
                    formattedLines.push(`<${listType} style="margin-left: 20px;">${currentListItems.join('')}</${listType}>`);
                    currentListItems = [];
                    inList = false;
                    listType = null;
                }
                formattedLines.push(line);
            }
        }

        if (inList && currentListItems.length > 0) {
            formattedLines.push(`<${listType} style="margin-left: 20px;">${currentListItems.join('')}</${listType}>`);
        }

        messageContent.innerHTML = formattedLines
            .map(line => line.startsWith('<ol>') || line.startsWith('<ul') ? line : line + '<br>')
            .join('');

    } else {
        messageContent.textContent = message;
    }

    messageElement.appendChild(messageContent);

    const timestamp = document.createElement('div');
    timestamp.classList.add('message-timestamp');
    const now = new Date();
    timestamp.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    messageElement.appendChild(timestamp);

    aiChatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Show typing indicator
function showTypingIndicator() {
    if (isTyping) return;

    isTyping = true;
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('typing-indicator');
    typingIndicator.id = 'typingIndicator';

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('typing-dot');
        typingIndicator.appendChild(dot);
    }

    aiChatMessages.appendChild(typingIndicator);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
        isTyping = false;
    }
}

// Scroll chat to bottom
function scrollToBottom() {
    aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
}

// Send a message to the API
async function sendMessage(message) {
    if (!isLoggedIn) {
        addMessage('Please login first.', false);
        return;
    }

    addMessage(message, true);
    showTypingIndicator();

    try {
        const response = await fetch('http://127.0.0.1:8000/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: message,
                access_token: userData.apiKey
            })
        });

        if (!response.ok) {
            throw new Error('API did not respond');
        }

        const data = await response.json();
        hideTypingIndicator();

        // Process and display the response from the API
        addMessage(data.response, false);
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Sorry, an error occurred. Please try again later.', false);
    }
}

// Show welcome message based on current section
function showWelcomeMessage() {
    if (isChatOpen) {
        const welcomeMessage = welcomeMessagesBySection[currentSection] || welcomeMessagesBySection.home;
        const greeting = isLoggedIn ? `Hello ${userData.firstName}! ${welcomeMessage}` : welcomeMessage;
        addMessage(greeting, false);
    }
}

// Update quick replies based on current section
function updateQuickReplies() {
    const replies = quickRepliesBySection[currentSection] || quickRepliesBySection.home;
    quickReplies.innerHTML = '';

    replies.forEach(reply => {
        const quickReply = document.createElement('div');
        quickReply.classList.add('quick-reply');
        quickReply.textContent = reply;
        quickReply.addEventListener('click', () => {
            aiChatInput.value = reply;
            // Call the message sending function directly instead of triggering the form submit event
            const message = aiChatInput.value.trim();
            if (message) {
                sendMessage(message);
                aiChatInput.value = '';
                charCount.textContent = "0 / 1000"; // Reset the character counter
            }
        });
        quickReplies.appendChild(quickReply);
    });
}

// Show notification
function showNotification() {
    if (!isChatOpen) {
        const message = notificationMessagesBySection[currentSection] || notificationMessagesBySection.home;
        notificationText.textContent = isLoggedIn ?
            `Hello ${userData.firstName}! ${message}` : message;
        aiNotification.classList.add('show');

        // Hide notification after 10 seconds
        setTimeout(() => {
            if (aiNotification.classList.contains('show')) {
                aiNotification.classList.remove('show');
            }
        }, 10000);
    }
}

// Initialize chat
function initChat() {
    aiChatMessages.innerHTML = '';
    updateQuickReplies();
    showWelcomeMessage();
}

// Event listeners
menuItems.forEach(item => {
    item.addEventListener('click', () => {
        const target = item.dataset.section;

        // Update active section
        sections.forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(target).classList.add('active');

        // Update 'active' class in menu items
        menuItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        // Show section message
        const message = welcomeMessagesBySection[target];
        if (message) {
            addMessage(message, false); // Show as AI message
        }

        // Update quick replies
        updateQuickReplies(target);

        // Change notification text
        const notifMessage = notificationMessagesBySection[target];
        if (notifMessage) {
            notificationText.textContent = notifMessage;
        }

        currentSection = target;
    });
});

aiChatInput.addEventListener('input', () => {
    const length = aiChatInput.value.length;
    charCount.textContent = `${length} / 1000`;
});

aiCloseButton.addEventListener('click', () => {
    aiChatContainer.classList.remove('open');
    isChatOpen = false;

    // Reset position
    setTimeout(() => {
        resetChatPosition();
    }, 300); // After closing animation completes
});

aiCloseButton.addEventListener('click', () => {
    const hasCustomPosition = aiChatContainer.style.left || aiChatContainer.style.top;

    if (hasCustomPosition) {
        aiChatContainer.style.transition = 'none';
        aiChatContainer.classList.remove('open');

        setTimeout(resetChatPosition, 100);
    } else {
        aiChatContainer.classList.remove('open');
    }

    isChatOpen = false;
});

aiChatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = aiChatInput.value.trim();

    if (message) {
        sendMessage(message);
        aiChatInput.value = '';
    }
});

loginButton.addEventListener('click', () => {
    loginModal.classList.add('active');
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const apiKey = document.getElementById('apiKey').value.trim();

    if (firstName && lastName && apiKey) {
        userData.firstName = firstName;
        userData.lastName = lastName;
        userData.apiKey = apiKey;

        // Save to cookies
        setCookie('firstName', firstName);
        setCookie('lastName', lastName);
        setCookie('apiKey', apiKey);

        isLoggedIn = true;
        updateLoginUI();
        loginModal.classList.remove('active');

        // Update welcome message if chat is open
        if (isChatOpen) {
            addMessage(`Welcome, ${firstName}! How can I help you?`, false);
        } else {
            // Show notification
            notificationText.textContent = `Welcome, ${firstName}! How can I help you?`;
            aiNotification.classList.add('show');
        }
    }
});

logoutButton.addEventListener('click', () => {
    // Clear user data
    userData.firstName = '';
    userData.lastName = '';
    userData.apiKey = '';

    // Delete cookies
    deleteCookie('firstName');
    deleteCookie('lastName');
    deleteCookie('apiKey');

    isLoggedIn = false;
    updateLoginUI();

    // Update welcome message if chat is open
    if (isChatOpen) {
        addMessage('You have logged out. See you next time!', false);
    }
});

document.addEventListener('click', (e) => {
    if (loginModal.classList.contains('active') && !e.target.closest('.modal') && !e.target.closest('.login-btn')) {
        loginModal.classList.remove('active');
    }
});

aiChatButton.addEventListener('click', () => {
    resetChatPosition();
    aiChatContainer.style.display = ''; // Ensure visibility

    setTimeout(() => {
        aiChatContainer.classList.add('open');
        isChatOpen = true;
        aiNotification.classList.remove('show');

        if (aiChatMessages.children.length === 0) {
            initChat();
        }
    }, 10);
});

notificationOpen.addEventListener('click', () => {
    aiNotification.classList.remove('show');
    aiChatButton.click();
});

notificationDismiss.addEventListener('click', () => {
    aiNotification.classList.remove('show');
});



let isDragging = false;
let offsetX, offsetY;

function resetChatPosition() {
    aiChatContainer.style.left = '';
    aiChatContainer.style.top = '';
    aiChatContainer.style.position = 'fixed';
    aiChatContainer.style.transform = '';
    aiChatContainer.style.transition = '';
    aiChatContainer.style.bottom = '';  // Clear bottom value

    // Reset visibility
    if (!isChatOpen) {
        aiChatContainer.style.display = 'none';
        setTimeout(() => {
            aiChatContainer.style.display = '';
            aiChatContainer.style.transition = 'bottom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        }, 50);
    } else {
        aiChatContainer.style.transition = 'bottom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    }
}

aiChatHeader.addEventListener('mousedown', function (e) {
    if (aiChatContainer.classList.contains('open')) {
        isDragging = true;

        const rect = aiChatContainer.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;

        aiChatContainer.style.transition = 'none';

        document.addEventListener('mousemove', dragElement);
        document.addEventListener('mouseup', stopDragging);

        e.preventDefault();
    }
});

function dragElement(e) {
    if (!isDragging) return;

    aiChatContainer.style.left = `${e.clientX - offsetX}px`;
    aiChatContainer.style.top = `${e.clientY - offsetY}px`;

    aiChatContainer.style.bottom = '';

    e.preventDefault();
}

function stopDragging() {
    isDragging = false;
    document.removeEventListener('mousemove', dragElement);
    document.removeEventListener('mouseup', stopDragging);
}

// Show random notifications periodically
function scheduleRandomNotification() {
    if (!isChatOpen && Math.random() > 0.5) {
        setTimeout(() => {
            const randomMessages = [
                'Can I help you?',
                'Do you have a question?',
                'How are you today?',
                'Do you need any information?'
            ];
            const randomMessage = randomMessages[Math.floor(Math.random() * randomMessages.length)];

            notificationText.textContent = isLoggedIn ?
                `Hello ${userData.firstName}! ${randomMessage}` : randomMessage;

            aiNotification.classList.add('show');

            // Hide notification after 10 seconds
            setTimeout(() => {
                if (aiNotification.classList.contains('show')) {
                    aiNotification.classList.remove('show');
                }
            }, 10000);
        }, Math.random() * 60000 + 30000); // Show between 30s and 90s
    }

    // Schedule next notification
    setTimeout(scheduleRandomNotification, Math.random() * 120000 + 60000); // Schedule between 1-3 minutes
}

// Initialize the app
function init() {
    checkLoginStatus();
    updateQuickReplies();

    // Show initial notification after 5 seconds
    setTimeout(showNotification, 5000);

    // Start random notifications after 1 minute
    setTimeout(scheduleRandomNotification, 60000);
}

// Call init when the page loads
window.addEventListener('load', init);

document.addEventListener('DOMContentLoaded', function () {
    // Select theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');

    // Load user's theme preference from local storage
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Apply saved theme when page loads
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    // Theme toggle function
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        // Set theme to HTML data-theme attribute
        document.documentElement.setAttribute('data-theme', newTheme);

        // Change the theme toggle button icon
        if (newTheme === 'dark') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }

        // Save user's theme preference
        localStorage.setItem('theme', newTheme);
    }

    // Listen for clicks on the theme toggle button
    themeToggle.addEventListener('click', toggleTheme);

    // Check system theme preference (optional)
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Change theme when system preference changes (optional)
    prefersDarkScheme.addEventListener('change', function (e) {
        // If user hasn't selected a theme before
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);

            if (newTheme === 'dark') {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        }
    });
});
