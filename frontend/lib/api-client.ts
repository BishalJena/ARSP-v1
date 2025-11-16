const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    // Load token from localStorage if available
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // ============ AUTH ENDPOINTS ============
  async register(data: { email: string; password: string; full_name: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Invalid credentials');
    }

    const data = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  async getCurrentUser() {
    return this.request('/users/me');
  }

  // ============ TOPICS ENDPOINTS ============
  async getTrendingTopics(params?: { discipline?: string; limit?: number; language?: string }) {
    const query = new URLSearchParams(params as any).toString();
    return this.request(`/topics/trending${query ? `?${query}` : ''}`);
  }

  async getPersonalizedTopics(data: { interests: string[]; research_area?: string }) {
    return this.request('/topics/personalized', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getTopicEvolution(data: { topic: string; years?: number }) {
    return this.request('/topics/evolution', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ============ PAPERS ENDPOINTS ============
  async uploadPaper(file: File, options?: { language?: string }) {
    const formData = new FormData();
    formData.append('file', file);

    const headers: Record<string, string> = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseURL}/papers-enhanced/upload`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return response.json();
  }

  async processPaper(paperId: number, options?: { language?: string; paper_type?: string }) {
    const params = new URLSearchParams();
    if (options?.language) params.append('language', options.language);
    if (options?.paper_type) params.append('paper_type', options.paper_type);

    const queryString = params.toString();
    const url = `/papers-enhanced/${paperId}/process${queryString ? `?${queryString}` : ''}`;

    return this.request(url, {
      method: 'POST',
    });
  }

  async getPaper(paperId: number, options?: { language?: string }) {
    const queryString = options?.language ? `?language=${options.language}` : '';
    return this.request(`/papers-enhanced/${paperId}${queryString}`);
  }

  async listPapers(options?: { limit?: number; offset?: number; language?: string }) {
    const params = new URLSearchParams();
    if (options?.limit) params.append('limit', options.limit.toString());
    if (options?.offset) params.append('offset', options.offset.toString());
    if (options?.language) params.append('language', options.language);

    const queryString = params.toString();
    return this.request(`/papers-enhanced/${queryString ? `?${queryString}` : ''}`);
  }

  async getRelatedPapers(paperId: number, limit: number = 10) {
    return this.request(`/papers/${paperId}/related?limit=${limit}`);
  }

  async deletePaper(paperId: number) {
    return this.request(`/papers-enhanced/${paperId}`, {
      method: 'DELETE',
    });
  }

  // ============ PLAGIARISM ENDPOINTS ============
  async checkPlagiarism(data: {
    text?: string;
    file_url?: string;
    website?: string;
    excluded_sources?: string[];
    language?: string;
    country?: string;
    check_online?: boolean;
    use_winston?: boolean;
  }) {
    return this.request('/plagiarism/check', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getPlagiarismReport(reportId: number) {
    return this.request(`/plagiarism/report/${reportId}`);
  }

  async getPlagiarismHistory() {
    return this.request('/plagiarism/history');
  }

  async suggestCitations(data: { claims: string[] }) {
    return this.request('/plagiarism/citations/suggest', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ============ JOURNALS ENDPOINTS ============
  async recommendJournals(data: {
    abstract: string;
    keywords: string[];
    language?: string;
    preferences?: {
      open_access_only?: boolean;
      min_impact_factor?: number;
      max_time_to_publish?: number;
    };
  }) {
    return this.request('/journals/recommend', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getJournal(journalId: number) {
    return this.request(`/journals/${journalId}`);
  }

  async searchJournals(params: { query: string; discipline?: string }) {
    const query = new URLSearchParams(params as any).toString();
    return this.request(`/journals/search?${query}`);
  }

  // ============ GOVERNMENT ENDPOINTS ============
  async analyzeGovernmentAlignment(data: {
    research_topic: string;
    research_abstract: string;
    keywords: string[];
  }) {
    return this.request('/government/analyze-alignment', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async predictImpact(data: {
    research_topic: string;
    research_abstract: string;
    target_districts?: string[];
  }) {
    return this.request('/government/predict-impact', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getGovernmentPriorities() {
    return this.request('/government/priorities');
  }

  async getFundingSchemes() {
    return this.request('/government/funding');
  }

  async getDistricts() {
    return this.request('/government/districts');
  }

  async analyzeFullGovernment(data: {
    research_topic: string;
    research_abstract: string;
    keywords: string[];
    target_districts?: string[];
  }) {
    return this.request('/government/analyze-full', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new APIClient(API_BASE_URL);
