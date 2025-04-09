// Message types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  agent_name?: string; // For assistant messages, to identify which agent responded
}

// Conversation type
export interface Conversation {
  id: string;
  messages: Message[];
  title?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Chat state
export interface ChatState {
  conversations: Conversation[];
  currentConversationId: string | null;
  isLoading: boolean;
  error: string | null;
}

// Action types for the chat reducer
export enum ChatActionType {
  SET_CONVERSATIONS = 'SET_CONVERSATIONS',
  ADD_CONVERSATION = 'ADD_CONVERSATION',
  SET_CURRENT_CONVERSATION = 'SET_CURRENT_CONVERSATION',
  ADD_MESSAGE = 'ADD_MESSAGE',
  SET_LOADING = 'SET_LOADING',
  SET_ERROR = 'SET_ERROR',
} 