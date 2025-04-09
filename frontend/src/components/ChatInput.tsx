import React, { useState, useRef, FormEvent } from 'react';
import { Box, Flex, Textarea, IconButton, useToast } from '@chakra-ui/react';
import { IoSend, IoMic, IoAttach } from 'react-icons/io5';
import { COLORS } from '../utils/constants';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  isLoading,
  placeholder = 'Message Concordia AI...'
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const toast = useToast();

  const handleSubmit = (e?: FormEvent) => {
    e?.preventDefault();
    
    if (!message.trim()) return;
    
    onSendMessage(message);
    setMessage('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea up to 5 lines
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const newHeight = Math.min(textareaRef.current.scrollHeight, 150); // 150px is ~5 lines
      textareaRef.current.style.height = `${newHeight}px`;
    }
  };

  return (
    <Box 
      as="form" 
      onSubmit={handleSubmit}
      p={4}
      borderTop={`1px solid ${COLORS.lightGray}`}
      bg={COLORS.white}
    >
      <Flex 
        maxW="800px" 
        mx="auto" 
        bg={COLORS.lightGray}
        borderRadius="md"
        p={2}
        align="flex-end"
      >
        <Textarea
          ref={textareaRef}
          value={message}
          onChange={handleTextAreaChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          border="none"
          resize="none"
          minH="40px"
          maxH="150px"
          py={2}
          px={3}
          bg="transparent"
          _focus={{
            boxShadow: 'none',
            outline: 'none',
          }}
          disabled={isLoading}
        />
        <Flex align="center">
          <IconButton
            icon={<IoSend />}
            aria-label="Send message"
            colorScheme="burgundy"
            bg={COLORS.burgundy}
            color={COLORS.white}
            isLoading={isLoading}
            type="submit"
            isDisabled={!message.trim()}
            _hover={{
              bg: '#701a2b', // Darker burgundy
            }}
            size="sm"
          />
        </Flex>
      </Flex>
    </Box>
  );
};

export default ChatInput; 