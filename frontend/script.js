let mediaRecorder;
let audioChunks = [];
let audioBlob = null;

// Backend URL - works both locally and in Docker
const BACKEND_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'http://native-language-backend:8000';

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const submitBtn = document.getElementById('submitBtn');
const audioPlayback = document.getElementById('audioPlayback');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMsg = document.getElementById('errorMsg');
const resultSection = document.getElementById('resultSection');
const stateResult = document.getElementById('stateResult');
const cuisineCards = document.getElementById('cuisineCards');

recordBtn.onclick = async () => {
  errorMsg.classList.add('d-none');
  resultSection.style.display = 'none';
  audioPlayback.innerHTML = '';
  audioBlob = null;
  submitBtn.disabled = true;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = () => {
      audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const audioUrl = URL.createObjectURL(audioBlob);
      audioPlayback.innerHTML = `
        <audio controls src="${audioUrl}" class="w-100"></audio>
      `;
      submitBtn.disabled = false;
    };
    mediaRecorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;
  } catch (err) {
    errorMsg.textContent = 'Microphone access denied or not available.';
    errorMsg.classList.remove('d-none');
  }
};

stopBtn.onclick = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    recordBtn.disabled = false;
    stopBtn.disabled = true;
  }
};

submitBtn.onclick = async () => {
  if (!audioBlob) return;
  loadingSpinner.style.display = 'block';
  errorMsg.classList.add('d-none');
  resultSection.style.display = 'none';

  const formData = new FormData();
  formData.append('file', audioBlob, 'audio.webm');

  try {
    const response = await fetch(`${BACKEND_URL}/predict/`, {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Backend error: ${response.status}`);
    }
    const data = await response.json();

    // Display result
    stateResult.innerHTML = `<strong>State:</strong> ${data.state} <strong>(Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%)`;
    cuisineCards.innerHTML = '';
    if (data.cuisines && Array.isArray(data.cuisines) && data.cuisines.length > 0) {
      data.cuisines.forEach(cuisine => {
        cuisineCards.innerHTML += `
          <div class="col-md-6">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">${cuisine.name}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${cuisine.price}</h6>
                <p class="card-text">${cuisine.description}</p>
              </div>
            </div>
          </div>
        `;
      });
    } else {
      cuisineCards.innerHTML = '<div class="col-12"><p>No cuisines found for this state.</p></div>';
    }
    resultSection.style.display = 'block';
  } catch (err) {
    errorMsg.textContent = `Error: ${err.message}`;
    errorMsg.classList.remove('d-none');
  } finally {
    loadingSpinner.style.display = 'none';
  }
};
