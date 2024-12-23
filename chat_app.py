import requests
import json
import gradio as gr

# API URL and Headers
url = "http://localhost:11434/api/generate"  # Ensure the API is running on this URL
headers = {
    'Content-Type': 'application/json',
}

# Global conversation history
conversation_history = []

# Function to generate response
def generate_response(prompt):
    """
    This function sends the user's prompt and conversation history to the API,
    receives the model's response, and updates the conversation history.
    """
    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Format the conversation history into a single string for the model
    full_prompt = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])

    # Prepare payload for the API
    data = {
        "model": "falcon3",
        "stream": False,
        "prompt": full_prompt,
    }

    # Send POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Handle the API response
    if response.status_code == 200:
        response_data = response.json()
        model_response = response_data["response"]

        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": model_response})

        # Format the chat history for display
        formatted_history = "\n".join([f"{item['role']}: {item['content']}" for item in conversation_history])
        return formatted_history  # Return the full conversation
    else:
        # Handle errors and display them
        error_message = f"Error: {response.status_code} - {response.text}"
        print(error_message)
        return error_message

# Define the Gradio interface
with gr.Blocks() as chat_ui:
    gr.Markdown("# 🧠 Chat with Ollama GPT")
    gr.Markdown("Welcome! Type your question below and interact with the bot.")
    
    # Chat History Display
    chatbox = gr.Textbox(label="Conversation", lines=15, interactive=False)

    # User Input and Submit Button
    with gr.Row():
        user_input = gr.Textbox(label="Your Input", placeholder="Type your message here...", lines=2)
        submit_button = gr.Button("Send")

    # Connect UI components with the function
    submit_button.click(
        fn=generate_response,  # Function to call
        inputs=user_input,     # Input from the user
        outputs=chatbox        # Update chat history display
    )

# Launch the Gradio app
chat_ui.launch()