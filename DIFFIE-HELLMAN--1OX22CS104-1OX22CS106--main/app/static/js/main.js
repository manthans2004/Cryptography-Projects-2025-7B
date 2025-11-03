function getParams() {
  const p = document.getElementById('p').value;
  const g = document.getElementById('g').value;
  const a = document.getElementById('a').value;
  const b = document.getElementById('b').value;
  return { p: Number(p), g: Number(g), a: Number(a), b: Number(b) };
}

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Request failed');
  return data;
}

function showComputeResult(outEl, data) {
  outEl.textContent = [
    `Alice public key A = g^a mod p = ${data.A}`,
    `Bob public key B = g^b mod p = ${data.B}`,
    `Alice shared s1 = B^a mod p = ${data.s1}`,
    `Bob shared s2 = A^b mod p = ${data.s2}`,
    data.match ? 'Match: s1 == s2 ✅' : 'Mismatch: s1 != s2 ❌'
  ].join('\n');
}

function showCryptoResult(outEl, title, obj) {
  outEl.textContent = [
    title,
    `Ciphertext: ${obj.ciphertext || ''}`,
    obj.plaintext !== undefined ? `Plaintext: ${obj.plaintext}` : '',
    obj.shared_secret !== undefined ? `(Shared secret used: ${obj.shared_secret})` : ''
  ].filter(Boolean).join('\n');
}

async function compute() {
  const out = document.getElementById('compute-output');
  out.textContent = 'Computing...';
  try {
    const params = getParams();
    const data = await postJSON('/api/compute', params);
    showComputeResult(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
}

async function encryptAlice() {
  const out = document.getElementById('alice-crypto-output');
  out.textContent = 'Encrypting...';
  try {
    const params = getParams();
    const message = document.getElementById('msg-alice').value;
    const data = await postJSON('/api/encrypt', { ...params, sender: 'alice', message });
    showCryptoResult(out, 'Alice -> Bob', data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
}

async function decryptAliceAsBob() {
  const out = document.getElementById('alice-crypto-output');
  const lines = out.textContent.split('\n');
  const ctLine = lines.find(l => l.startsWith('Ciphertext: '));
  if (!ctLine) { out.textContent = 'Please encrypt first.'; return; }
  const ciphertext = ctLine.replace('Ciphertext: ', '').trim();
  out.textContent = 'Decrypting...';
  try {
    const params = getParams();
    const data = await postJSON('/api/decrypt', { ...params, recipient: 'bob', ciphertext });
    showCryptoResult(out, 'Alice -> Bob (decrypted by Bob)', { ...data, ciphertext });
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
}

async function encryptBob() {
  const out = document.getElementById('bob-crypto-output');
  out.textContent = 'Encrypting...';
  try {
    const params = getParams();
    const message = document.getElementById('msg-bob').value;
    const data = await postJSON('/api/encrypt', { ...params, sender: 'bob', message });
    showCryptoResult(out, 'Bob -> Alice', data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
}

async function decryptBobAsAlice() {
  const out = document.getElementById('bob-crypto-output');
  const lines = out.textContent.split('\n');
  const ctLine = lines.find(l => l.startsWith('Ciphertext: '));
  if (!ctLine) { out.textContent = 'Please encrypt first.'; return; }
  const ciphertext = ctLine.replace('Ciphertext: ', '').trim();
  out.textContent = 'Decrypting...';
  try {
    const params = getParams();
    const data = await postJSON('/api/decrypt', { ...params, recipient: 'alice', ciphertext });
    showCryptoResult(out, 'Bob -> Alice (decrypted by Alice)', { ...data, ciphertext });
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-compute').addEventListener('click', compute);
  document.getElementById('btn-encrypt-alice').addEventListener('click', encryptAlice);
  document.getElementById('btn-decrypt-alice').addEventListener('click', decryptAliceAsBob);
  document.getElementById('btn-encrypt-bob').addEventListener('click', encryptBob);
  document.getElementById('btn-decrypt-bob').addEventListener('click', decryptBobAsAlice);
});
