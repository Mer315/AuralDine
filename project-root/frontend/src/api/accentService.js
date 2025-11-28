/**
 * Accent Service
 */
import apiClient from './apiClient';
import FormData from 'form-data';

export const accentService = {
  async predictAccent(audioUri) {
    try {
      const formData = new FormData();
      formData.append('file', {
        uri: audioUri,
        type: 'audio/wav',
        name: 'recording.wav',
      });

      const response = await apiClient.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response;
    } catch (error) {
      console.error('Error predicting accent:', error);
      throw error;
    }
  },

  async checkHealth() {
    try {
      const response = await apiClient.get('/health');
      return response;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },
};
