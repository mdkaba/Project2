import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../utils/constants';

// API client with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface ChatRequest {
  query: string;
  conversation_id: string | null;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  agent_name: string;
  context_docs: any[] | null;
  debug_info: any | null;
}

// API functions
export const chatApi = {
  // Send a message to the chatbot
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    try {
      const response = await apiClient.post<ChatResponse>(
        API_ENDPOINTS.chat,
        request
      );
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },
}; 