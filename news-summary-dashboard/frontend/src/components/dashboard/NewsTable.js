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
  Spinner
} from "@chakra-ui/react";
import { FaRegBookmark, FaBookmark } from "react-icons/fa";
import { supabase } from "../../services/supabaseClient";

const NewsTable = () => {
  // State for data, loading, and error handling
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // State for UI interactions
  const [bookmarks, setBookmarks] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // useEffect hook to fetch data from Supabase when the component mounts
  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      setError(null);

      try {
        // Fetch data from the 'news_articles' table in Supabase
        const { data, error: dbError } = await supabase
          .from("fireant_data")
          .select("*") // Select all columns
          .order("date", { ascending: false }); // Order by date, newest first

        if (dbError) {
          // If Supabase returns an error, throw it to be caught by the catch block
          throw dbError;
        }

        // Set the fetched data to our state
        setNewsData(data || []);
        // Initialize bookmarks based on the number of fetched items
        setBookmarks(Array((data || []).length).fill(false));
      } catch (err) {
        // If any error occurs, update the error state
        console.error("Error fetching data:", err.message);
        setError("Không thể tải dữ liệu tin tức. Vui lòng thử lại sau.");
      } finally {
        // Set loading to false after the fetch attempt is complete
        setLoading(false);
      }
    };

    fetchNews();
  }, []); // The empty dependency array ensures this effect runs only once

  const handleBookmark = (idx) => {
    setBookmarks((bm) => {
      const copy = [...bm];
      copy[idx] = !copy[idx];
      return copy;
    });
  };

  // --- Render logic ---

  // Display a loading spinner while data is being fetched
  if (loading) {
    return (
      <Flex justify="center" align="center" height="400px">
        <Spinner
          thickness="4px"
          speed="0.65s"
          emptyColor="gray.200"
          color="blue.500"
          size="xl"
        />
        <Text ml={4} fontSize="lg">
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

  return (
    <Box>
      <Box overflowX="auto">
        <Table variant="simple" width="100%">
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
              <Th w="16%" fontSize="lg" fontWeight="bold" textTransform="none">
                Ngành
              </Th>
              <Th w="20%" fontSize="lg" fontWeight="bold" textTransform="none">
                Tiêu đề
              </Th>
              <Th w="30%" fontSize="lg" fontWeight="bold" textTransform="none">
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
                <Td w="16%">
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
                    <Box cursor="pointer" maxW="120px">
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
                            whiteSpace="nowrap"
                            userSelect="none"
                            fontWeight="medium"
                            width="fit-content"
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
                <Td w="20%">
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
                <Td w="30%">
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
                    <Text>{row.summary_token_count}</Text>
                    <Box w="30px" h="20px" bg={row.color} borderRadius="sm" />
                  </HStack>
                </Td>
                {/* Hashtags */}
                <Td w="12%">
                  <Tooltip
                    label={
                      Array.isArray(row.sentiment)
                        ? row.sentiment.join(" ")
                        : ""
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
                    <Box cursor="pointer" maxW="100px">
                      <Flex direction="column" gap={1} align="flex-start">
                        {Array.isArray(row.sentiment) &&
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
                        {Array.isArray(row.sentiment) &&
                          row.sentiment.length > 2 && (
                            <Tag
                              size="sm"
                              colorScheme="gray"
                              variant="subtle"
                              whiteSpace="nowrap"
                              userSelect="none"
                              width="fit-content"
                            >
                              +{row.sentiment.length - 2}
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
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          isDisabled={currentPage === 1}
          size="sm"
        >
          Trang trước
        </Button>
        <Text alignSelf="center">
          Trang {currentPage} / {totalPages > 0 ? totalPages : 1}
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