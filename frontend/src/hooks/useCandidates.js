import { useQuery, useMutation, useQueryClient } from 'react-query';
import { candidateService } from '@services/candidateService';
import toast from 'react-hot-toast';

/**
 * Hook for managing candidates data and operations
 */
export const useCandidates = () => {
  const queryClient = useQueryClient();

  // Fetch candidates with optional filters
  const useCandidatesList = (filters = {}, options = {}) => {
    return useQuery(
      ['candidates', filters],
      () => candidateService.getCandidates(filters),
      {
        keepPreviousData: true,
        staleTime: 5 * 60 * 1000, // 5 minutes
        ...options
      }
    );
  };

  // Fetch a single candidate by ID
  const useCandidate = (id, options = {}) => {
    return useQuery(
      ['candidate', id],
      () => candidateService.getCandidate(id),
      {
        enabled: !!id,
        ...options
      }
    );
  };

  // Upload a new candidate
  const useUploadCandidate = () => {
    return useMutation(
      (formData) => candidateService.uploadCandidate(formData),
      {
        onSuccess: () => {
          queryClient.invalidateQueries('candidates');
          toast.success('Candidate uploaded successfully');
        },
        onError: (error) => {
          toast.error(error.response?.data?.detail || 'Failed to upload candidate');
        }
      }
    );
  };

  // Contact a candidate
  const useContactCandidate = () => {
    return useMutation(
      ({ id, jobId }) => candidateService.contactCandidate(id, jobId),
      {
        onSuccess: () => {
          queryClient.invalidateQueries('candidates');
          toast.success('Email sent to candidate');
        }
      }
    );
  };

  // Schedule an interview
  const useScheduleInterview = () => {
    return useMutation(
      ({ id, data }) => candidateService.scheduleInterview(id, data),
      {
        onSuccess: () => {
          queryClient.invalidateQueries('candidates');
          toast.success('Interview scheduled successfully');
        }
      }
    );
  };

  return {
    useCandidatesList,
    useCandidate,
    useUploadCandidate,
    useContactCandidate,
    useScheduleInterview
  };
};

export default useCandidates; 