// -------------------- Playfair Cipher --------------------
function preparePlayfairKey(key) {
  key = key.toUpperCase().replace(/J/g, "I");
  let seen = new Set();
  let result = "";
  for (let c of key) {
    if (c >= "A" && c <= "Z" && !seen.has(c)) {
      seen.add(c);
      result += c;
    }
  }
  for (let i = 65; i <= 90; i++) {
    let ch = String.fromCharCode(i);
    if (ch == "J") continue;
    if (!seen.has(ch)) {
      result += ch;
      seen.add(ch);
    }
  }
  let matrix = [];
  for (let i = 0; i < 5; i++)
    matrix.push(result.slice(i * 5, (i + 1) * 5).split(""));
  return matrix;
}

function playfairEncryptPair(a, b, matrix) {
  const pos = (ch) => {
    for (let i = 0; i < 5; i++)
      for (let j = 0; j < 5; j++) if (matrix[i][j] == ch) return [i, j];
  };
  let [r1, c1] = pos(a),
    [r2, c2] = pos(b);
  if (r1 == r2) return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5];
  if (c1 == c2) return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2];
  return matrix[r1][c2] + matrix[r2][c1];
}

function playfairDecryptPair(a, b, matrix) {
  const pos = (ch) => {
    for (let i = 0; i < 5; i++)
      for (let j = 0; j < 5; j++) if (matrix[i][j] == ch) return [i, j];
  };
  let [r1, c1] = pos(a),
    [r2, c2] = pos(b);
  if (r1 == r2) return matrix[r1][(c1 + 4) % 5] + matrix[r2][(c2 + 4) % 5];
  if (c1 == c2) return matrix[(r1 + 4) % 5][c1] + matrix[(r2 + 4) % 5][c2];
  return matrix[r1][c2] + matrix[r2][c1];
}

function playfairEncrypt(text, key) {
  text = text
    .toUpperCase()
    .replace(/J/g, "I")
    .replace(/[^A-Z]/g, "");
  if (text.length % 2 != 0) text += "X";
  let matrix = preparePlayfairKey(key);
  let out = "";
  for (let i = 0; i < text.length; i += 2) {
    let a = text[i],
      b = text[i + 1];
    if (a == b) b = "X";
    out += playfairEncryptPair(a, b, matrix);
  }
  return out;
}

function playfairDecrypt(text, key) {
  let matrix = preparePlayfairKey(key);
  let out = "";
  for (let i = 0; i < text.length; i += 2) {
    out += playfairDecryptPair(text[i], text[i + 1], matrix);
  }
  return out;
}

// -------------------- Monoalphabetic Cipher (Caesar Shift) --------------------
function monoEncrypt(text, shift) {
  text = text.toUpperCase().replace(/[^A-Z]/g, "");
  return text
    .split("")
    .map((c) => {
      let code = c.charCodeAt(0) - 65;
      return String.fromCharCode(((code + shift) % 26) + 65);
    })
    .join("");
}

function monoDecrypt(text, shift) {
  text = text.toUpperCase().replace(/[^A-Z]/g, "");
  return text
    .split("")
    .map((c) => {
      let code = c.charCodeAt(0) - 65;
      return String.fromCharCode(((code - shift + 26) % 26) + 65);
    })
    .join("");
}

// -------------------- Odd-Even Split & Mix (Word-by-Word) --------------------
let originalWordsMap = []; // To store original letters including J

function encrypt() {
  let P = document.getElementById("plaintext").value;
  let K1 = document.getElementById("playfairKey").value;
  let shift = parseInt(document.getElementById("monoKey").value);

  if (!P || !K1) {
    alert("Enter plaintext and Playfair key");
    return;
  }

  let words = P.split(" ");
  let encryptedWords = [];
  originalWordsMap = []; // reset mapping

  for (let w of words) {
    let original = w.split(""); // save original letters
    originalWordsMap.push(original);

    let clean = w
      .toUpperCase()
      .replace(/J/g, "I")
      .replace(/[^A-Z]/g, "");
    if (clean.length % 2 != 0) clean += "X";

    let odd = [],
      even = [];
    for (let i = 0; i < clean.length; i++) {
      if (i % 2 == 0) odd.push(clean[i]);
      else even.push(clean[i]);
    }
    even.reverse();

    let C_odd = playfairEncrypt(odd.join(""), K1);
    let C_even = monoEncrypt(even.join(""), shift);

    encryptedWords.push(C_odd + C_even);
  }

  document.getElementById("output").value = encryptedWords.join(" ");
}

function decrypt() {
  let C = document.getElementById("output").value;
  let K1 = document.getElementById("playfairKey").value;
  let shift = parseInt(document.getElementById("monoKey").value);

  if (!C || !K1) {
    alert("Ciphertext and Playfair key required");
    return;
  }

  let words = C.split(" ");
  let decryptedWords = [];

  for (let wi = 0; wi < words.length; wi++) {
    let w = words[wi];
    let original = originalWordsMap[wi]; // original letters including J

    let n = w.length;
    let odd_count = Math.ceil(n / 2);
    let C_odd = w.slice(0, odd_count);
    let C_even = w.slice(odd_count);

    let P_odd = playfairDecrypt(C_odd, K1).split("");
    let P_even_rev = monoDecrypt(C_even, shift).split("");
    let P_even = P_even_rev.reverse();

    let plaintext = [];
    let oi = 0,
      ei = 0;
    for (let i = 0; i < n; i++) {
      if (i % 2 == 0) plaintext.push(P_odd[oi++]);
      else plaintext.push(P_even[ei++]);
    }

    // Remove filler X if added (only if length > original word length and last char is X)
    if (
      plaintext.length > original.length &&
      plaintext[plaintext.length - 1] == "X"
    ) {
      plaintext.pop();
    }

    // Restore original letters like J
    for (let i = 0; i < original.length; i++) {
      plaintext[i] = original[i];
    }

    decryptedWords.push(plaintext.join(""));
  }

  document.getElementById("output").value = decryptedWords.join(" ");
}
