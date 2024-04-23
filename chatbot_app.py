import streamlit as st
import requests

# Define the layout of the app
st.title('UWI CHATBOT')

# Adding a simple HTML greeting


col1, col2 = st.columns(2)

with col1:
    st.header("Chatbot")
    if 'chatbot_messages' not in st.session_state:
        st.session_state['chatbot_messages'] = "Chatbot: Hello! Type your message and press send.\n\n"
    
    chatbot_messages = st.text_area("Messages from Chatbot", value=st.session_state['chatbot_messages'], height=300, disabled=True)

with col2:
    st.header("User")
    user_input = st.text_input("Your message", key="user")
    if st.button("Send"):
        # Display user's message in text area
       
        # Sending POST request
        url = "http://localhost:8000/message/"
        body = {"message": user_input}
        response = requests.post(url, json=body)
        response_json = response.json()
        
        # Extract server response and handle potential missing fields
        server_response = response_json.get('response', 'No response from server')
        
        # Update chatbot messages
        st.session_state['chatbot_messages'] += f"\nUser: {user_input}\nChatbot: {server_response}"
        
        # Rerun the app to update the text area
        st.rerun()