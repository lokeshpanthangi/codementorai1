/**
 * API Service Layer
 * ==================
 * Centralized API calls to the FastAPI backend
 */

import axios from 'axios';

// API Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============= TYPE DEFINITIONS =============

export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  avatar_url: string;
  role: string;
  stats: UserStats;
  created_at: string;
}

export interface UserStats {
  total_solved: number;
  easy_solved: number;
  medium_solved: number;
  hard_solved: number;
  total_submissions: number;
  acceptance_rate: number;
  current_streak: number;
  longest_streak: number;
  reputation_points: number;
}

export interface Problem {
  id: string;
  problem_number: number;
  title: string;
  slug: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  category: string;
  topics: string[];
  companies: string[];
  acceptance_rate: number;
  frequency: number;
}

export interface ProblemDetail extends Problem {
  description: {
    problem_statement: string;
    examples: Array<{
      input: string;
      output: string;
      explanation?: string;
    }>;
    constraints: string[];
  };
  hints: string[];
  solution_templates: Record<string, string>;
  stats: {
    total_submissions: number;
    total_accepted: number;
    acceptance_rate: number;
    difficulty_rating: number;
    total_solved: number;
    like_count: number;
    dislike_count: number;
  };
  time_complexity?: string;
  space_complexity?: string;
  similar_problems: number[];
}

export interface TestCase {
  id: string;
  test_case_number: number;
  is_hidden: boolean;
  input_string: string;
  expected_output_string: string;
  explanation?: string;
}

export interface SubmissionResult {
  id: string;
  status: string;
  score: number;
  test_results: TestResult[];
  summary?: {
    total_tests: number;
    passed_tests: number;
    failed_tests: number;
    avg_runtime_ms: number;
    avg_memory_kb: number;
  };
  submitted_at: string;
}

export interface TestResult {
  test_case_number: number;
  status: string;
  passed: boolean;
  runtime_ms: number;
  memory_kb: number;
  expected_output: string;
  user_output: string;
  stdout?: string;
  stderr?: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon: string;
  color: string;
  problem_count: number;
  difficulty_distribution: {
    easy: number;
    medium: number;
    hard: number;
  };
}

export interface DailyChallenge {
  id: string;
  date: string;
  problem_number: number;
  bonus_points: number;
  participants_count: number;
  solvers_count: number;
  problem?: ProblemDetail;
}

// ============= AUTH API =============

export const authAPI = {
  signup: async (username: string, email: string, password: string) => {
    const response = await api.post('/auth/signup', { username, email, password });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    
    // Store token
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// ============= PROBLEMS API =============

export const problemsAPI = {
  getAllProblems: async (): Promise<Problem[]> => {
    const response = await api.get('/problems/');
    return response.data;
  },

  getProblemBySlug: async (slug: string): Promise<ProblemDetail> => {
    const response = await api.get(`/problems/${slug}`);
    return response.data;
  },

  getProblemStats: async (problemId: string) => {
    const response = await api.get(`/problems/${problemId}/stats`);
    return response.data;
  },
};

// ============= TEST CASES API =============

export const testCasesAPI = {
  getVisibleTestCases: async (problemNumber: number): Promise<TestCase[]> => {
    const response = await api.get(`/testcases/${problemNumber}/visible`);
    return response.data;
  },

  getAllTestCases: async (problemNumber: number): Promise<TestCase[]> => {
    const response = await api.get(`/testcases/${problemNumber}/all`);
    return response.data;
  },
};

// ============= SUBMISSIONS API =============

export const submissionsAPI = {
  runCode: async (
    problemNumber: number,
    language: string,
    code: string
  ): Promise<SubmissionResult> => {
    const response = await api.post('/submissions/run', {
      problem_number: problemNumber,
      language,
      code,
    });
    return response.data;
  },

  submitCode: async (
    problemNumber: number,
    language: string,
    code: string
  ): Promise<SubmissionResult> => {
    const response = await api.post('/submissions/submit', {
      problem_number: problemNumber,
      language,
      code,
    });
    return response.data;
  },

  getUserSubmissions: async (userId: string) => {
    const response = await api.get(`/submissions/user/${userId}`);
    return response.data;
  },
};

// ============= CATEGORIES API =============

export const categoriesAPI = {
  getAllCategories: async (): Promise<Category[]> => {
    const response = await api.get('/categories/');
    return response.data;
  },

  getCategoryBySlug: async (slug: string): Promise<Category> => {
    const response = await api.get(`/categories/${slug}`);
    return response.data;
  },
};

// ============= DAILY CHALLENGE API =============

export const dailyChallengeAPI = {
  getTodayChallenge: async (): Promise<DailyChallenge> => {
    const response = await api.get('/daily-challenge/today');
    return response.data;
  },

  getChallengeHistory: async (limit: number = 7) => {
    const response = await api.get(`/daily-challenge/history?limit=${limit}`);
    return response.data;
  },
};

// Export default api instance for custom calls
export default api;
