import React from 'react';
import { Box, Flex, Text, Badge } from '@chakra-ui/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '../types/chat';
import { AGENTS, COLORS } from '../utils/constants';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUserMessage = message.role === 'user';
  
  // Get agent info if it's an assistant message
  const agentInfo = !isUserMessage && message.agent_name
    ? AGENTS[message.agent_name as keyof typeof AGENTS] || AGENTS.GeneralAgent
    : null;

  return (
    <Box
      w="100%"
      py={4}
      px={8}
      bg={isUserMessage ? COLORS.lightGray : COLORS.white}
      borderBottom={`1px solid ${COLORS.lightGray}`}
    >
      <Box maxW="800px" mx="auto">
        {/* If it's an assistant message, show the agent badge */}
        {!isUserMessage && agentInfo && (
          <Flex mb={2} align="center">
            <Text fontSize="lg" mr={2}>
              {agentInfo.icon}
            </Text>
            <Badge
              px={2}
              py={0.5}
              borderRadius="full"
              colorScheme="gray"
              bg={agentInfo.color}
              color={agentInfo.color === COLORS.beige ? COLORS.darkGray : COLORS.white}
              fontSize="xs"
            >
              {agentInfo.name}
            </Badge>
          </Flex>
        )}
        
        {/* Message content */}
        <Box className={`chat-message ${isUserMessage ? 'user' : 'assistant'}`}>
          <ReactMarkdown
            className="markdown-content"
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ node, ...props }) => (
                <Text mb={2} {...props} />
              ),
              a: ({ node, ...props }) => (
                <Text as="a" color={COLORS.burgundy} textDecoration="underline" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <Box as="ul" pl={5} mb={3} {...props} />
              ),
              ol: ({ node, ...props }) => (
                <Box as="ol" pl={5} mb={3} {...props} />
              ),
              li: ({ node, ...props }) => (
                <Box as="li" mb={1} {...props} />
              ),
              h1: ({ node, ...props }) => (
                <Text as="h1" fontSize="2xl" fontWeight="bold" mb={3} mt={4} {...props} />
              ),
              h2: ({ node, ...props }) => (
                <Text as="h2" fontSize="xl" fontWeight="bold" mb={2} mt={3} {...props} />
              ),
              h3: ({ node, ...props }) => (
                <Text as="h3" fontSize="lg" fontWeight="bold" mb={2} mt={3} {...props} />
              ),
              code: ({ node, inline, ...props }) => 
                inline ? (
                  <Text as="code" bg={COLORS.lightGray} p={1} borderRadius="md" fontSize="sm" {...props} />
                ) : (
                  <Box
                    as="pre"
                    bg={COLORS.lightGray}
                    p={3}
                    borderRadius="md"
                    fontSize="sm"
                    overflowX="auto"
                    my={3}
                    {...props}
                  />
                ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatMessage; 