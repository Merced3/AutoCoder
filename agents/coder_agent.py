import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import logging
import torch
import sys

# Configure transformers logging for detailed debug output
logging.set_verbosity_debug()

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cred import ACCESS_TOKEN

class CoderAgent:
    def __init__(self, model_path, model_cache_dir, access_token):
        print("Initializing CoderAgent...")
        self.model_path = model_path
        self.model_cache_dir = model_cache_dir
        self.access_token = access_token
        self.tokenizer = None
        self.model = None
        print(f"Initialized with model_path: {self.model_path}, cache_dir: {self.model_cache_dir}")

    def download_model(self):
        """Download the StarCoder model if not already present."""
        print("Checking if model exists in cache directory...")
        if not os.path.exists(self.model_cache_dir) or not os.listdir(self.model_cache_dir):
            print(f"Model not found in {self.model_cache_dir}. Starting download...")
            try:
                # Authenticate with Hugging Face token
                print("Downloading tokenizer...")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path,
                    cache_dir=self.model_cache_dir,
                    use_auth_token=self.access_token
                )
                print("Tokenizer downloaded successfully!")

                print("Downloading model...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    cache_dir=self.model_cache_dir,
                    use_auth_token=self.access_token
                )
                print("Model downloaded successfully!")
            except Exception as e:
                print(f"Error downloading model: {e}")
        else:
            print(f"Model already exists in {self.model_cache_dir}. Skipping download.")
            self.load_model()

    def load_model(self):
        """Load the model and tokenizer from the cache directory."""
        try:
            print(f"Loading tokenizer from {self.model_cache_dir}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, cache_dir=self.model_cache_dir)
            print("Tokenizer loaded successfully!")

            print(f"Loading model from {self.model_cache_dir}...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                cache_dir=self.model_cache_dir,
                torch_dtype=torch.float16,  # Reduce precision for memory savings
                device_map="auto",  # Automatically use CPU/GPU based on availability
                low_cpu_mem_usage=True  # Efficient memory usage
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")

    def test_model(self, prompt="Write a Python function to add two numbers."):
        """Generate code to test the model."""
        print("Starting test_model function...")
        if self.model is None or self.tokenizer is None:
            print("Model or tokenizer not loaded. Exiting test_model function.")
            return

        print(f"Prompt: {prompt}")
        try:
            print("Preparing input...")
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Inputs prepared: {inputs}")

            print("Generating outputs...")
            # Directly use the model without moving it manually
            outputs = self.model.generate(inputs.input_ids, max_length=100, temperature=0.7)
            print(f"Outputs generated: {outputs}")

            generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            print("\nGenerated Code:")
            print(generated_code)
        except Exception as e:
            print(f"Error during code generation: {e}")



if __name__ == "__main__":
    print("Starting main program...")
    # Define the model path and cache directory
    model_path = "bigcode/starcoder"
    model_cache_dir = "./models/starcoder"

    # Your Hugging Face access token
    access_token = ACCESS_TOKEN

    print("Creating CoderAgent instance...")
    # Create the CoderAgent instance
    coder_agent = CoderAgent(model_path=model_path, model_cache_dir=model_cache_dir, access_token=access_token)

    print("Checking or downloading model...")
    # Trigger the model download or load
    coder_agent.download_model()

    print("Testing the model...")
    # Test the model with a simple prompt
    coder_agent.test_model()
