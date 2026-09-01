document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Get CSRF token from form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to UI
        appendMessage(message, 'user');
        chatInput.value = '';

        // Show loading indicator
        const loadingId = showLoading();

        try {
            const response = await fetch('/chatbot/api/chat/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            removeLoading(loadingId);

            if (response.ok) {
                appendBotResponse(data);
            } else {
                appendMessage(`Error: ${JSON.stringify(data)}`, 'bot');
            }
        } catch (error) {
            removeLoading(loadingId);
            appendMessage(`Error: Could not connect to the server. ${error.message}`, 'bot');
        }
    });

    function appendMessage(text, sender) {
        const isUser = sender === 'user';
        const msgRow = document.createElement('div');
        msgRow.className = `msg-row ${isUser ? 'sent' : 'recv'}`;
        
        let avatarHtml = isUser ? '' : '<div class="msg-avatar"><i class="ti ti-robot"></i></div>';
        
        const timeStr = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const ticks = isUser ? '<i class="ti ti-checks" style="color:#53bdeb; font-size:14px"></i>' : '';

        msgRow.innerHTML = `
            ${avatarHtml}
            <div class="msg-bubble">
                ${text}
                <div class="msg-meta">${timeStr} ${ticks}</div>
            </div>
        `;
        
        chatMessages.appendChild(msgRow);
        scrollToBottom();
    }

    function appendBotResponse(response) {
        const msgRow = document.createElement('div');
        msgRow.className = 'msg-row recv';
        
        const avatarHtml = '<div class="msg-avatar"><i class="ti ti-robot"></i></div>';
        const timeStr = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-bubble';
        
        const replyText = document.createElement('div');
        replyText.textContent = response.reply;
        contentDiv.appendChild(replyText);

        if (response.data) {
            let actualData = response.data;
            
            // If the backend wraps the array in {"data": [...]} or {"results": [...]}
            if (typeof actualData === 'object' && !Array.isArray(actualData)) {
                if (Array.isArray(actualData.data)) {
                    actualData = actualData.data;
                } else if (Array.isArray(actualData.results)) {
                    actualData = actualData.results;
                }
            }

            if (Array.isArray(actualData) && actualData.length > 0) {
                contentDiv.appendChild(createTable(actualData));
            } else if (typeof actualData === 'object') {
                contentDiv.appendChild(createCard(actualData));
            } else if (typeof response.data === 'object') {
                // Fallback to original object if actualData was somehow cleared
                contentDiv.appendChild(createCard(response.data));
            }
        }

        const metaDiv = document.createElement('div');
        metaDiv.className = 'msg-meta';
        metaDiv.innerHTML = `${timeStr}`;
        contentDiv.appendChild(metaDiv);

        msgRow.innerHTML = avatarHtml;
        msgRow.appendChild(contentDiv);
        
        chatMessages.appendChild(msgRow);
        scrollToBottom();
    }

    function createTable(dataArray) {
        if (!dataArray || dataArray.length === 0) return document.createTextNode('');
        
        const table = document.createElement('table');
        table.className = 'data-table';
        
        // Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const keys = Object.keys(dataArray[0]);
        keys.forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Body
        const tbody = document.createElement('tbody');
        dataArray.forEach(item => {
            const tr = document.createElement('tr');
            keys.forEach(key => {
                const td = document.createElement('td');
                td.textContent = typeof item[key] === 'object' ? JSON.stringify(item[key]) : item[key];
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        
        return table;
    }

    function createCard(dataObj) {
        const card = document.createElement('div');
        card.className = 'data-card';
        
        for (const [key, value] of Object.entries(dataObj)) {
            const item = document.createElement('div');
            item.className = 'data-card-item';
            
            const label = document.createElement('span');
            label.className = 'data-card-label';
            label.textContent = key;
            
            const val = document.createElement('span');
            val.textContent = typeof value === 'object' ? JSON.stringify(value) : value;
            
            item.appendChild(label);
            item.appendChild(val);
            card.appendChild(item);
        }
        
        return card;
    }

    function showLoading() {
        const id = 'loading-' + Date.now();
        const msgRow = document.createElement('div');
        msgRow.className = 'msg-row recv';
        msgRow.id = id;
        
        msgRow.innerHTML = `
            <div class="msg-avatar"><i class="ti ti-robot"></i></div>
            <div class="msg-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(msgRow);
        scrollToBottom();
        return id;
    }

    function removeLoading(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
