import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import logging
import torch
import sys
import time
import psutil
from accelerate import init_empty_weights, infer_auto_device_map

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
            with init_empty_weights():
                print("Initializing empty weights for memory-efficient loading...")
                model_config = AutoModelForCausalLM.from_pretrained(self.model_path, cache_dir=self.model_cache_dir)
                print("Inferring device map...")
                device_map = infer_auto_device_map(
                    model_config, max_memory={"cpu": "32GB"}  # Force CPU usage
                )
                print(f"Device map: {device_map}")
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    cache_dir=self.model_cache_dir,
                    device_map=device_map,
                    torch_dtype=torch.float32,  # Use float32 for compatibility
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
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cpu")
            print(f"Inputs prepared on device: {inputs}")
            print(f"Attention mask: {inputs['attention_mask']}")

            # Track memory usage before generation
            memory_before = psutil.virtual_memory().used // (1024 ** 2)
            print(f"Memory usage before generation: {memory_before} MB")

            # Track start time
            start_time = time.time()

            print("Generating outputs...")
            outputs = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,  # Explicit attention mask
                max_length=100,
                temperature=0.7,
                do_sample=True,  # Enable sampling for varied results
                pad_token_id=self.tokenizer.eos_token_id  # Explicit pad token
            )
            end_time = time.time()

            # Track memory usage after generation
            memory_after = psutil.virtual_memory().used // (1024 ** 2)
            print(f"Memory usage after generation: {memory_after} MB")

            # Calculate time taken
            print(f"Time taken for generation: {end_time - start_time:.2f} seconds")

            # Log the number of tokens generated
            print(f"Number of tokens generated: {len(outputs[0])}")

            generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            print("\nGenerated Code:")
            print(generated_code)
        except Exception as e:
            print(f"Error during code generation: {e}")

if __name__ == "__main__":
    print("Starting main program...")
    model_path = "bigcode/starcoder"
    model_cache_dir = "./models/starcoder"

    access_token = ACCESS_TOKEN

    print("Creating CoderAgent instance...")
    coder_agent = CoderAgent(model_path=model_path, model_cache_dir=model_cache_dir, access_token=access_token)

    print("Checking or downloading model...")
    coder_agent.download_model()

    print("Testing the model...")
    coder_agent.test_model()
