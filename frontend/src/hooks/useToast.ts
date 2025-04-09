// Simple toast implementation
type ToastOptions = {
  title: string;
  description?: string;
  status?: 'info' | 'warning' | 'success' | 'error';
  duration?: number;
  isClosable?: boolean;
};

// Custom hook for toast notifications
export const useToast = () => {
  return (options: ToastOptions) => {
    console.error(`${options.status?.toUpperCase() || 'INFO'}: ${options.title}${options.description ? ` - ${options.description}` : ''}`);
    alert(`${options.title}${options.description ? `\n${options.description}` : ''}`);
  };
}; 