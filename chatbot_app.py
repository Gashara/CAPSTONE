import streamlit as st

def get_response(user_input):
    # Dummy response generator - replace this with your actual chatbot model call
    return "Echo: " + user_input

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")

# Initialize session state for chat history if it does not exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

st.title('Chatbot Interface')
st.subheader("This is a simple chatbot interface with enhanced features.")

# Input text box for user
user_input = st.text_input("Type your message here:", key="user_input")

# Send button
send_button = st.button("Send")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state['history'] = []

if send_button and user_input:
    # Store user message in session
    st.session_state['history'].append(("You", user_input))

    # Get response from the chatbot function
    response = get_response(user_input)
    st.session_state['history'].append(("Bot", response))

    # Clear the input box after sending
    st.session_state.user_input = ""

# Display the chat history
for role, message in st.session_state['history']:
    if role == "You":
        st.text_area("", value=message, height=40, key=message[:10], style="color: blue; font-weight: bold;")
    else:
        st.text_area("", value=message, height=40, key=message[:10], style="color: green; font-weight: bold;")

# Keep scrolling to the last message
st.experimental_rerun()
