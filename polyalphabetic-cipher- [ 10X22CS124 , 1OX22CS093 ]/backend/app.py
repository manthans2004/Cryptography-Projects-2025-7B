from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ========== CORRECTED CLASSIC VIGENÈRE ==========
def encrypt_classic(plaintext, key):
    ciphertext = ""
    key_len = len(key)
    key_index = 0
    
    for ch in plaintext:
        if ch.isalpha():
            p_num = ord(ch.upper()) - 65
            k_num = ord(key[key_index % key_len].upper()) - 65
            c_num = (p_num + k_num) % 26
            ciphertext += chr(c_num + 65)
            key_index += 1
        else:
            ciphertext += ch
    return ciphertext

def decrypt_classic(ciphertext, key):
    plaintext = ""
    key_len = len(key)
    key_index = 0
    
    for ch in ciphertext:
        if ch.isalpha():
            c_num = ord(ch.upper()) - 65
            k_num = ord(key[key_index % key_len].upper()) - 65
            p_num = (c_num - k_num + 26) % 26
            plaintext += chr(p_num + 65)
            key_index += 1
        else:
            plaintext += ch
    return plaintext

# ========== CORRECTED DYNAMIC POLYALPHABETIC ==========
def encrypt_dynamic(plaintext, key):
    ciphertext = ""
    # Start with first key character
    current_key = ord(key[0].upper()) - 65
    
    for ch in plaintext:
        if ch.isalpha():
            p_num = ord(ch.upper()) - 65
            # Encrypt: C_i = (P_i + K_i) mod 26
            c_num = (p_num + current_key) % 26
            cipher_char = chr(c_num + 65)
            ciphertext += cipher_char
            
            # CORRECTED: Dynamic key update: Next Key = (Current Key + Current Cipher) mod 26
            current_key = (current_key + c_num) % 26
        else:
            ciphertext += ch
    
    return ciphertext

def decrypt_dynamic(ciphertext, key):
    plaintext = ""
    # Start with first key character
    current_key = ord(key[0].upper()) - 65
    
    for ch in ciphertext:
        if ch.isalpha():
            c_num = ord(ch.upper()) - 65
            # Decrypt: P_i = (C_i - K_i + 26) mod 26
            p_num = (c_num - current_key + 26) % 26
            plain_char = chr(p_num + 65)
            plaintext += plain_char
            
            # CORRECTED: Dynamic key update (same as encryption): Next Key = (Current Key + Current Cipher) mod 26
            current_key = (current_key + c_num) % 26
        else:
            plaintext += ch
    
    return plaintext

# ========== VERIFICATION FUNCTION ==========
def verify_manual_example():
    """Verify our implementation matches the manual example"""
    plaintext = "ATTACK"
    key = "LEMON"
    
    classic_result = encrypt_classic(plaintext, key)
    dynamic_result = encrypt_dynamic(plaintext, key)
    
    # Step-by-step verification for dynamic cipher
    print("=== VERIFYING MANUAL EXAMPLE ===")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Expected Classic: LXFOPV")
    print(f"Actual Classic: {classic_result}")
    print(f"Classic Match: {classic_result == 'LXFOPV'}")
    print(f"Expected Dynamic: LPEPGU")
    print(f"Actual Dynamic: {dynamic_result}")
    print(f"Dynamic Match: {dynamic_result == 'LPEPGU'}")
    
    # Step-by-step dynamic encryption
    print("\n=== STEP-BY-STEP DYNAMIC ENCRYPTION ===")
    current_key = ord('L') - 65  # 11
    steps = []
    for i, char in enumerate(plaintext):
        p_num = ord(char) - 65
        c_num = (p_num + current_key) % 26
        cipher_char = chr(c_num + 65)
        old_key = current_key
        current_key = (current_key + c_num) % 26
        steps.append(f"Step {i+1}: P={char}({p_num}) + K={chr(old_key+65)}({old_key}) = C={cipher_char}({c_num}) → Next K={chr(current_key+65)}({current_key})")
    
    for step in steps:
        print(step)

# ========== API ROUTES ==========
@app.route("/encrypt_text", methods=["POST"])
def encrypt_text_api():
    data = request.json
    plaintext = data.get("plaintext", "")
    key = data.get("key", "A")
    method = data.get("method", "traditional")

    if method == "traditional":
        ciphertext = encrypt_classic(plaintext, key)
    else:
        ciphertext = encrypt_dynamic(plaintext, key)

    return jsonify({"ciphertext": ciphertext})

@app.route("/decrypt_text", methods=["POST"])
def decrypt_text_api():
    data = request.json
    ciphertext = data.get("ciphertext", "")
    key = data.get("key", "A")
    method = data.get("method", "traditional")

    if method == "traditional":
        plaintext = decrypt_classic(ciphertext, key)
    else:
        plaintext = decrypt_dynamic(ciphertext, key)

    return jsonify({"plaintext": plaintext})

# ========== TEST ROUTES ==========
@app.route("/test_encrypt", methods=["GET"])
def test_encrypt():
    """Test route to verify the encryption matches your manual example"""
    plaintext = "ATTACK"
    key = "LEMON"
    
    classic_result = encrypt_classic(plaintext, key)
    dynamic_result = encrypt_dynamic(plaintext, key)
    
    # Test repeated pattern
    repeated_plaintext = "ATTACK ATTACK"
    classic_repeated = encrypt_classic(repeated_plaintext, key)
    dynamic_repeated = encrypt_dynamic(repeated_plaintext, key)
    
    return jsonify({
        "plaintext": plaintext,
        "key": key,
        "classic_vigenere": classic_result,
        "dynamic_cipher": dynamic_result,
        "expected_classic": "LXFOPV",
        "expected_dynamic": "LPEPGU",
        "classic_correct": classic_result == "LXFOPV",
        "dynamic_correct": dynamic_result == "LPEPGU",
        "repeated_test": {
            "plaintext": repeated_plaintext,
            "classic_result": classic_repeated,
            "dynamic_result": dynamic_repeated,
            "classic_pattern_preserved": classic_repeated == "LXFOPV LXFOPV",
            "dynamic_pattern_preserved": dynamic_repeated != "LPEPGU LPEPGU"
        }
    })

@app.route("/verify_implementation", methods=["GET"])
def verify_implementation():
    """Detailed verification endpoint"""
    verify_manual_example()
    return jsonify({"message": "Check console for verification details"})

@app.route("/")
def home():
    return "Polyalphabetic Cipher Backend is running!"

# ========== MAIN ==========
if __name__ == "__main__":
    # Run verification when starting
    verify_manual_example()
    app.run(debug=True, host='127.0.0.1', port=5000)