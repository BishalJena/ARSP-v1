/**
 * API Client with Clerk Authentication Integration
 *
 * This is a wrapper around the API client that automatically
 * injects Clerk JWT tokens for authenticated requests.
 *
 * Usage:
 *   const client = useAuthenticatedAPI();
 *   const topics = await client.getTrendingTopics();
 */

import { useAuth } from '@clerk/nextjs';
import { apiClient } from './api-client';

export function useAuthenticatedAPI() {
  const { getToken } = useAuth();

  // Create a wrapper that injects the token before each request
  const authenticatedClient = {
    async makeRequest<T>(requestFn: () => Promise<T>): Promise<T> {
      try {
        // Get Clerk JWT token
        const token = await getToken();

        // Set token in API client
        if (token) {
          apiClient.setToken(token);
        }

        // Make the request
        return await requestFn();
      } catch (error) {
        // Clear token on auth errors
        if (error instanceof Error && error.message.includes('401')) {
          apiClient.clearToken();
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
    uploadPaper: async (file: File) => {
      return await authenticatedClient.makeRequest(() => apiClient.uploadPaper(file));
    },

    processPaper: async (paperId: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.processPaper(paperId));
    },

    getPaper: async (paperId: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.getPaper(paperId));
    },

    listPapers: async () => {
      return await authenticatedClient.makeRequest(() => apiClient.listPapers());
    },

    getRelatedPapers: async (paperId: number, limit?: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.getRelatedPapers(paperId, limit));
    },

    deletePaper: async (paperId: number) => {
      return await authenticatedClient.makeRequest(() => apiClient.deletePaper(paperId));
    },

    // Plagiarism endpoints (auth required for now, can be made optional)
    checkPlagiarism: async (data: { text: string; language?: string; check_online?: boolean }) => {
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
