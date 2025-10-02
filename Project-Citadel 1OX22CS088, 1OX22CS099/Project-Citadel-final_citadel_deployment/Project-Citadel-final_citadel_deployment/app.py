from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import random
import ast
import math
import base64
import io
from PIL import Image
import os
import json
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)
CORS(app)

class ProjectCitadel:
    def __init__(self, key_matrix=None, block_size=2):
        self.mod = 256  # Using 256 for binary data instead of 26 for text
        
        if key_matrix is None:
            self.block_size = block_size
            self.key_matrix = self.generate_valid_key_matrix()
        else:
            # convert to numpy array, ensure ints and mod 256
            self.key_matrix = np.array(key_matrix, dtype=int) % self.mod
            self.block_size = self.key_matrix.shape[0]
            if not self.is_valid_key(self.key_matrix):
                raise ValueError("Key matrix is not invertible mod 256")
        
        self.sbox = self.create_sbox()
        self.inverse_sbox = self.create_inverse_sbox()
    
    def is_valid_key(self, matrix):
        """Check if the key matrix is invertible mod 256"""
        if matrix.shape[0] != matrix.shape[1]:
            return False
        try:
            det = int(round(np.linalg.det(matrix))) % self.mod
        except Exception:
            return False
        return det != 0 and math.gcd(det, self.mod) == 1
    
    def create_sbox(self):
        """Create S-Box: S(x) = (7x + 3) mod 256 for binary data"""
        return [(7 * x + 3) % self.mod for x in range(self.mod)]
    
    def create_inverse_sbox(self):
        """Create true inverse S-Box lookup table"""
        sbox = self.create_sbox()
        inverse = [0] * self.mod
        for i, val in enumerate(sbox):
            inverse[val] = i
        return inverse
    
    def generate_valid_key_matrix(self):
        """Generate a random valid key matrix (invertible mod 256)"""
        while True:
            matrix = np.random.randint(0, 256, (self.block_size, self.block_size))
            if self.is_valid_key(matrix):
                return matrix
    
    def add_vectors(self, vec1, vec2):
        v1 = vec1.tolist() if isinstance(vec1, np.ndarray) else vec1
        v2 = vec2.tolist() if isinstance(vec2, np.ndarray) else vec2
        return [(a + b) % self.mod for a, b in zip(v1, v2)]
    
    def sub_vectors(self, vec1, vec2):
        v1 = vec1.tolist() if isinstance(vec1, np.ndarray) else vec1
        v2 = vec2.tolist() if isinstance(vec2, np.ndarray) else vec2
        return [(a - b) % self.mod for a, b in zip(v1, v2)]
    
    def apply_sbox(self, vector, sbox):
        v = vector.tolist() if isinstance(vector, np.ndarray) else vector
        return [sbox[int(x)] for x in v]
    
    def generate_iv(self):
        return [random.randint(0, 255) for _ in range(self.block_size)]
    
    def encrypt_binary(self, data):
        """Encrypt binary data using Project Citadel"""
        # Convert data to bytes if it's not already
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate IV
        iv = self.generate_iv()
        
        # Convert data to list of integers (0-255)
        data_bytes = list(data)
        
        # Pad data to be multiple of block_size
        padding_length = self.block_size - (len(data_bytes) % self.block_size)
        data_bytes += [padding_length] * padding_length
        
        # Encrypt each block
        cipher_bytes = []
        previous_block = iv
        
        for i in range(0, len(data_bytes), self.block_size):
            block = data_bytes[i:i+self.block_size]
            
            # CBC mode: XOR with previous ciphertext block
            combined = self.add_vectors(block, previous_block)
            
            # Hill cipher: matrix multiplication
            hill_result = (np.dot(self.key_matrix, combined) % self.mod).astype(int).tolist()
            
            # S-Box substitution
            sbox_result = self.apply_sbox(hill_result, self.sbox)
            
            cipher_bytes.extend(sbox_result)
            previous_block = sbox_result
        
        # Convert back to bytes
        ciphertext = bytes(cipher_bytes)
        return ciphertext, iv
    
    def decrypt_binary(self, ciphertext, iv):
        """Decrypt binary data using Project Citadel"""
        # Convert ciphertext to list of integers (0-255)
        cipher_bytes = list(ciphertext)
        
        # Calculate inverse key matrix
        det = int(round(np.linalg.det(self.key_matrix))) % self.mod
        det_inv = self.modular_inverse(det, self.mod)
        if det_inv is None:
            raise ValueError("Invalid key, determinant not invertible mod 256.")
        adjugate = np.round(np.linalg.inv(self.key_matrix) * np.linalg.det(self.key_matrix)).astype(int) % self.mod
        inv_key_matrix = (det_inv * adjugate) % self.mod
        
        # Decrypt each block
        plain_bytes = []
        previous_block = iv
        
        for i in range(0, len(cipher_bytes), self.block_size):
            block = cipher_bytes[i:i+self.block_size]
            
            # Inverse S-Box
            inverse_sbox_result = self.apply_sbox(block, self.inverse_sbox)
            
            # Inverse Hill cipher
            hill_result = (np.dot(inv_key_matrix, inverse_sbox_result) % self.mod).astype(int).tolist()
            
            # CBC mode: XOR with previous ciphertext block
            plain_block = self.sub_vectors(hill_result, previous_block)
            
            plain_bytes.extend(plain_block)
            previous_block = block
        
        # Remove padding
        padding_length = plain_bytes[-1]
        if padding_length < self.block_size:
            plain_bytes = plain_bytes[:-padding_length]
        
        # Convert back to bytes
        plaintext = bytes(plain_bytes)
        return plaintext

    def modular_inverse(self, a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt_pdf', methods=['POST'])
def encrypt_pdf():
    try:
        # Get the file from request
        file = request.files['file']
        key_input = request.form.get('key_matrix')
        
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        # Read file data
        file_data = file.read()
        
        # Parse key matrix
        key_matrix = ast.literal_eval(key_input) if key_input else None
        cipher = ProjectCitadel(key_matrix=key_matrix)
        
        # Encrypt the file data
        ciphertext, iv = cipher.encrypt_binary(file_data)
        
        # Return the encrypted data and IV
        return jsonify({
            'success': True,
            'filename': file.filename,
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': iv,
            'key_matrix': cipher.key_matrix.tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'PDF encryption error: {str(e)}'})

@app.route('/decrypt_pdf', methods=['POST'])
def decrypt_pdf():
    try:
        # Get the file from request
        file = request.files['file']
        key_input = request.form.get('key_matrix')
        iv_input = request.form.get('iv')
        
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        # Read file data
        file_data = file.read()
        
        # Parse key matrix and IV
        key_matrix = ast.literal_eval(key_input) if key_input else None
        iv = ast.literal_eval(iv_input) if iv_input else None
        
        if not key_matrix or not iv:
            return jsonify({'success': False, 'error': 'Key matrix and IV are required'})
        
        cipher = ProjectCitadel(key_matrix=key_matrix)
        
        # Decrypt the file data
        plaintext = cipher.decrypt_binary(file_data, iv)
        
        # Create a response with the decrypted file
        return send_file(
            io.BytesIO(plaintext),
            as_attachment=True,
            download_name=f"decrypted_{file.filename}",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': f'PDF decryption error: {str(e)}'})

@app.route('/encrypt_image', methods=['POST'])
def encrypt_image():
    try:
        # Get the image from request
        image_file = request.files['image']
        key_input = request.form.get('key_matrix')
        
        if not image_file:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Open and process the image
        image = Image.open(image_file)
        
        # Convert image to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()
        
        # Parse key matrix
        key_matrix = ast.literal_eval(key_input) if key_input else None
        cipher = ProjectCitadel(key_matrix=key_matrix)
        
        # Encrypt the image data
        ciphertext, iv = cipher.encrypt_binary(img_data)
        
        # Return the encrypted data and IV
        return jsonify({
            'success': True,
            'filename': image_file.filename,
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': iv,
            'key_matrix': cipher.key_matrix.tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Image encryption error: {str(e)}'})

@app.route('/decrypt_image', methods=['POST'])
def decrypt_image():
    try:
        # Get the image from request
        image_file = request.files['image']
        key_input = request.form.get('key_matrix')
        iv_input = request.form.get('iv')
        
        if not image_file:
            return jsonify({'success': False, 'error': 'No image provided'})
        
        # Read image data
        img_data = image_file.read()
        
        # Parse key matrix and IV
        key_matrix = ast.literal_eval(key_input) if key_input else None
        iv = ast.literal_eval(iv_input) if iv_input else None
        
        if not key_matrix or not iv:
            return jsonify({'success': False, 'error': 'Key matrix and IV are required'})
        
        cipher = ProjectCitadel(key_matrix=key_matrix)
        
        # Decrypt the image data
        plaintext = cipher.decrypt_binary(img_data, iv)
        
        # Convert back to image
        image = Image.open(io.BytesIO(plaintext))
        
        # Save image to bytes for response
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Return the decrypted image
        return send_file(
            img_byte_arr,
            as_attachment=True,
            download_name=f"decrypted_{image_file.filename}",
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': f'Image decryption error: {str(e)}'})

if __name__ == '__main__':
     app.run(debug=False, host='0.0.0.0', port=5000)
