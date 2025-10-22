from flask import Flask, render_template, request, jsonify
import numpy as np
import random
import ast
import math

app = Flask(__name__)

class ProjectCitadel:
    def __init__(self, key_matrix=None, block_size=2):
        self.mod = 26
        
        if key_matrix is None:
            self.block_size = block_size
            self.key_matrix = self.generate_valid_key_matrix()
        else:
            # convert to numpy array, ensure ints and mod 26
            self.key_matrix = np.array(key_matrix, dtype=int) % self.mod
            self.block_size = self.key_matrix.shape[0]
            if not self.is_valid_key(self.key_matrix):
                raise ValueError("Key matrix is not invertible mod 26")
        
        self.sbox = self.create_sbox()
        self.inverse_sbox = self.create_inverse_sbox()
    
    def is_valid_key(self, matrix):
        """Check if the key matrix is invertible mod 26"""
        if matrix.shape[0] != matrix.shape[1]:
            return False
        try:
            det = int(round(np.linalg.det(matrix))) % self.mod
        except Exception:
            return False
        return det != 0 and math.gcd(det, self.mod) == 1
    
    def create_sbox(self):
        """Create S-Box: S(x) = (7x + 3) mod 26"""
        return [(7 * x + 3) % self.mod for x in range(self.mod)]
    
    def create_inverse_sbox(self):
        """Create true inverse S-Box lookup table"""
        sbox = self.create_sbox()
        inverse = [0] * self.mod
        for i, val in enumerate(sbox):
            inverse[val] = i
        return inverse
    
    def generate_valid_key_matrix(self):
        """Generate a random valid key matrix (invertible mod 26)"""
        while True:
            matrix = np.random.randint(0, 26, (self.block_size, self.block_size))
            if self.is_valid_key(matrix):
                return matrix
    
    def text_to_vectors(self, text):
        """Convert text to numerical vectors (A=0, ..., Z=25)"""
        text = ''.join(filter(str.isalpha, str(text).upper()))
        if len(text) % self.block_size != 0:
            text += 'X' * (self.block_size - len(text) % self.block_size)
        
        numbers = [ord(char) - ord('A') for char in text]
        return [numbers[i:i + self.block_size] 
                for i in range(0, len(numbers), self.block_size)]
    
    def vectors_to_text(self, vectors):
        """Convert numerical vectors back to text"""
        numbers = []
        for vector in vectors:
            if isinstance(vector, np.ndarray):
                numbers.extend(vector.tolist())
            else:
                numbers.extend(vector)
        return ''.join(chr(int(num) + ord('A')) for num in numbers)
    
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
        return [random.randint(0, 25) for _ in range(self.block_size)]
    
    def encrypt_with_steps(self, plaintext):
        iv = self.generate_iv()
        plain_vectors = self.text_to_vectors(plaintext)
        cipher_vectors = []
        previous_block = iv
        
        steps = [{
            'step': 'Initial Setup',
            'details': [
                f'Plaintext: "{plaintext}"',
                f'Key Matrix: {self.key_matrix.tolist()}',
                f'IV: {iv}',
                f'Blocks: {plain_vectors}'
            ]
        }]
        
        for i, plain_vector in enumerate(plain_vectors):
            block_steps = []
            combined = self.add_vectors(plain_vector, previous_block)
            block_steps.append(f'CBC: {plain_vector} + {previous_block} = {combined}')
            
            hill_result = (np.dot(self.key_matrix, combined) % self.mod).astype(int).tolist()
            block_steps.append(f'Hill: {self.key_matrix.tolist()} × {combined} = {hill_result}')
            
            sbox_result = self.apply_sbox(hill_result, self.sbox)
            block_steps.append(f'S-Box: {hill_result} → {sbox_result}')
            
            cipher_vectors.append(sbox_result)
            previous_block = sbox_result
            
            steps.append({
                'step': f'Block {i+1} Encryption',
                'details': block_steps,
                'result': f'Cipher Block: {sbox_result}'
            })
        
        ciphertext = self.vectors_to_text(cipher_vectors)
        steps.append({'step': 'Final Result', 'details': [f'Ciphertext: "{ciphertext}"']})
        
        return ciphertext, iv, steps
    
    def decrypt_with_steps(self, ciphertext, iv):
        cipher_vectors = self.text_to_vectors(ciphertext)
        plain_vectors = []
        previous_block = iv
        
        det = int(round(np.linalg.det(self.key_matrix))) % self.mod
        det_inv = self.modular_inverse(det, self.mod)
        if det_inv is None:
            raise ValueError("Invalid key, determinant not invertible mod 26.")
        adjugate = np.round(np.linalg.inv(self.key_matrix) * np.linalg.det(self.key_matrix)).astype(int) % self.mod
        inv_key_matrix = (det_inv * adjugate) % self.mod
        
        steps = [{
            'step': 'Initial Setup',
            'details': [
                f'Ciphertext: "{ciphertext}"',
                f'IV: {iv}',
                f'Inverse Key: {inv_key_matrix.tolist()}',
                f'Blocks: {cipher_vectors}'
            ]
        }]
        
        for i, cipher_vector in enumerate(cipher_vectors):
            block_steps = []
            inverse_sbox_result = self.apply_sbox(cipher_vector, self.inverse_sbox)
            block_steps.append(f'Inverse S-Box: {cipher_vector} → {inverse_sbox_result}')
            
            hill_result = (np.dot(inv_key_matrix, inverse_sbox_result) % self.mod).astype(int).tolist()
            block_steps.append(f'Inverse Hill: {inv_key_matrix.tolist()} × {inverse_sbox_result} = {hill_result}')
            
            plain_vector = self.sub_vectors(hill_result, previous_block)
            block_steps.append(f'CBC: {hill_result} - {previous_block} = {plain_vector}')
            
            plain_vectors.append(plain_vector)
            previous_block = cipher_vector
            
            steps.append({
                'step': f'Block {i+1} Decryption',
                'details': block_steps,
                'result': f'Plain Block: {plain_vector}'
            })
        
        plaintext = self.vectors_to_text(plain_vectors)
        steps.append({'step': 'Final Result', 'details': [f'Decrypted: "{plaintext}"']})
        
        return plaintext, steps

    def modular_inverse(self, a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json or {}
    action = data.get('action')
    text = data.get('text', '')
    key_input = data.get('key_matrix', None)
    
    key_matrix = None
    if key_input is not None:
        try:
            if isinstance(key_input, str):
                parsed = ast.literal_eval(key_input)
                key_matrix = parsed
            else:
                key_matrix = key_input
        except Exception:
            return jsonify({'success': False, 'error': 'Invalid key matrix format'})
        # validate square
        if (not isinstance(key_matrix, list) or 
            not all(isinstance(row, list) for row in key_matrix) or
            len(key_matrix) == 0 or
            any(len(row) != len(key_matrix) for row in key_matrix)):
            return jsonify({'success': False, 'error': 'Key must be a square matrix (n×n)'})
    try:
        cipher = ProjectCitadel(key_matrix=key_matrix)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Key error: {str(e)}'})
    
    try:
        if action == 'encrypt':
            ciphertext, iv, steps = cipher.encrypt_with_steps(text)
            return jsonify({
                'success': True,
                'result': ciphertext,
                'iv': iv,
                'steps': steps,
                'key_matrix': cipher.key_matrix.tolist(),
                'sbox': cipher.sbox,
                'plaintext': text
            })
        elif action == 'decrypt':
            iv = data.get('iv')
            if iv is None:
                return jsonify({'success': False, 'error': 'IV missing for decryption'})
            plaintext, steps = cipher.decrypt_with_steps(text, iv)
            return jsonify({'success': True, 'result': plaintext, 'steps': steps})
        else:
            return jsonify({'success': False, 'error': 'Unknown action'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Processing error: {str(e)}'})

@app.route('/generate_key', methods=['POST'])
def generate_key():
    data = request.json or {}
    size = int(data.get('size', 2))  # default 2x2 if not provided
    try:
        cipher = ProjectCitadel(block_size=size)
        return jsonify({
            'success': True,
            'key_matrix': cipher.key_matrix.tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)