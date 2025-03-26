import os
import shutil

def cleanup_user_data(user_id):
    temp_dir = f"temp_{user_id}"
    final_file = f"final_{user_id}.mp4"
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    if os.path.exists(final_file):
        os.remove(final_file)

def format_size(size_bytes):
    # Implement size formatting
    return "0MB"
