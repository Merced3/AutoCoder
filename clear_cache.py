import shutil
import os
from transformers import logging

# Function to locate the cache directory
def get_cache_dir():
    try:
        # Attempt to get the cache directory from Hugging Face Hub
        from huggingface_hub.file_download import HF_CACHE_HOME
        cache_dir = HF_CACHE_HOME
        print(f"Located Hugging Face cache directory using HF_CACHE_HOME: {cache_dir}")
        return cache_dir
    except ImportError:
        # Fallback to transformers' default cache location
        fallback_dir = os.path.expanduser("~/.cache/huggingface")
        print(f"Hugging Face Hub not installed or HF_CACHE_HOME unavailable. Using fallback: {fallback_dir}")
        return fallback_dir

# Clear the cache directory
def clear_cache():
    cache_dir = get_cache_dir()
    print(f"Cache directory to be cleared: {cache_dir}")
    
    if not os.path.exists(cache_dir):
        print("Cache directory does not exist or is already empty.")
        return

    try:
        print("Clearing cache directory...")
        shutil.rmtree(cache_dir)
        print("Cache cleared successfully.")
    except PermissionError as pe:
        print(f"Permission error: {pe}. Try running the script with elevated privileges.")
    except Exception as e:
        print(f"Error while clearing cache: {e}")

if __name__ == "__main__":
    # Set logging verbosity for debugging
    logging.set_verbosity_debug()
    print("Starting cache clearing process...")
    clear_cache()
    print("Cache clearing process completed.")
