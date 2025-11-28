/**
 * API Client
 */
import axios from 'axios';

const BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

// Add request interceptor
apiClient.interceptors.request.use(
  config => {
    // Add any authentication headers if needed
    return config;
  },
  error => Promise.reject(error)
);

// Add response interceptor
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default apiClient;
