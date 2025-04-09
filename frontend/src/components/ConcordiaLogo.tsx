import React from 'react';
import { Box, Text } from '@chakra-ui/react';
import { COLORS } from '../utils/constants';

interface ConcordiaLogoProps {
  size?: 'sm' | 'md' | 'lg';
}

const ConcordiaLogo: React.FC<ConcordiaLogoProps> = ({ size = 'md' }) => {
  // Size mapping
  const sizeMap = {
    sm: { height: '30px', fontSize: '16px' },
    md: { height: '40px', fontSize: '20px' },
    lg: { height: '60px', fontSize: '28px' },
  };

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="flex-start"
      height={sizeMap[size].height}
    >
      <Text
        fontFamily="serif"
        fontWeight="bold"
        fontSize={sizeMap[size].fontSize}
        color={COLORS.burgundy}
        letterSpacing="tighter"
        mr={1}
      >
        Concordia
      </Text>
      <Text
        fontFamily="serif"
        fontSize={sizeMap[size].fontSize}
        color={COLORS.gold}
        letterSpacing="tighter"
        fontWeight="light"
      >
        AI
      </Text>
    </Box>
  );
};

export default ConcordiaLogo; 