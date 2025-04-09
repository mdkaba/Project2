// Color scheme based on Concordia University branding
export const COLORS = {
  // Primary Concordia colors
  burgundy: '#912338',
  gold: '#9D8845',
  orange: '#FF8200',
  
  // Additional UI colors
  beige: '#D4D0C8',
  darkGray: '#333333',
  lightGray: '#F5F5F5',
  white: '#FFFFFF',
  black: '#000000',
};

// Agent configurations with their respective colors
export const AGENTS = {
  AdmissionsAgent: {
    name: 'Admissions Agent',
    color: COLORS.burgundy,
    icon: '🎓',
  },
  AIExpertAgent: {
    name: 'AI Expert',
    color: COLORS.gold,
    icon: '🤖',
  },
  GeneralAgent: {
    name: 'General Assistant',
    color: COLORS.beige,
    icon: '💬',
  },
};

// API endpoints
export const API_BASE_URL = 'http://localhost:8000';
export const API_ENDPOINTS = {
  chat: '/api/v1/chat/',
}; 