import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from cred import ACCESS_TOKEN

class CoderAgent:
    def __init__(self, model_path, model_cache_dir, access_token):
        self.model_path = model_path
        self.model_cache_dir = model_cache_dir
        self.access_token = access_token

    def download_model(self):
        """Download the StarCoder model if not already present."""
        if not os.path.exists(self.model_cache_dir) or not os.listdir(self.model_cache_dir):
            print(f"Downloading StarCoder model to {self.model_cache_dir}...")
            try:
                # Authenticate with Hugging Face token
                auth_headers = {"Authorization": f"Bearer {self.access_token}"}

                # Download tokenizer
                tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path,
                    cache_dir=self.model_cache_dir,
                    use_auth_token=self.access_token
                )
                print("Tokenizer downloaded successfully!")

                # Download model
                model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    cache_dir=self.model_cache_dir,
                    use_auth_token=self.access_token
                )
                print("Model downloaded successfully!")
            except Exception as e:
                print(f"Error downloading model: {e}")
        else:
            print("Model already exists. Skipping download.")

if __name__ == "__main__":
    # Define the model path and cache directory
    model_path = "bigcode/starcoder"
    model_cache_dir = "./models/starcoder"

    # Your Hugging Face access token
    access_token = ACCESS_TOKEN

    # Create the CoderAgent instance
    coder_agent = CoderAgent(model_path=model_path, model_cache_dir=model_cache_dir, access_token=access_token)

    # Trigger the model download
    coder_agent.download_model()
