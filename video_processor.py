import os
import base64
import hashlib
import threading
from Crypto.Cipher import AES
import requests
import m3u8
from config import Config

class VideoProcessor:
    def __init__(self):
        self.config = Config()
        self.lock = threading.Lock()
        
    def _generate_key(self, time_val, token):
        n = time_val[-4:]
        r, i, o = int(n[0]), int(n[1:3]), int(n[3])
        combined = time_val + token[r:i]
        digest = hashlib.sha256(combined.encode()).digest()
        return base64.b64encode(digest[:16 if o ==6 else 24 if o ==7 else 32]).decode()

    def _decrypt_segment(self, data, key, iv):
        key = base64.b64decode(key)
        iv = base64.b64decode(iv)
        return AES.new(key, AES.MODE_CBC, iv).decrypt(base64.b64decode(data))

    async def download_video(self, encrypted_url, iv, token, user_id, max_segments=0):
        try:
            # Initialize download
            playlist = m3u8.load(encrypted_url)
            segments = playlist.segments[:max_segments] if max_segments else playlist.segments
            
            # Create temp directory
            temp_dir = f"temp_{user_id}"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download segments
            total = len(segments)
            for idx, segment in enumerate(segments):
                ext = segment.uri.split('.')[-1]
                response = requests.get(segment.uri, timeout=15)
                
                # Apply decoding based on extension
                decoded_data = self._decode_data(response.content.decode(), ext)
                
                # Decrypt and save
                decrypted = self._decrypt_segment(decoded_data, key, iv)
                with open(f"{temp_dir}/seg_{idx}.ts", "wb") as f:
                    f.write(decrypted)
                
                # Progress update
                with self.lock:
                    print(f"Downloaded {idx+1}/{total} segments")
            
            # Combine segments
            output_file = f"final_{user_id}.mp4"
            self._combine_segments(temp_dir, output_file)
            return output_file
            
        except Exception as e:
            print(f"Download Error: {str(e)}")
            return None
        finally:
            self._cleanup(temp_dir)

    def _decode_data(self, data, ext):
        # Implement your tsb/tsc/tsd decoders here
        return data  # Placeholder

    def _combine_segments(self, temp_dir, output_file):
        with open(output_file, 'wb') as outfile:
            for file in sorted(os.listdir(temp_dir)):
                with open(f"{temp_dir}/{file}", 'rb') as infile:
                    outfile.write(infile.read())

    def _cleanup(self, temp_dir):
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(f"{temp_dir}/{file}")
            os.rmdir(temp_dir)
