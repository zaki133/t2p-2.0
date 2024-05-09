import openai

class ApiCaller:
    def __init__(self, api_key):
        # Initialize the OpenAI client with the provided API key
        self.client = openai.OpenAI(api_key=api_key)

    def run(self, text):
        try:
            # Sending a chat completion to the OpenAI API and getting the response
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": text}
                ],
                model="gpt-4-turbo",  
                max_tokens=4096  ################# CHANGE THIS LATER
            )
            # Return the text of the first completion in the response
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            # Handle exceptions that might occur during the API call
            return f"An error occurred: {str(e)}"
