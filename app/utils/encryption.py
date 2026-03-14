from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import current_app
import base64
import hashlib
import os
import json

class EncryptionUtil:
    
    @staticmethod
    def get_key():
        """Lấy encryption key từ SECRET_KEY"""
        secret = current_app.config['SECRET_KEY'].encode()
        return hashlib.sha256(secret).digest()
    
    @staticmethod
    def encrypt_value(value):
        """Mã hóa một giá trị"""
        try:
            key = EncryptionUtil.get_key()
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            
            # Convert value sang bytes
            if isinstance(value, (dict, list)):
                plaintext = json.dumps(value).encode()
            elif isinstance(value, str):
                plaintext = value.encode()
            else:
                plaintext = str(value).encode()
            
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)
            encrypted = nonce + ciphertext
            
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return value
    
    @staticmethod
    def encrypt_dict(data, exclude_keys=None):
        """Mã hóa values trong dict, giữ nguyên keys"""
        if exclude_keys is None:
            exclude_keys = []
        
        encrypted_data = {}
        
        for key, value in data.items():
            if key in exclude_keys:
                encrypted_data[key] = value
            elif isinstance(value, dict):
                encrypted_data[key] = EncryptionUtil.encrypt_dict(value, exclude_keys)
            elif isinstance(value, list):
                encrypted_data[key] = [
                    EncryptionUtil.encrypt_dict(item, exclude_keys) if isinstance(item, dict) 
                    else EncryptionUtil.encrypt_value(item)
                    for item in value
                ]
            else:
                encrypted_data[key] = EncryptionUtil.encrypt_value(value)
        
        return encrypted_data
    
    @staticmethod
    def decrypt_value(encrypted_value):
        """Giải mã một giá trị"""
        try:
            key = EncryptionUtil.get_key()
            aesgcm = AESGCM(key)
            
            encrypted = base64.b64decode(encrypted_value.encode())
            nonce = encrypted[:12]
            ciphertext = encrypted[12:]
            
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            decrypted_str = plaintext.decode()
            
            # Thử parse JSON
            try:
                return json.loads(decrypted_str)
            except:
                return decrypted_str
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return encrypted_value
