import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(text):
    """Send a request to the Hugging Face model to get a summary."""
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 1500,  # Maximum length of the summary
            "min_length": 500,  # Minimum length of the summary
            "num_return_sequences": 1,
            "do_sample": True
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    keys_list = list(response.json()[0].keys())

    # Get the index you're interested in
    index = 0
    # Use the index to get the key
    key_at_index = keys_list[index] 
    return response.json()[0][key_at_index]

def allowed_file(filename):
    """Check if the file is a PDF."""
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
