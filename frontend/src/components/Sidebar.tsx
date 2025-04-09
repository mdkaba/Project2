import React from 'react';
import { 
  Box, 
  VStack, 
  Button, 
  Text, 
  Divider, 
  Flex, 
  IconButton, 
  Tooltip
} from '@chakra-ui/react';
import { IoAdd, IoMenu } from 'react-icons/io5';
import ConcordiaLogo from './ConcordiaLogo';
import { COLORS } from '../utils/constants';
import { Conversation } from '../types/chat';

interface SidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onNewConversation: () => void;
  onSelectConversation: (id: string) => void;
  isMobile?: boolean;
  isOpen?: boolean;
  onToggle?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  conversations,
  currentConversationId,
  onNewConversation,
  onSelectConversation,
  isMobile = false,
  isOpen = true,
  onToggle,
}) => {
  // Only show a limited number of conversations in the sidebar
  const recentConversations = [...conversations]
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())
    .slice(0, 15);

  if (isMobile && !isOpen) {
    return (
      <Box 
        position="fixed" 
        top="0" 
        left="0" 
        p={4} 
        zIndex="999"
      >
        <IconButton
          icon={<IoMenu />}
          aria-label="Open menu"
          onClick={onToggle}
          colorScheme="blackAlpha"
          variant="outline"
        />
      </Box>
    );
  }

  return (
    <Box
      w={isMobile ? 'full' : '250px'}
      h="100vh"
      bg="white"
      borderRight={`1px solid ${COLORS.lightGray}`}
      p={4}
      overflow="auto"
      position={isMobile ? 'fixed' : 'relative'}
      top="0"
      left="0"
      zIndex="999"
      transition="0.3s ease"
      transform={isMobile && !isOpen ? 'translateX(-100%)' : 'translateX(0)'}
      boxShadow={isMobile ? 'lg' : 'none'}
    >
      <VStack h="full" spacing={6} align="stretch">
        {/* Logo section */}
        <Flex justify="space-between" align="center">
          <ConcordiaLogo size="md" />
          {isMobile && (
            <IconButton
              icon={<IoMenu />}
              aria-label="Close menu"
              onClick={onToggle}
              variant="ghost"
              size="sm"
            />
          )}
        </Flex>

        {/* New chat button */}
        <Button
          leftIcon={<IoAdd />}
          onClick={onNewConversation}
          bg={COLORS.burgundy}
          color="white"
          _hover={{ bg: '#701a2b' }}
          w="full"
        >
          New conversation
        </Button>

        <Divider />

        {/* Conversation history */}
        <VStack spacing={2} align="stretch" overflow="auto" flex="1">
          {recentConversations.length > 0 ? (
            recentConversations.map((conversation) => (
              <Button
                key={conversation.id}
                variant="ghost"
                justifyContent="flex-start"
                px={3}
                py={2}
                borderRadius="md"
                overflow="hidden"
                textOverflow="ellipsis"
                whiteSpace="nowrap"
                bg={currentConversationId === conversation.id ? COLORS.lightGray : 'transparent'}
                _hover={{ bg: COLORS.lightGray }}
                onClick={() => onSelectConversation(conversation.id)}
              >
                <Text fontSize="sm" isTruncated>
                  {conversation.title || 'New conversation'}
                </Text>
              </Button>
            ))
          ) : (
            <Text fontSize="sm" color="gray.500" px={3}>
              No conversations yet
            </Text>
          )}
        </VStack>

        {/* Footer */}
        <Box>
          <Divider mb={4} />
          <Text fontSize="xs" color="gray.500" textAlign="center">
            © {new Date().getFullYear()} Concordia University
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default Sidebar; 