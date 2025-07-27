import React from "react";
import {
  Box,
  VStack,
  HStack,
  Text,
  Icon,
  Divider,
  List,
  ListItem,
  useColorModeValue
} from "@chakra-ui/react";
import { FiHome, FiBarChart2, FiBookmark, FiSettings, FiZap, FiRefreshCw, FiMapPin, FiHelpCircle } from "react-icons/fi";

const Sidebar = () => {
  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");
  const iconColor = "blue.500";

  return (
    <Box
      w="240px"
      minH="100vh"
      bg={bgColor}
      borderRight="1px"
      borderColor={borderColor}
      display="flex"
      flexDirection="column"
      py={2}
    >
      <HStack px={6} mb={6}>
        <Icon as={FiBookmark} w={8} h={8} color={iconColor} />
        <Text fontSize="xl" fontWeight="bold" color="gray.700">
          news
        </Text>
      </HStack>

      <List spacing={1}>
        <ListItem>
          <HStack
            px={6}
            py={2}
            cursor="pointer"
            _hover={{ bg: "gray.50" }}
            bg="blue.50"
          >
            <Icon as={FiHome} w={5} h={5} color={iconColor} />
            <Text>Dashboard</Text>
          </HStack>
        </ListItem>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiBarChart2} w={5} h={5} color={iconColor} />
            <Text>Analytics</Text>
          </HStack>
        </ListItem>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiBookmark} w={5} h={5} color={iconColor} />
            <Text>Saved Articles</Text>
          </HStack>
        </ListItem>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiSettings} w={5} h={5} color={iconColor} />
            <Text>Settings</Text>
          </HStack>
        </ListItem>
      </List>

      <Divider my={4} mx={4} />
      
      <Text px={6} fontSize="xs" color="gray.500" fontWeight="bold" letterSpacing="wider">
        QUICK FILTERS
      </Text>

      <List spacing={1}>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiZap} w={5} h={5} color={iconColor} />
            <Text>Breaking News</Text>
          </HStack>
        </ListItem>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiRefreshCw} w={5} h={5} color={iconColor} />
            <Text>Industry Updates</Text>
          </HStack>
        </ListItem>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiMapPin} w={5} h={5} color={iconColor} />
            <Text>Local News</Text>
          </HStack>
        </ListItem>
      </List>

      <Box flexGrow={1} />

      <List>
        <ListItem>
          <HStack px={6} py={2} cursor="pointer" _hover={{ bg: "gray.50" }}>
            <Icon as={FiHelpCircle} w={5} h={5} color={iconColor} />
            <Text>Help</Text>
          </HStack>
        </ListItem>
      </List>
    </Box>
  );
};

export default Sidebar; 