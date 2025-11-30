/**
 * Accent Detection API Client
 * Handles communication between frontend and backend for accent/dialect detection
 */
class AccentAPI {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    this.accentData = this.getAccentDatabase();
    console.log('🎯 AccentAPI initialized with baseURL:', this.baseURL || 'relative path');
  }

  /**
   * Get the comprehensive accent and cuisine database
   */
  getAccentDatabase() {
    return {
      'Mumbai': {
        language: 'Marathi',
        region: 'Mumbai, Maharashtra',
        characteristics: ['Nasal vowels', 'Retroflex consonants', 'Rhythm variation'],
        confidence: 0.92,
        cuisine: {
          name: 'Marathi Cuisine',
          description: 'The soul of Marathi food lies in its simplicity and the generous use of peanuts and sesame seeds. Dishes are often milder than other Indian cuisines, focusing on the natural flavors of ingredients.',
          dishes: ['Misal Pav', 'Poha', 'Bhakri', 'Amti', 'Puran Poli', 'Vada Pav']
        }
      },
      'Delhi': {
        language: 'Hindi (North Indian)',
        region: 'Delhi, North India',
        characteristics: ['Clear pronunciation', 'Standard Hindi patterns', 'Minimal nasalization'],
        confidence: 0.88,
        cuisine: {
          name: 'Mughlai Cuisine',
          description: 'A grand blend of Central Asian and Indian flavors, Mughlai cuisine is known for its rich, aromatic dishes. Biryani, tandoori preparations, and creamy gravies are the hallmarks of this imperial culinary tradition.',
          dishes: ['Butter Chicken', 'Biryani', 'Tandoori Paneer', 'Seekh Kebab', 'Shahi Tukda', 'Nihari']
        }
      },
      'Bangalore': {
        language: 'Kannada',
        region: 'Bangalore, Karnataka',
        characteristics: ['Velar consonants', 'Open vowel patterns', 'Soft ending'],
        confidence: 0.85,
        cuisine: {
          name: 'Kannada Cuisine',
          description: 'Rooted in the agricultural abundance of Karnataka, Kannada cuisine celebrates the simplicity of rice, legumes, and spices. The food is hearty, flavorful, and deeply connected to the seasons.',
          dishes: ['Bisi Bele Bath', 'Rasam', 'Idli', 'Uttapam', 'Jaggery Cookies', 'Payasam']
        }
      },
      'Kolkata': {
        language: 'Bengali',
        region: 'Kolkata, West Bengal',
        characteristics: ['Palatalized sounds', 'Aspirated consonants', 'Musical intonation'],
        confidence: 0.90,
        cuisine: {
          name: 'Bengali Cuisine',
          description: 'Bengali food is a celebration of rice, fish, and mustard oil. Known for its subtle flavors and the perfect balance of sweet, salty, and spicy, Bengal\'s cuisine is a treasure trove of delicate preparations.',
          dishes: ['Fish Curry', 'Sandesh', 'Luchi', 'Rosogolla', 'Parathas', 'Shrikhandi']
        }
      },
      'Chennai': {
        language: 'Tamil',
        region: 'Chennai, Tamil Nadu',
        characteristics: ['Retroflex dominance', 'Glottal stops', 'Rapid speech patterns'],
        confidence: 0.87,
        cuisine: {
          name: 'Tamil Cuisine',
          description: 'Deeply rooted in tradition, Tamil cuisine is a blend of flavors from the Chola, Pandya, and Chera kingdoms. Rice, coconut, and tamarind form the base of most dishes, creating bold and distinctive flavors.',
          dishes: ['Dosa', 'Sambar', 'Vadai', 'Pongal', 'Appalam', 'Idiyappam']
        }
      },
      'Hyderabad': {
        language: 'Telugu/Urdu',
        region: 'Hyderabad, Telangana',
        characteristics: ['Velar dominance', 'Rhotic pronunciation', 'Melodic rhythm'],
        confidence: 0.84,
        cuisine: {
          name: 'Hyderabadi Cuisine',
          description: 'Born from the fusion of Mughal and South Indian traditions, Hyderabadi cuisine is famous for its biryani and halim. The use of spices is bold and the cooking techniques are traditional and time-honored.',
          dishes: ['Hyderabadi Biryani', 'Halim', 'Kebab', 'Khichdi', 'Naan', 'Phirni']
        }
      }
    };
  }

  /**
   * Send audio to backend for analysis
   */
  async sendForAnalysis(audioData) {
    try {
      const blob = new Blob([audioData], { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', blob, 'recording.webm');
      // Use explicit backend URL when provided, otherwise default to localhost
      const endpoint = (this.baseURL && this.baseURL !== '') ? `${this.baseURL}/predict` : 'http://localhost:8000/predict';
      console.log('📡 Sending audio to:', endpoint);
      console.log('   Blob size:', (blob.size / 1024).toFixed(2) + 'KB');
      
      // Use AbortController to enforce a fetch timeout in browsers
      const controller = new AbortController();
      const timeoutMs = 30000; // 30s
      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
      
      let response;
      try {
        response = await fetch(endpoint, {
          method: 'POST',
          body: formData,
          signal: controller.signal
        });
      } finally {
        clearTimeout(timeoutId);
      }
      
      console.log('📡 Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.warn(`⚠️ HTTP error! status: ${response.status}, message: ${errorText}`);
        throw new Error(`Backend error: ${response.status} - ${errorText}`);
      }
      
      const result = await response.json();
      console.log('✅ Backend response received:', result);

      // Surface the raw backend JSON for quick debugging in DOM if a debug area exists
      try {
        const dbg = document.getElementById('backendDebug');
        if (dbg) dbg.textContent = JSON.stringify(result, null, 2);
      } catch (e) {}
      
      return {
        region: result.state ? this.getRegionNameFromState(result.state) : 'Unknown',
        language: result.language || this.getLanguageFromState(result.state),
        confidence: (typeof result.confidence !== 'undefined') ? result.confidence : 0.0,
        characteristics: this.getCharacteristicsFromState(result.state),
        duration_ms: result.duration_ms || 0,
        cuisines: result.cuisines || [],
        state: result.state
      };
    } catch (error) {
      console.error('❌ Error sending audio for analysis:', error && error.message ? error.message : error);
      console.error('   Endpoint attempted:', (this.baseURL && this.baseURL !== '') ? `${this.baseURL}/predict` : 'http://localhost:8000/predict');
      // Surface error in a debug area if present
      try {
        const dbg = document.getElementById('backendDebug');
        if (dbg) dbg.textContent = `ERROR: ${error}`;
      } catch (e) {}
      throw error;
    }
  }

  /**
   * Send audio for preprocessing and return summary + preview WAV (base64)
   */
  async sendForPreprocess(audioData) {
    try {
      const blob = new Blob([audioData], { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('file', blob, 'recording.webm');

      const endpoint = this.baseURL ? `${this.baseURL}/preprocess/` : '/preprocess/';
      console.log('🔬 Sending audio for preprocessing to:', endpoint);

      const controller = new AbortController();
      const timeoutMs = 20000; // 20s for preprocessing
      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
      let response;
      try {
        response = await fetch(endpoint, { method: 'POST', body: formData, signal: controller.signal });
      } finally {
        clearTimeout(timeoutId);
      }

      if (!response.ok) {
        const err = await response.text();
        throw new Error(`Preprocess failed: ${response.status} ${err}`);
      }

      const result = await response.json();
      console.log('🔬 Preprocess result:', result);
      return result;
    } catch (error) {
      console.error('❌ Preprocess error:', error.message);
      throw error;
    }
  }

  /**
   * Get mock prediction for demo/testing
   */
  getMockPrediction() {
    const regions = Object.keys(this.accentData);
    const randomRegion = regions[Math.floor(Math.random() * regions.length)];
    const data = this.accentData[randomRegion];
    
    return {
      region: randomRegion,
      language: data.language,
      confidence: (data.confidence * (0.85 + Math.random() * 0.15)).toFixed(2),
      characteristics: data.characteristics
    };
  }

  /**
   * Get cuisine information by region
   */
  getCuisineByRegion(region) {
    const data = this.accentData[region];
    return data ? data.cuisine : null;
  }

  /**
   * Get all accent data
   */
  getAllAccentData() {
    return this.accentData;
  }

  /**
   * Get specific region data
   */
  getRegionData(region) {
    return this.accentData[region] || null;
  }

  /**
   * Get list of all regions
   */
  getRegions() {
    return Object.keys(this.accentData);
  }

  /**
   * Fetch dish information from backend
   */
  async getDishInfo(region) {
    try {
      const response = await fetch(`${this.baseURL}/dish-info?region=${encodeURIComponent(region)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching dish info:', error);
      return this.getCuisineByRegion(region);
    }
  }

  /**
   * Set custom base URL
   */
  setBaseURL(url) {
    this.baseURL = url;
  }

  /**
   * Map backend state to region name
   */
  getRegionNameFromState(state) {
    const stateMap = {
      'andhrapradesh': 'Hyderabad',
      'gujarath': 'Ahmedabad',
      'kerala': 'Kochi',
      'karnataka': 'Bangalore',
      'jharkhand': 'Ranchi',
      'tamilnadu': 'Chennai'
    };
    return stateMap[state] || 'Unknown';
  }

  /**
   * Get language from state
   */
  getLanguageFromState(state) {
    const languageMap = {
      'andhrapradesh': 'Telugu/Urdu',
      'gujarath': 'Kannada',
      'kerala': 'Kannada',
      'karnataka': 'Kannada',
      'jharkhand': 'Hindi (North Indian)',
      'tamilnadu': 'Tamil'
    };
    return languageMap[state] || 'Kannada';
  }

  /**
   * Get characteristics from state
   */
  getCharacteristicsFromState(state) {
    const characteristicsMap = {
      'andhrapradesh': ['Velar dominance', 'Rhotic pronunciation', 'Melodic rhythm'],
      'gujarath': ['Retroflex consonants', 'Open vowel patterns', 'Soft ending'],
      'kerala': ['Retroflex consonants', 'Open vowel patterns', 'Soft ending'],
      'karnataka': ['Retroflex consonants', 'Open vowel patterns', 'Soft ending'],
      'jharkhand': ['Clear pronunciation', 'Standard Hindi patterns', 'Minimal nasalization'],
      'tamilnadu': ['Retroflex dominance', 'Glottal stops', 'Rapid speech patterns']
    };
    return characteristicsMap[state] || ['Clear pronunciation', 'Unique patterns', 'Regional influence'];
  }
}

// Export for use in other modules
window.AccentAPI = AccentAPI;
console.log('📦 api.js loaded');
