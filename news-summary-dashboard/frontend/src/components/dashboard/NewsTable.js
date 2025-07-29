import React, { useState, useEffect } from "react";
import {
  Tooltip,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Box,
  Text,
  HStack,
  Tag,
  IconButton,
  useColorModeValue,
  Button,
  Flex,
  Spinner,
} from "@chakra-ui/react";
import { keyframes } from "@emotion/react";
import { FaRegBookmark, FaBookmark } from "react-icons/fa";

const NewsTable = ({ newsData, loading, error }) => {
  // State for UI interactions
  const [bookmarks, setBookmarks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    setBookmarks(Array((newsData || []).length).fill(false));
    setCurrentPage(1); // Luôn quay về trang 1 khi có dữ liệu mới
  }, [newsData]);

  const handleBookmark = (idx) => {
    setBookmarks((bm) => {
      const copy = [...bm];
      copy[idx] = !copy[idx];
      return copy;
    });
  };

  // --- Render logic ---

  // Tạo hiệu ứng xoay
  const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

  // Tạo hiệu ứng nhấp nháy cho text
  const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

  // Trong component của bạn
  if (loading) {
    return (
      <Flex
        justify="center"
        align="center"
        height="400px"
        flexDirection="column"
        gap={6}
      >
        {/* Gradient Spinner */}
        <Box position="relative" w="80px" h="80px">
          <Box
            position="absolute"
            top="0"
            left="0"
            w="100%"
            h="100%"
            borderRadius="full"
            border="4px solid"
            borderColor="transparent"
            borderTopColor="blue.400"
            animation={`${spin} 1s linear infinite`}
          />
          <Box
            position="absolute"
            top="0"
            left="0"
            w="100%"
            h="100%"
            borderRadius="full"
            border="4px solid"
            borderColor="transparent"
            borderBottomColor="purple.500"
            animation={`${spin} 0.5s linear infinite reverse`}
          />
        </Box>

        {/* Animated Text */}
        <Text
          fontSize="xl"
          fontWeight="medium"
          bgGradient="linear(to-r, blue.400, purple.500)"
          bgClip="text"
          animation={`${pulse} 1.5s ease-in-out infinite`}
        >
          Đang tải dữ liệu...
        </Text>
      </Flex>
    );
  }

  // Display an error message if the fetch failed
  if (error) {
    return (
      <Flex justify="center" align="center" height="400px" color="red.500">
        <Text fontSize="lg">{error}</Text>
      </Flex>
    );
  }

  // --- Pagination Logic (runs after data is loaded) ---
  const totalPages = Math.ceil(newsData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = newsData.slice(startIndex, endIndex);

  const formatPageNumber = (number) => {
    // Chuyển số thành chuỗi và thêm '0' vào trước nếu cần để đủ 2 ký tự
    return String(number).padStart(2, "0");
  };

  return (
    <Box>
      <Box overflowX="auto">
        <Table variant="simple" width="100%" tableLayout="fixed">
          <Thead>
            <Tr bg="gray.100">
              <Th
                w="2%"
                fontSize="lg"
                fontWeight="bold"
                textTransform="none"
              ></Th>
              <Th w="10%" fontSize="lg" fontWeight="bold" textTransform="none">
                Ngày
              </Th>
              <Th w="12%" fontSize="lg" fontWeight="bold" textTransform="none">
                Ngành
              </Th>
              <Th w="22%" fontSize="lg" fontWeight="bold" textTransform="none">
                Tiêu đề
              </Th>
              <Th w="32%" fontSize="lg" fontWeight="bold" textTransform="none">
                Tóm tắt
              </Th>
              <Th w="10%" fontSize="lg" fontWeight="bold" textTransform="none">
                Ảnh hưởng
              </Th>
              <Th w="12%" fontSize="lg" fontWeight="bold" textTransform="none">
                Hashtags
              </Th>
            </Tr>
          </Thead>
          <Tbody>
            {currentData.map((row, idx) => (
              <Tr
                key={row.id || idx}
                _hover={{ bg: "gray.50" }}
                height="110px"
                minHeight="110px"
              >
                {/* Bookmark */}
                <Td w="2%" textAlign="center">
                  <IconButton
                    icon={
                      bookmarks[startIndex + idx] ? (
                        <FaBookmark />
                      ) : (
                        <FaRegBookmark />
                      )
                    }
                    color={
                      bookmarks[startIndex + idx] ? "yellow.400" : "blue.500"
                    }
                    variant="ghost"
                    size="sm"
                    onClick={() => handleBookmark(startIndex + idx)}
                    aria-label={
                      bookmarks[startIndex + idx]
                        ? "Bỏ bookmark"
                        : "Đánh dấu bookmark"
                    }
                  />
                </Td>
                {/* Date */}
                <Td w="10%">{row.date}</Td>
                {/* Industry */}
                <Td w="12%">
                  <Tooltip
                    label={
                      Array.isArray(row.industry)
                        ? row.industry.join(", ")
                        : row.industry
                    }
                    placement="right"
                    openDelay={300}
                    bg="blue.100"
                    color="gray.800"
                    borderRadius="md"
                    fontSize="sm"
                    px={4}
                    py={2}
                  >
                    <Box cursor="pointer">
                      <Flex
                        direction="column"
                        gap={1}
                        align="flex-start"
                        color="blue.500"
                      >
                        {(Array.isArray(row.industry)
                          ? row.industry.slice(0, 2)
                          : [row.industry]
                        ).map((item, i) => (
                          <Text
                            key={i}
                            // whiteSpace="nowrap"
                            userSelect="none"
                            fontWeight="medium"
                            // width="fit-content"
                            isTruncated
                          >
                            {item}
                          </Text>
                        ))}
                        {Array.isArray(row.industry) &&
                          row.industry.length > 2 && (
                            <Text
                              fontSize="sm"
                              color="gray.500"
                              width="fit-content"
                            >
                              +{row.industry.length - 2}
                            </Text>
                          )}
                      </Flex>
                    </Box>
                  </Tooltip>
                </Td>
                {/* Title */}
                <Td w="22%">
                  <Tooltip
                    label={row.title}
                    isDisabled={row.title.length <= 50}
                    placement="top-start"
                    bg="blue.100"
                    color="gray.800"
                    borderRadius="md"
                    fontSize="sm"
                    px={4}
                    py={2}
                  >
                    <Text
                      fontWeight="medium"
                      noOfLines={2}
                      cursor={row.title.length > 50 ? "pointer" : "default"}
                    >
                      {row.title}
                    </Text>
                  </Tooltip>
                </Td>
                {/* Summary */}
                <Td w="32%">
                  <Tooltip
                    label={row.summary}
                    isDisabled={row.summary.length <= 80}
                    placement="top-start"
                    openDelay={300}
                    bg="blue.50"
                    color="gray.800"
                    borderRadius="md"
                    fontSize="sm"
                    px={4}
                    py={2}
                  >
                    <Text
                      color="gray.600"
                      noOfLines={2}
                      cursor={row.summary.length > 80 ? "pointer" : "default"}
                    >
                      {row.summary}
                    </Text>
                  </Tooltip>
                </Td>
                {/* Score */}
                <Td w="10%">
                  <HStack spacing={2}>
                    <Text>{row.influence_score}</Text>
                    <Box w="30px" h="20px" bg={row.color} borderRadius="sm" />
                  </HStack>
                </Td>
                {/* Hashtags */}
                <Td w="12%">
                  <Tooltip
                    label={
                      Array.isArray(row.hashtags) ? row.hashtags.join(" ") : ""
                    }
                    placement="right"
                    openDelay={300}
                    bg="blue.100"
                    color="gray.800"
                    borderRadius="md"
                    fontSize="sm"
                    px={4}
                    py={2}
                  >
                    <Box cursor="pointer">
                      <Flex direction="column" gap={1} align="flex-start">
                        {Array.isArray(row.hashtags) &&
                          row.hashtags.slice(0, 2).map((tag, i) => (
                            <Tag
                              key={i}
                              size="sm"
                              colorScheme="blue"
                              variant="subtle"
                              whiteSpace="nowrap"
                              userSelect="none"
                              width="fit-content"
                            >
                              {tag}
                            </Tag>
                          ))}
                        {Array.isArray(row.hashtags) &&
                          row.hashtags.length > 2 && (
                            <Tag
                              size="sm"
                              colorScheme="gray"
                              variant="subtle"
                              whiteSpace="nowrap"
                              userSelect="none"
                              width="fit-content"
                            >
                              +{row.hashtags.length - 2}
                            </Tag>
                          )}
                      </Flex>
                    </Box>
                  </Tooltip>
                </Td>
              </Tr>
            ))}
            {/* Add empty rows to maintain table height */}
            {Array(itemsPerPage - currentData.length)
              .fill("")
              .map((_, i) => (
                <Tr key={"empty-" + i} height="110px" minHeight="110px">
                  <Td colSpan={7} />
                </Tr>
              ))}
          </Tbody>
        </Table>
      </Box>
      {/* Pagination controls */}
      <Flex justify="center" mt={4} gap={2}>
        <Button
          onClick={() => setCurrentPage(1)}
          isDisabled={currentPage === 1}
          size="sm"
        >
          Trang đầu
        </Button>
        <Button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          isDisabled={currentPage === 1}
          size="sm"
        >
          Trang trước
        </Button>
        <Text alignSelf="center">
          Trang {formatPageNumber(currentPage)} /{" "}
          {formatPageNumber(totalPages > 0 ? totalPages : 1)}
        </Text>
        <Button
          onClick={() =>
            setCurrentPage((prev) => Math.min(prev + 1, totalPages))
          }
          isDisabled={currentPage === totalPages || totalPages === 0}
          size="sm"
        >
          Trang sau
        </Button>
      </Flex>
    </Box>
  );
};

export default NewsTable; 