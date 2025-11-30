/**
 * UI Management Module
 * Handles page navigation, state management, and event handlers
 */

class UIManager {
  constructor() {
    this.currentPage = 'home'; // 'home' or 'detector'
    this.recorder = null;
    this.api = null;
    this.currentPrediction = null;
    
    console.log('UIManager constructor called');
    console.log('All templates in document:', Array.from(document.querySelectorAll('template')).map(t => ({ id: t.id, length: t.innerHTML.length })));
    
    this.appRoot = document.getElementById('appRoot');
    console.log('appRoot element:', this.appRoot);
    
    if (!this.appRoot) {
      console.error('appRoot element not found!');
      return;
    }
    
    // Check if required classes are available
    if (typeof AudioRecorder === 'undefined') {
      console.error('AudioRecorder not loaded');
      return;
    }
    if (typeof AccentAPI === 'undefined') {
      console.error('AccentAPI not loaded');
      return;
    }
    
    try {
      this.recorder = new AudioRecorder();
        // Determine backend URL based on environment
        const backendUrl = (window.BACKEND_URL && window.BACKEND_URL !== '') ? window.BACKEND_URL : (window.location.hostname === 'localhost' 
          ? 'http://localhost:8000' 
          : `http://${window.location.hostname === '127.0.0.1' ? 'localhost' : 'backend'}:8000`);
        this.api = new AccentAPI(backendUrl);
      console.log('✅ AudioRecorder and AccentAPI initialized');
        console.log('✅ AudioRecorder and AccentAPI initialized with URL:', backendUrl);
        // Start preloading cuisine images (non-blocking)
        this.preloadCuisineImages();
    } catch (error) {
      console.error('Error initializing modules:', error);
      return;
    }
    
    this.initializeEventListeners();
    this.renderPage();
  }

