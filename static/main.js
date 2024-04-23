/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}

/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showUserMessage` and `showBotMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper">
			<div class="text">${args.text}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/* Sends a message when the 'Enter' key is pressed.
 */
$(document).ready(function() {
    $('#msg_input').keydown(function(e) {
        // Check for 'Enter' key
        if (e.key === 'Enter') {
            // Prevent default behaviour of enter key
            e.preventDefault();
			// Trigger send button click event
            $('#send_button').click();
        }
    });
});

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showUserMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showBotMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}

/**
 * Get input from user and show it on screen on button click.
 */
$('#send_button').on('click', function (e) {
    let userInput = $('#msg_input').val();
    $('#msg_input').val(''); // Clear the input after capturing the value
    showUserMessage(userInput); // Show the user message immediately

    // Now send this input to the backend for a response
    $.ajax({
        url: 'http://localhost:8000/message/', // Ensure the URL matches your FastAPI host and port
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: userInput }),
        success: function (response) {
            // Assuming the backend sends back a JSON with a 'response' key
			// console.log(response.response.response)
            showBotMessage(response.response.response);
        },
        error: function (xhr, status, error) {
            // Handle errors
            showBotMessage("Sorry, I couldn't process that message.");
        }
	});
});
   

/**
 * Returns a random string. Just to specify bot message to the user.
 */
// function randomstring(length = 20) {
// 	let output = '';

// 	// magic function
// 	var randomchar = function () {
// 		var n = Math.floor(Math.random() * 62);
// 		if (n < 10) return n;
// 		if (n < 36) return String.fromCharCode(n + 55);
// 		return String.fromCharCode(n + 61);
// 	};

// 	while (output.length < length) output += randomchar();
// 	return output;
// }

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
	showBotMessage('Hello there! Type in a message.');
});

