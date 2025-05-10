import api from './api';

export const candidateService = {
  /**
   * Get paginated candidates with optional filters
   * @param {Object} params - Query parameters
   * @returns {Promise} - API response
   */
  getCandidates: async (params = {}) => {
    const response = await api.get('/candidates/', { params });
    return response.data;
  },

  /**
   * Get a specific candidate by ID
   * @param {number} id - Candidate ID
   * @returns {Promise} - API response
   */
  getCandidate: async (id) => {
    const response = await api.get(`/candidates/${id}`);
    return response.data;
  },

  /**
   * Upload a new candidate resume
   * @param {FormData} formData - Form data with candidate info and resume
   * @returns {Promise} - API response
   */
  uploadCandidate: async (formData) => {
    const response = await api.post('/candidates/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Contact a candidate for interview
   * @param {number} id - Candidate ID
   * @param {number} jobId - Optional job ID
   * @returns {Promise} - API response
   */
  contactCandidate: async (id, jobId = null) => {
    const params = jobId ? { job_id: jobId } : {};
    const response = await api.post(`/candidates/${id}/contact`, {}, { params });
    return response.data;
  },

  /**
   * Schedule an interview with a candidate
   * @param {number} id - Candidate ID
   * @param {Object} data - Schedule data (datetime, job_id)
   * @returns {Promise} - API response
   */
  scheduleInterview: async (id, data) => {
    const formData = new FormData();
    formData.append('date_time', data.dateTime);
    if (data.jobId) {
      formData.append('job_id', data.jobId);
    }
    
    const response = await api.post(`/candidates/${id}/schedule`, formData);
    return response.data;
  }
}; 