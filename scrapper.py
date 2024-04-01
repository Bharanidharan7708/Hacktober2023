import google.generativeai as genai
 
genai.configure(api_key="AIzaSyBN6SSHyiu-Mqil86uqBwBP_zDT7gO7UF8")
 
# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
 
# Initialize the chat history
chat_history = []
 
# Start the conversation
convo = model.start_chat(history=chat_history)
 
# Get input from the user
while True:
    user_input = input("Enter your message: ")
    if user_input == "exit":
        break
 
    # Send the user's message to the model
    convo.send_message(user_input)
 
    # Append the new message to the chat history
    chat_history.append(convo.last)
 
    # Print the model's response
    print(convo.last.text)
