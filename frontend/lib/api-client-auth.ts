/**
 * API Client with JWT Authentication
 *
 * This is a wrapper around the API client that automatically
 * injects JWT tokens for authenticated requests.
 *
 * Usage:
 *   const client = useAuthenticatedAPI();
 *   const topics = await client.getTrendingTopics();
 */

import { apiClient } from './api-client';

export function useAuthenticatedAPI() {
  // Token is already set in apiClient by AuthProvider
  // This hook exists for consistency and future enhancements

  const authenticatedClient = {
    async makeRequest<T>(requestFn: () => Promise<T>): Promise<T> {
      try {
        // Get token from localStorage
        const token = localStorage.getItem('token');

        if (token) {
          apiClient.setToken(token);
        }

        // Make the request
        return await requestFn();
      } catch (error) {
        // Clear token on 401 errors
        if (error instanceof Error && error.message.includes('401')) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          apiClient.clearToken();
          // Optionally redirect to login
          window.location.href = '/login';
        }
        throw error;
      }
    },

    // Topics endpoints (no auth required)
    getTrendingTopics: (params?: { discipline?: string; limit?: number }) =>
      apiClient.getTrendingTopics(params),

    getPersonalizedTopics: (data: { interests: string[]; research_area?: string }) =>
      apiClient.getPersonalizedTopics(data),

    getTopicEvolution: (data: { topic: string; years?: number }) =>
      apiClient.getTopicEvolution(data),

    // Papers endpoints (auth required)
    uploadPaper: async (file: File, options?: { language?: string }) => {
      return await authenticatedClient.makeRequest(() => apiClient.uploadPaper(file));
    },

    processPaper: async (paperId: number, options?: { language?: string; paper_type?: string }) => {
      return await authenticatedClient.makeRequest(() => apiClient.processPaper(paperId, options));
    },

    getPaper: async (paperId: number, options?: { language?: string }) => {
      return await authenticatedClient.makeRequest(() => apiClient.getPaper(paperId, options?.language));
    },

    listPapers: async (options?: { language?: string; limit?: number; offset?: number }) => {
      return await authenticatedClient.makeRequest(() => apiClient.listPapers(options));
    },

    getRelatedPapers: async (paperId: number, limit?: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.getRelatedPapers(paperId, limit));
    },

    deletePaper: async (paperId: number, options?: { language?: string }) => {
      return await authenticatedClient.makeRequest(() => apiClient.deletePaper(paperId));
    },

    // Plagiarism endpoints (auth required)
    checkPlagiarism: async (data: {
      text?: string;
      file_url?: string;
      website?: string;
      excluded_sources?: string[];
      language?: string;
      country?: string;
      check_online?: boolean;
      use_winston?: boolean;
    }) => {
      return await authenticatedClient.makeRequest(() => apiClient.checkPlagiarism(data));
    },

    getPlagiarismReport: async (reportId: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.getPlagiarismReport(reportId));
    },

    getPlagiarismHistory: async () => {
      return await authenticatedClient.makeRequest(() => apiClient.getPlagiarismHistory());
    },

    suggestCitations: async (data: { claims: string[] }) => {
      return await authenticatedClient.makeRequest(() => apiClient.suggestCitations(data));
    },

    // Journals endpoints (auth required)
    recommendJournals: async (data: {
      abstract: string;
      keywords: string[];
      preferences?: {
        open_access_only?: boolean;
        min_impact_factor?: number;
        max_time_to_publish?: number;
      };
    }) => {
      return await authenticatedClient.makeRequest(() => apiClient.recommendJournals(data));
    },

    getJournal: async (journalId: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.getJournal(journalId));
    },

    searchJournals: async (params: { query: string; discipline?: string }) => {
      return await authenticatedClient.makeRequest(() => apiClient.searchJournals(params));
    },
  };

  return authenticatedClient;
}
