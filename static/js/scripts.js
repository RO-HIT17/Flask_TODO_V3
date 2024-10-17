    document.addEventListener('DOMContentLoaded', function() {
    const themeToggleButton = document.getElementById('theme-toggle');
    const lightThemeLink = document.getElementById('light-theme');
    const darkThemeLink = document.getElementById('dark-theme');

    if (localStorage.getItem('theme') === 'dark') {
    darkThemeLink.removeAttribute('disabled');
    lightThemeLink.setAttribute('disabled', 'disabled');
    themeToggleButton.textContent = 'Switch to Light Theme';
    }

    themeToggleButton.addEventListener('click', function() {
    if (darkThemeLink.disabled) {
        
        darkThemeLink.removeAttribute('disabled');
        lightThemeLink.setAttribute('disabled', 'disabled');
        localStorage.setItem('theme', 'dark');
        themeToggleButton.textContent = 'Switch to Light Theme';
    } else {
        lightThemeLink.removeAttribute('disabled');
        darkThemeLink.setAttribute('disabled', 'disabled');
        localStorage.setItem('theme', 'light');
        themeToggleButton.textContent = 'Switch to Dark Theme';
    }
    });

    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0');
    var year = today.getFullYear();
    var todayDate = year + '-' + month + '-' + day;
    var deadlineDateInput = document.getElementById('deadlineDate');
    if (deadlineDateInput) {
    deadlineDateInput.value = todayDate;
    }
    });

    function initializeSpeechRecognition() {
    const startVoiceInput = document.getElementById('startVoiceInput');
    const taskInput = document.getElementById('taskInput');

    startVoiceInput.addEventListener('click', function() {
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!window.SpeechRecognition) {
            alert("Your browser does not support Speech Recognition.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();  

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            taskInput.value = transcript; 
        };

        recognition.onspeechend = function() {
            recognition.stop();
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
        };
    });
    }

    initializeSpeechRecognition();
    function openEditDialog(taskId, title, priority, deadline) {
    const editDialog = document.getElementById('editTaskDialog');

    document.getElementById('taskId').value = taskId;
    document.getElementById('taskTitle').value = title;
    document.getElementById('taskPriority').value = priority;
    document.getElementById('taskDeadline').value = deadline;

    editDialog.showModal();
    }

    function closeEditDialog() {
    const editDialog = document.getElementById('editTaskDialog');
    editDialog.close();
    }
