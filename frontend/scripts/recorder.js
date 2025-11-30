/**
 * AudioRecorder - Handles microphone recording and audio capture
 */
class AudioRecorder {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.isRecording = false;
    this.recordingStartTime = null;
    this.recordingDuration = 0;
    this.stream = null;
    this.recordingHistory = this.loadRecordingHistory();
    console.log('✅ AudioRecorder initialized');
  }

  // Initialize microphone access
  async initialize() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });
      console.log('✅ Microphone access granted');
      return true;
    } catch (error) {
      console.error('❌ Microphone error:', error.name);
      if (error.name === 'NotAllowedError') {
        alert('Microphone access denied. Please allow microphone access in browser settings.');
      } else if (error.name === 'NotFoundError') {
        alert('No microphone found. Please connect a microphone.');
      } else {
        alert('Error accessing microphone: ' + error.message);
      }
      return false;
    }
  }

  // Start recording
  async startRecording() {
    if (!this.stream) {
      const initialized = await this.initialize();
      if (!initialized) return false;
    }

    this.audioChunks = [];
    this.mediaRecorder = new MediaRecorder(this.stream);
    
    this.mediaRecorder.ondataavailable = (event) => {
      this.audioChunks.push(event.data);
    };

    this.mediaRecorder.onstop = () => {
      console.log('✅ Recording stopped, processing audio...');
    };

    this.mediaRecorder.start();
    this.isRecording = true;
    this.recordingStartTime = Date.now();
    
    // Auto-stop after 5 seconds
    setTimeout(() => {
      if (this.isRecording) {
        this.stopRecording();
      }
    }, 5000);

    console.log('🎙️ Recording started');
    return true;
  }

  // Stop recording
  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
      this.recordingDuration = Math.round((Date.now() - this.recordingStartTime) / 1000);
      console.log(`✅ Recording stopped after ${this.recordingDuration}s`);
      return true;
    }
    return false;
  }

  // Get audio blob
  getAudioBlob() {
    if (this.audioChunks.length === 0) {
      console.error('❌ No audio data');
      return null;
    }
    const blob = new Blob(this.audioChunks, { type: 'audio/wav' });
    console.log(`✅ Audio blob created: ${(blob.size / 1024).toFixed(2)}KB`);
    return blob;
  }

  // Check if currently recording
  isCurrentlyRecording() {
    return this.isRecording;
  }

  // Get recording duration in seconds
  getRecordingTime() {
    if (this.isRecording) {
      return Math.round((Date.now() - this.recordingStartTime) / 1000);
    }
    return this.recordingDuration;
  }

  // Get audio level for visualization
  getAudioLevel() {
    if (!this.stream) return 0;
    
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const microphone = audioContext.createMediaStreamSource(this.stream);
    microphone.connect(analyser);
    
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);
    
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
    return Math.min(average / 255, 1);
  }

  // Save recording to history
  saveRecordingToHistory(blob) {
    const recording = {
      timestamp: new Date().toLocaleString(),
      size: (blob.size / 1024).toFixed(2) + 'KB',
      duration: this.recordingDuration + 's'
    };
    
    this.recordingHistory.unshift(recording);
    if (this.recordingHistory.length > 5) {
      this.recordingHistory.pop();
    }
    
    localStorage.setItem('recordingHistory', JSON.stringify(this.recordingHistory));
    console.log('💾 Recording saved to history');
  }

  // Load recording history
  loadRecordingHistory() {
    const saved = localStorage.getItem('recordingHistory');
    return saved ? JSON.parse(saved) : [];
  }

  // Get recording history
  getRecordingHistory() {
    return this.recordingHistory;
  }

  // Stop all streams on cleanup
  stopAllStreams() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  }
}

// Export
window.AudioRecorder = AudioRecorder;
console.log('📦 recorder.js loaded');
