import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const { response } = error;
    
    // Handle error responses
    if (response) {
      // Handle 401 Unauthorized - Token expired or invalid
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
        toast.error('Your session has expired. Please log in again.');
      }
      
      // Handle 403 Forbidden
      if (response.status === 403) {
        toast.error('You do not have permission to perform this action.');
      }
      
      // Handle 500 Internal Server Error
      if (response.status >= 500) {
        toast.error('Server error. Please try again later.');
      }
      
      // Handle validation errors (422)
      if (response.status === 422) {
        const errors = response.data.detail;
        if (Array.isArray(errors)) {
          errors.forEach(err => toast.error(err.msg));
        } else {
          toast.error(response.data.detail || 'Validation error');
        }
      }
    } else {
      // Network errors
      toast.error('Network error. Please check your connection.');
    }
    
    return Promise.reject(error);
  }
);

export default api; 