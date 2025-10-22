// Reverse Cipher - simple client-side implementation
const input = document.getElementById('inputText');
const output = document.getElementById('outputText');
const reverseBtn = document.getElementById('reverseBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const liveToggle = document.getElementById('liveToggle');

function reverseString(s){
  // Basic reversal by Unicode code units. This works for most use-cases.
  return Array.from(s).reverse().join('');
}

function doReverse(){
  output.value = reverseString(input.value);
}

reverseBtn.addEventListener('click', doReverse);
copyBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(output.value);
    copyBtn.textContent = 'Copied!';
    setTimeout(()=> copyBtn.textContent = 'Copy', 1200);
  } catch (e) {
    alert('Copy failed — try manually selecting the output and copying.');
  }
});

downloadBtn.addEventListener('click', () => {
  const blob = new Blob([output.value], {type: 'text/plain;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const filename = 'reversed.txt';
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

// Live toggle
liveToggle.addEventListener('input', (e) => {
  if (e.target.checked) doReverse();
});

input.addEventListener('input', () => {
  if (liveToggle.checked) doReverse();
});

// Keyboard shortcut: Ctrl/Cmd+Enter to reverse
input.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    doReverse();
  }
});

// Initialize with sample text
input.value = "Hello, world! — नमस्ते दुनिया";
doReverse();