  async preloadCuisineImages() {
    // Loads manifest from /images/manifest.json and preloads images into memory.
    this._imageCache = {}; // filename -> { url, dataUrl (optional) }
    const origin = window.location.origin;
    const ts = Date.now();

    try {
      const manifestUrl = origin + '/images/manifest.json?v=' + ts;
      console.log('[Preloader] fetching manifest', manifestUrl);
      const res = await fetch(manifestUrl, { cache: 'no-store' });
      if (!res.ok) {
        console.warn('[Preloader] manifest fetch failed', res.status);
        return;
      }
      const files = await res.json();
      // Preload concurrently, but don't block UI
      await Promise.all(files.map(async (fname) => {
        const url = origin + '/images/' + fname + '?v=' + ts;
        try {
          await this._loadImageToCache(fname, url);
          console.log('[Preloader] cached', fname);
        } catch (err) {
          // fallback: try fetching as blob and convert to dataURL
          try {
            const blobRes = await fetch(url, { cache: 'no-store' });
            if (blobRes.ok) {
              const blob = await blobRes.blob();
              const dataUrl = await new Promise((resolve) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = () => resolve(null);
                reader.readAsDataURL(blob);
              });
              if (dataUrl) {
                this._imageCache[fname] = { url, dataUrl };
                console.log('[Preloader] blob->dataURL cached', fname);
              }
            }
          } catch (e) {
            console.warn('[Preloader] failed fallback for', fname, e);
          }
        }
      }));
      console.log('[Preloader] done');
    } catch (err) {
      console.warn('[Preloader] error', err);
    }
  }

  _loadImageToCache(fname, url) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      // Force fetch fresh copy
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        this._imageCache[fname] = { url };
        resolve(true);
      };
      img.onerror = (e) => {
        reject(e);
      };
      img.src = url;
    });
  }

  initializeEventListeners() {
    // Will be set after rendering
  }

  renderPage() {
    if (this.currentPage === 'home') {
      this.renderHomePage();
    } else if (this.currentPage === 'detector') {
      this.renderDetectorPage();
    }
  }

  renderHomePage() {
    const template = document.getElementById('homePageTemplate');
    if (!template) {
      console.error('homePageTemplate not found');
      console.log('Available templates:', Array.from(document.querySelectorAll('template')).map(t => t.id));
      return;
    }
    console.log('Rendering home page...');
    // Use template cloning instead of innerHTML to preserve templates
    this.appRoot.innerHTML = '';
    const content = template.content.cloneNode(true);
    this.appRoot.appendChild(content);
    
    // Add event listeners to home page buttons with error handling
    console.log('Looking for buttons on home page...');
    const getStartedBtn = this.appRoot.querySelector('#getStartedBtn');
    const headerListenBtn = this.appRoot.querySelector('#headerListenBtn');

    console.log('getStartedBtn:', getStartedBtn);
    console.log('headerListenBtn:', headerListenBtn);
    console.log('All buttons on page:', this.appRoot.querySelectorAll('button'));
    
    if (getStartedBtn) {
      console.log('Attaching click listener to getStartedBtn');
      getStartedBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Get Started clicked');
        this.goToDetector();
      });
    } else {
      console.warn('❌ getStartedBtn not found');
    }
    
    if (headerListenBtn) {
      console.log('Attaching click listener to headerListenBtn');
      headerListenBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Header Listen clicked');
        this.goToDetector();
      });
    } else {
      console.warn('❌ headerListenBtn not found');
    }
    
    // Create animated region badges
    this.renderRegionBadges();
  }

  renderRegionBadges() {
    const regionBadgesContainer = this.appRoot.querySelector('#regionBadges');
    const regions = this.api.getRegions();
    
    const containerSize = 400; // Container size
    const center = containerSize / 2;
    const radius = 120;
    const angleStep = (360 / regions.length);
    
    regions.forEach((region, index) => {
      const angle = (angleStep * index - 90) * (Math.PI / 180);
      const x = center + radius * Math.cos(angle);
      const y = center + radius * Math.sin(angle);
      
      const badge = document.createElement('div');
      badge.className = 'region-badge'; // Removed animate-orbit - stops animation
      badge.style.left = x + 'px';
      badge.style.top = y + 'px';
      badge.innerHTML = region;
      badge.title = `${region} - ${this.api.getRegionData(region).language}`;
      
      regionBadgesContainer.appendChild(badge);
    });
  }

  renderDetectorPage() {
    const template = document.getElementById('accentDetectorTemplate');
    if (!template) {
      console.error('accentDetectorTemplate not found');
      console.log('Available templates:', Array.from(document.querySelectorAll('template')).map(t => t.id));
      return;
    }

    console.log('Rendering detector page...');
    // Clone template content to avoid removing template elements
    this.appRoot.innerHTML = '';
    const content = template.content.cloneNode(true);
    this.appRoot.appendChild(content);
    
    // Set up event listeners with error handling
    console.log('Looking for buttons on detector page...');
    const micBtn = this.appRoot.querySelector('#micBtn');
    const backBtn = this.appRoot.querySelector('#backBtn');
    const tryAgainBtn = this.appRoot.querySelector('#tryAgainBtn');
    const backHomeBtn = this.appRoot.querySelector('#backHomeBtn');
    
    console.log('micBtn:', micBtn);
    console.log('backBtn:', backBtn);
    console.log('tryAgainBtn:', tryAgainBtn);
    console.log('backHomeBtn:', backHomeBtn);
    
    if (micBtn) {
      console.log('Attaching click listener to micBtn');
      micBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Mic button clicked');
        this.handleMicButtonClick();
      });
    } else {
      console.warn('❌ micBtn not found');
    }
    
    if (backBtn) {
      console.log('Attaching click listener to backBtn');
      backBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Back button clicked');
        this.goToHome();
      });
    } else {
      console.warn('❌ backBtn not found');
    }
    
    if (tryAgainBtn) {
      console.log('Attaching click listener to tryAgainBtn');
      tryAgainBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Try Again button clicked');
        this.resetDetector();
      });
    } else {
      console.warn('❌ tryAgainBtn not found');
    }
    
    if (backHomeBtn) {
      console.log('Attaching click listener to backHomeBtn');
      backHomeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        console.log('✅ Back to Home button clicked');
        this.goToHome();
      });
    } else {
      console.warn('❌ backHomeBtn not found');
    }
  }

  async handleMicButtonClick() {
    const micBtn = document.getElementById('micBtn');
    const statusText = document.getElementById('statusText');
    const recordingInfo = document.getElementById('recordingInfo');
    
    if (!micBtn || !statusText || !recordingInfo) {
      console.error('❌ Required elements not found for recording');
      return;
    }
    
    if (!this.recorder.isCurrentlyRecording()) {
      // Start recording
      console.log('🎙️ Starting recording...');
      const initialized = await this.recorder.initialize();
      if (!initialized) {
        alert('Error: Could not access microphone. Please check permissions.');
        console.error('❌ Failed to initialize recorder');
        return;
      }
      
      const started = await this.recorder.startRecording();
      if (started) {
        console.log('✅ Recording started');
        micBtn.classList.add('mic-recording', 'mic-processing');
        micBtn.classList.remove('hover:bg-orange-600');
        statusText.textContent = 'Recording...';
        recordingInfo.classList.remove('hidden');
        
        // Update audio level visualization
        this.updateAudioLevel();
      } else {
        console.error('❌ Failed to start recording');
        alert('Failed to start recording. Please try again.');
      }
    } else {
      // Stop recording
      console.log('⏹️ Stopping recording...');
      this.recorder.stopRecording();
      micBtn.classList.remove('mic-recording', 'mic-processing');
      micBtn.classList.add('hover:bg-orange-600');
      statusText.textContent = 'Processing...';
      recordingInfo.classList.add('hidden');
      
      console.log('⏳ Processing audio, waiting for backend response...');
      
      // Add delay to ensure mediaRecorder finishes writing chunks
      await new Promise(resolve => setTimeout(resolve, 200));
      
      // Show results after processing
      try {
        // 1) Show the recorded audio (playback is already available)
        // 2) Send for preprocessing, display summary, then send for final analysis
        const blob = this.recorder.getAudioBlob();
        if (!blob) {
          throw new Error('No audio blob available after recording');
        }
        
        const arrayBuffer = await blob.arrayBuffer();
        try {
          const pre = await this.api.sendForPreprocess(arrayBuffer);
          console.log('Preprocess summary:', pre);
          // display minimal preprocess info
          const preprocessInfo = document.getElementById('preprocessInfo');
          if (preprocessInfo) {
            preprocessInfo.classList.remove('hidden');
            preprocessInfo.textContent = `Preprocessed: ${pre.num_windows} windows, ${pre.num_segments} segments`;
          }
        } catch (preErr) {
          console.warn('Preprocess failed, continuing to prediction', preErr);
        }

        // Now run the analysis/prediction as before
        await this.showResults();
      } catch (error) {
        console.error('❌ Error during processing:', error);
        alert('Error processing audio: ' + error.message);
        this.resetDetector();
      }
    }
  }

  updateAudioLevel() {
    if (!this.recorder.isCurrentlyRecording()) return;
    
    const level = this.recorder.getAudioLevel();
    const micBtn = document.getElementById('micBtn');
    
    // Scale the button based on audio level
    const scale = 1 + level * 0.2;
    micBtn.style.transform = `scale(${scale})`;
    
    requestAnimationFrame(() => this.updateAudioLevel());
  }

  async showResults() {
    const audioBlob = this.recorder.getAudioBlob();
    if (!audioBlob) {
      console.error('❌ Failed to get audio blob');
      alert('Error: No audio data recorded. Please try recording again.');
      this.resetDetector();
      return;
    }
    
    console.log('✅ Audio blob obtained:', (audioBlob.size / 1024).toFixed(2) + 'KB');
    const startTime = Date.now();
    
    try {
      // Convert blob to array buffer for sending
      const arrayBuffer = await audioBlob.arrayBuffer();
      console.log('✅ Audio blob converted to arrayBuffer');
      
      // Send audio to backend for analysis
      this.currentPrediction = await this.api.sendForAnalysis(arrayBuffer);
    } catch (arrayBufferError) {
      console.error('❌ Error converting blob to arrayBuffer:', arrayBufferError);
      alert('Error processing audio. Please try again.');
      this.resetDetector();
      return;
    }
    
    // Add processing time
    if (this.currentPrediction) {
      this.currentPrediction.processingTime = Date.now() - startTime;
      console.log('✅ Processing complete:', this.currentPrediction);
    }
    
    // Update UI with results
    this.displayResults();
  }

  displayResults() {
    if (!this.currentPrediction) {
      console.error('❌ No prediction data available');
      alert('Error: Could not process the recording. Please try again.');
      this.resetDetector();
      return;
    }
    
    console.log('📊 Displaying results:', this.currentPrediction);
    
    const recordingInterface = document.getElementById('recordingInterface');
    const resultsInterface = document.getElementById('resultsInterface');
    
    if (!recordingInterface || !resultsInterface) {
      console.error('❌ Result interface elements not found');
      return;
    }
    
    recordingInterface.classList.add('hidden');
    resultsInterface.classList.remove('hidden');
    
    // Update result fields
    const prediction = this.currentPrediction;
    
    const resultLanguage = document.getElementById('resultLanguage');
    const resultConfidence = document.getElementById('resultConfidence');
    const resultRegion = document.getElementById('resultRegion');
    const resultProcessingTime = document.getElementById('resultProcessingTime');
    
    if (resultLanguage) resultLanguage.textContent = prediction.language || '-';
    if (resultConfidence) resultConfidence.textContent = Math.round((prediction.confidence || 0) * 100) + '%';
    if (resultRegion) resultRegion.textContent = prediction.region || '-';
    if (resultProcessingTime) {
      const timeMs = prediction.duration_ms || prediction.processingTime || 0;
      resultProcessingTime.textContent = timeMs + 'ms';
    }
    
    console.log('✅ Updated basic results');
    
    // Update characteristics tags
    const characteristicsTags = document.getElementById('characteristicsTags');
    if (characteristicsTags) {
      characteristicsTags.innerHTML = (prediction.characteristics || [])
        .map(char => `<span class="bg-[#3A2618] text-[#FFF8E7] px-4 py-1 rounded-full text-sm border border-orange-500/30">${char}</span>`)
        .join('');
      console.log('✅ Updated characteristics');
    }
    
    // Update cuisine information with new grid layout
    const cuisines = prediction.cuisines || [];
    const cuisineGrid = document.getElementById('cuisineGrid');
    
    if (cuisineGrid && cuisines.length > 0) {
      // Build grid using DOM methods to avoid HTML-escaping issues with large data URIs
      cuisineGrid.innerHTML = '';
      const origin = window.location.origin;
      const ts = Date.now();

      cuisines.forEach((cuisine, idx) => {
        const card = document.createElement('div');
        card.className = 'cuisine-card';

        // Image container
        if (cuisine.image) {
          let src = cuisine.image;
          const imgDiv = document.createElement('div');
          imgDiv.className = 'cuisine-img';
          imgDiv.setAttribute('aria-hidden', 'true');

          try {
            if (typeof src === 'string' && src.startsWith('data:')) {
              // Directly set backgroundImage from data URI
              imgDiv.style.backgroundImage = `url("${src}")`;
            } else {
              // Non-data URI: try cache or absolute URL
              let filename = null;
              if (src && src.startsWith('/')) filename = src.split('/').pop();
              if (filename && this._imageCache && this._imageCache[filename]) {
                const entry = this._imageCache[filename];
                const useUrl = (entry.dataUrl) ? entry.dataUrl : entry.url;
                imgDiv.style.backgroundImage = `url("${useUrl}")`;
              } else {
                if (src && src.startsWith('/')) src = origin + src;
                if (src) src = src + (src.includes('?') ? '&' : '?') + 'v=' + ts;
                imgDiv.style.backgroundImage = `url("${src}")`;
              }
            }
          } catch (e) {
            console.error('[Cuisine Image] Error setting image for', cuisine.name, e);
          }

          card.appendChild(imgDiv);
        }

        const h3 = document.createElement('h3');
        h3.textContent = cuisine.name || '';
        const priceP = document.createElement('p');
        priceP.className = 'price';
        priceP.textContent = cuisine.price || '₹-';
        const descP = document.createElement('p');
        descP.className = 'description';
        descP.textContent = cuisine.description || '';

        card.appendChild(h3);
        card.appendChild(priceP);
        card.appendChild(descP);

        cuisineGrid.appendChild(card);
      });

      console.log('✅ Updated cuisine grid (DOM) with ' + cuisines.length + ' items');
    } else {
      console.warn('⚠️ No cuisine data found for grid');
    }
    
    // Scroll to results
    setTimeout(() => {
      const resultsInterface = document.getElementById('resultsInterface');
      if (resultsInterface) {
        resultsInterface.scrollIntoView({ behavior: 'smooth' });
        console.log('✅ Scrolled to results');
      }
    }, 100);
  }

  resetDetector() {
    this.renderDetectorPage();
    document.getElementById('recordingInterface').classList.remove('hidden');
    document.getElementById('resultsInterface').classList.add('hidden');
  }

  goToDetector() {
    this.currentPage = 'detector';
    this.renderPage();
  }

  goToHome() {
    this.currentPage = 'home';
    this.renderPage();
  }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded fired');
  console.log('Document ready state:', document.readyState);
  
  // Wait a tiny bit for templates to be fully parsed
  setTimeout(() => {
    console.log('Initializing UIManager...');
    window.uiManager = new UIManager();
    console.log('UIManager initialized');
  }, 100);
});

// Also initialize on document ready if it fires after DOMContentLoaded
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  console.log('Document already interactive/complete, initializing...');
  setTimeout(() => {
    if (!window.uiManager) {
      console.log('Initializing UIManager (delayed)...');
      window.uiManager = new UIManager();
    }
  }, 100);
}

// Export for use in console/debugging
window.UIManager = UIManager;
