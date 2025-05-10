import api from './api';

export const jobService = {
  /**
   * Get paginated jobs with optional filters
   * @param {Object} params - Query parameters
   * @returns {Promise} - API response
   */
  getJobs: async (params = {}) => {
    const response = await api.get('/jobs/', { params });
    return response.data;
  },

  /**
   * Get a specific job by ID
   * @param {number} id - Job ID
   * @returns {Promise} - API response
   */
  getJob: async (id) => {
    const response = await api.get(`/jobs/${id}`);
    return response.data;
  },

  /**
   * Create a new job posting
   * @param {Object} jobData - Job data
   * @returns {Promise} - API response
   */
  createJob: async (jobData) => {
    const response = await api.post('/jobs/', jobData);
    return response.data;
  },

  /**
   * Update an existing job
   * @param {number} id - Job ID
   * @param {Object} jobData - Job data to update
   * @returns {Promise} - API response
   */
  updateJob: async (id, jobData) => {
    const response = await api.patch(`/jobs/${id}`, jobData);
    return response.data;
  },

  /**
   * Search for candidates from external sources for a job
   * @param {number} jobId - Job ID
   * @param {Array} sources - External sources to search
   * @returns {Promise} - API response
   */
  searchExternalCandidates: async (jobId, sources = ['linkedin', 'cvlibrary', 'naukri']) => {
    const response = await api.post('/search/external/', null, {
      params: {
        job_id: jobId,
        sources: sources.join(',')
      }
    });
    return response.data;
  }
}; 