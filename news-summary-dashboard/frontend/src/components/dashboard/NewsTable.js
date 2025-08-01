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
  Button,
  Flex,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  VStack,
  Heading,
  Icon,
} from "@chakra-ui/react";
import { keyframes } from "@emotion/react";
import { FaRegBookmark, FaBookmark } from "react-icons/fa";
import { StarIcon, CalendarIcon, ViewIcon } from '@chakra-ui/icons';

const NewsTable = ({ newsData, loading, error }) => {
  // State for UI interactions
  const [bookmarks, setBookmarks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // 2. THÊM STATE CHO MODAL
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedNews, setSelectedNews] = useState(null);

  useEffect(() => {
    setBookmarks(Array((newsData || []).length).fill(false));
    setCurrentPage(1);
  }, [newsData]);

  // Sửa lại hàm bookmark để ngăn sự kiện click lan ra hàng
  const handleBookmark = (e, idx) => {
    e.stopPropagation(); // Ngăn sự kiện click vào hàng
    setBookmarks((bm) => {
      const copy = [...bm];
      copy[idx] = !copy[idx];
      return copy;
    });
  };
  
  // 3. HÀM XỬ LÝ KHI CLICK VÀO MỘT HÀNG
  const handleRowClick = (newsItem) => {
    setSelectedNews(newsItem);
    onOpen();
  };


  // --- Render logic ---
  const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
  `;

  const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
  `;

  if (loading) {
    return (
      <Flex
        justify="center"
        align="center"
        height="400px"
        flexDirection="column"
        gap={6}
      >
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

  if (error) {
    return (
      <Flex justify="center" align="center" height="400px" color="red.500">
        <Text fontSize="lg">{error}</Text>
      </Flex>
    );
  }

  const totalPages = Math.ceil(newsData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = newsData.slice(startIndex, endIndex);

  const formatPageNumber = (number) => {
    return String(number).padStart(2, "0");
  };

  return (
    <Box>
      <Box overflowX="auto">
        <Table variant="simple" width="100%" tableLayout="fixed">
          <Thead>
            <Tr bg="gray.100">
              <Th w="2%"></Th>
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
              // 4. THÊM ONCLICK VÀ CURSOR POINTER CHO HÀNG
              <Tr
                key={row.id || idx}
                _hover={{ bg: "gray.50", cursor: "pointer" }}
                height="110px"
                minHeight="110px"
                onClick={() => handleRowClick(row)}
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
                    // Cập nhật onClick của bookmark
                    onClick={(e) => handleBookmark(e, startIndex + idx)}
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

      {/* 5. THÊM COMPONENT MODAL */}
      {selectedNews && (
        <Modal
          isOpen={isOpen}
          onClose={onClose}
          size="5xl"
          scrollBehavior="inside"
          motionPreset="scale"
          isCentered
        >
          <ModalOverlay bg="blackAlpha.700" backdropFilter="blur(2px)" />

          <ModalContent borderRadius="xl" overflow="hidden" boxShadow="xl">
            <Box bgGradient="linear(to-r, blue.600, blue.500)" px={6} py={4}>
              <ModalHeader color="white" px={0} pt={3}>
                <Heading size="xl">{selectedNews.title}</Heading>
              </ModalHeader>

              <ModalCloseButton
                size="lg"
                color="white"
                _hover={{ bg: "blue.400" }}
              />
            </Box>

            <ModalBody py={6} px={{ base: 4, md: 8 }}>
              <VStack align="start" spacing={6}>
                {/* --- Meta Information --- */}
                <Flex
                  direction={{ base: "column", md: "row" }}
                  gap={4}
                  wrap="wrap"
                  pb={3}
                  borderBottom="1px solid"
                  borderColor="gray.100"
                  w="full"
                >
                  {/* Sửa: Thay thế bằng icon trực tiếp */}
                  <HStack spacing={2} align="center">
                    <Icon as={CalendarIcon} color="blue.500" boxSize={5} />
                    <Text fontWeight="600" color="gray.600">
                      Ngày:
                    </Text>
                    <Text color="gray.800">{selectedNews.date}</Text>
                  </HStack>

                  <HStack spacing={2} align="center">
                    <Icon as={ViewIcon} color="green.500" boxSize={5} />
                    <Text fontWeight="600" color="gray.600">
                      Ngành:
                    </Text>
                    <Text color="gray.800">
                      {Array.isArray(selectedNews.industry)
                        ? selectedNews.industry.join(", ")
                        : selectedNews.industry}
                    </Text>
                  </HStack>

                  <HStack spacing={2} align="center">
                    <Icon as={StarIcon} color="orange.500" boxSize={5} />
                    <Text fontWeight="600" color="gray.600">
                      Ảnh hưởng:
                    </Text>
                    <Text color="gray.800">{selectedNews.influence_score}</Text>
                    <Box
                      w="20px"
                      h="20px"
                      bg={selectedNews.color}
                      borderRadius="sm"
                      ml={2}
                    />
                  </HStack>
                </Flex>

                {/* --- Summary --- */}
                <Box w="full">
                  <Heading
                    size="md"
                    mb={3}
                    color="blue.700"
                    display="flex"
                    alignItems="center"
                  >
                    <Box
                      w="4px"
                      h="22px"
                      bg="blue.500"
                      mr={2}
                      borderRadius="full"
                    />
                    Tóm tắt
                  </Heading>
                  <Text
                    bg="blue.50"
                    p={4}
                    borderRadius="lg"
                    borderLeft="4px solid"
                    borderColor="blue.500"
                    fontStyle="italic"
                    color="gray.700"
                    fontSize="lg"
                  >
                    {selectedNews.summary}
                  </Text>
                </Box>

                {/* --- Full Content --- */}
                <Box w="full">
                  <Heading
                    size="md"
                    mb={3}
                    color="blue.700"
                    display="flex"
                    alignItems="center"
                  >
                    <Box
                      w="4px"
                      h="22px"
                      bg="blue.500"
                      mr={2}
                      borderRadius="full"
                    />
                    Nội dung chi tiết
                  </Heading>
                  <Box
                    bg="gray.50"
                    p={4}
                    borderRadius="lg"
                    maxH="400px"
                    overflowY="auto"
                  >
                    <Text
                      whiteSpace="pre-wrap"
                      lineHeight="1.7"
                      fontSize="md"
                      color="gray.800"
                    >
                      {selectedNews.link ||
                        "Không có nội dung chi tiết để hiển thị."}
                    </Text>
                  </Box>
                </Box>

                {/* --- Hashtags --- */}
                <Box w="full">
                  <Heading
                    size="md"
                    mb={3}
                    color="blue.700"
                    display="flex"
                    alignItems="center"
                  >
                    <Box
                      w="4px"
                      h="22px"
                      bg="blue.500"
                      mr={2}
                      borderRadius="full"
                    />
                    Hashtags
                  </Heading>
                  <Flex wrap="wrap" gap={2}>
                    {Array.isArray(selectedNews.hashtags) &&
                      selectedNews.hashtags.map((tag, i) => (
                        <Tag
                          key={i}
                          size="md"
                          colorScheme="blue"
                          variant="solid"
                          borderRadius="full"
                          px={4}
                          py={1.5}
                          fontWeight="600"
                        >
                          #{tag}
                        </Tag>
                      ))}
                  </Flex>
                </Box>
              </VStack>
            </ModalBody>

            <ModalFooter borderTop="1px solid" borderColor="gray.100">
              <Button
                onClick={onClose}
                colorScheme="blue"
                size="lg"
                px={8}
                borderRadius="md"
                _hover={{ transform: "scale(1.02)" }}
                transition="all 0.2s"
              >
                Đóng
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      )}
    </Box>
  );
};

const SectionBlock = ({ title, children }) => (
  <Box w="full">
    <Heading size="md" mb={3} color="blue.700" display="flex" alignItems="center">
      <Box w="4px" h="22px" bg="blue.500" mr={2} borderRadius="full" />
      {title}
    </Heading>
    {children}
  </Box>
);

const BadgeInfo = ({ label, value, icon, colorScheme = "blue", badge }) => (
  <HStack spacing={2} align="center">
    <Icon as={icon} color={`${colorScheme}.500`} boxSize={5} />
    <Text fontWeight="600" color="gray.600">{label}:</Text>
    <Text color="gray.800">{value}</Text>
    {badge}
  </HStack>
);

export default NewsTable;