import React, { useState } from "react";
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
  Flex
} from "@chakra-ui/react";
import { FaRegBookmark, FaBookmark } from "react-icons/fa";

const newsData = [
  {
    date: "5/24/2023",
    industry: ["Technology", "Healthcare", "Agriculture"],
    title: "Gỡ nút thắt cho xuất khẩu sầu riêng sang Trung Quốc",
    subtitle:
      "Lập chốt kiểm dịch tại vườn, siết phân bón lậu, cải tạo đất là những cách có thể giúp Việt Nam giành lại lợi thế khi xuất khẩu sầu riêng sang Trung Quốc. Sau thời kỳ bùng nổ, sầu riêng - 'ngôi sao' mới của nông sản Việt - đang đối mặt hàng loạt rào cản như gian lận mã số vùng trồng, tiêu chuẩn siết chặt và sự cạnh tranh gay gắt từ Thái Lan, Philippines, lẫn sầu riêng nội địa Trung Quốc. Bài toán giữ thị phần và phát triển bền vững trở nên cấp thiết.",
    score: 62,
    hashtags: ["#AI", "#startups", "#healthcare", "#healthcare", "#healthcare"],
    color: "yellow.300",
  },
  {
    date: "5/24/2023",
    industry: ["Technology", "Healthcare", "Agriculture"],
    title: "Đồ chơi Labubu đắt hàng tại Mỹ bất chấp thuế quan",
    subtitle:
      "Bất chấp áp lực thuế quan hay niềm tin tiêu dùng yếu, Labubu là món đồ chơi Trung Quốc 'gây nghiện' của người dân Mỹ. Với đôi mắt to, nụ cười tinh quái, Labubu - đồ chơi nhồi bông lấy cảm hứng từ yêu tinh Bắc Âu - đang tạo ra cơn sốt với người tiêu dùng Mỹ. Lin, sinh viên y khoa tại Nebraska, sở hữu hàng chục mẫu Labubu. Tại Mỹ, món đồ chơi nhồi bông này có thể được bán từ vài chục đến hàng trăm USD trên các nền tảng trực tuyến, nhưng người hâm mộ sẵn sàng chi tiền. Lin từng chi hàng trăm USD và dành hàng giờ xem TikTok Live để săn một con Zimomo cao 22 inch có đuôi gai. 'Nó quá hot, đúng chuẩn một món đồ xa xỉ', cô nói.",
    score: 63,
    hashtags: ["#markets"],
    color: "yellow.300",
  },
  {
    date: "5/23/2023",
    industry: ["Finance"],
    title: "Ấn Độ muốn tăng gấp rưỡi sản lượng 'thép xám'",
    subtitle:
      "Ấn Độ muốn tăng gấp rưỡi sản lượng vào năm 2030, nhưng đang phụ thuộc vào công nghệ cũ với 1 tấn thép thải 2,6 tấn CO2. Theo báo cáo ngày 20/5 của Global Energy Monitor (GEM), tổ chức theo dõi các dự án năng lượng toàn cầu, kế hoạch tăng sản lượng thép lên 330 triệu tấn mỗi năm của Ấn Độ có thể gây áp lực lên mục tiêu giảm khí nhà kính của nước này cũng như toàn cầu.",
    score: 81,
    hashtags: ["#renewables"],
    color: "green.300",
  },
  {
    date: "5/23/2023",
    industry: ["Energy", "Healthcare", "Agriculture"],
    title: "Elon Musk phủ nhận khả năng rời Tesla",
    subtitle:
      "Người giàu nhất thế giới khẳng định vẫn điều hành hãng xe điện Tesla trong 5 năm tới, trừ phi ông không còn. Ngày 20/4, phát biểu tại một sự kiện tại Doha (Qatar), tỷ phú Elon Musk cho biết ông vẫn có ý định làm CEO Tesla thêm ít nhất 5 năm nữa, 'trừ phi tôi qua đời'. Tuyên bố này đã xóa bỏ tin đồn ông có thể sớm bị thay thế. Tin đồn xuất hiện từ cuối tháng 4, rằng Hội đồng quản trị (HĐQT) Tesla bắt đầu tìm CEO mới từ đầu tháng 3. WSJ đưa tin HĐQT hãng xe điện đã liên lạc với một số công ty tuyển dụng để tìm người kế nhiệm cho Musk. Nguyên nhân là họ lo ngại Musk bận rộn với công việc của Ban Hiệu suất Chính phủ (DOGE) và tình hình kinh doanh của Tesla cũng đi xuống trong quý I.",
    score: 48,
    hashtags: ["#energy", "#sustainable", "#healthcare"],
    color: "red.300",
  },
  {
    date: "5/22/2023",
    industry: ["Retail"],
    title: "Bán lẻ trực tuyến tăng trưởng mạnh",
    subtitle: "Doanh số bán hàng trực tuyến tăng 30% so với cùng kỳ.",
    score: 75,
    hashtags: [
      "#retail",
      "#ecommerce",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
    ],
    color: "green.300",
  },
  {
    date: "5/22/2023",
    industry: ["Manufacturing"],
    title: "Công nghiệp sản xuất phục hồi",
    subtitle: "Chỉ số sản xuất công nghiệp tăng 5% trong quý đầu.",
    score: 68,
    hashtags: ["#manufacturing", "#industry", "#healthcare", "#healthcare"],
    color: "yellow.300",
  },
  {
    date: "5/21/2023",
    industry: ["Real Estate"],
    title: "Thị trường bất động sản ổn định",
    subtitle: "Giá nhà đất duy trì ở mức hợp lý.",
    score: 55,
    hashtags: ["#realestate", "#property", "#healthcare"],
    color: "yellow.300",
  },
  {
    date: "5/21/2023",
    industry: ["Education"],
    title: "Đổi mới phương pháp giảng dạy",
    subtitle: "Áp dụng công nghệ mới vào giáo dục.",
    score: 72,
    hashtags: [
      "#education",
      "#technology",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
    ],
    color: "green.300",
  },
  {
    date: "5/20/2023",
    industry: ["Transportation"],
    title: "Phát triển giao thông công cộng",
    subtitle: "Mở rộng mạng lưới xe buýt nhanh.",
    score: 65,
    hashtags: [
      "#transport",
      "#public",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
    ],
    color: "yellow.300",
  },
  {
    date: "5/20/2023",
    industry: ["Agriculture"],
    title: "Nông nghiệp thông minh",
    subtitle: "Ứng dụng IoT trong sản xuất nông nghiệp.",
    score: 58,
    hashtags: [
      "#agriculture",
      "#smartfarming",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
    ],
    color: "green.300",
  },
  {
    date: "5/20/2023",
    industry: ["Agriculture"],
    title: "Nông nghiệp thông minh",
    subtitle: "Ứng dụng IoT trong sản xuất nông nghiệp.",
    score: 58,
    hashtags: [
      "#agriculture",
      "#smartfarming",
      "#healthcare",
      "#healthcare",
      "#healthcare",
      "#healthcare",
    ],
    color: "green.300",
  },
];

const NewsTable = () => {
  const [bookmarks, setBookmarks] = useState(Array(newsData.length).fill(false));
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");

  const handleBookmark = idx => {
    setBookmarks(bm => {
      const copy = [...bm];
      copy[idx] = !copy[idx];
      return copy;
    });
  };

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
              <Th w="2%" fontSize="lg" fontWeight="bold" textTransform="none"></Th>
              <Th w="10%" fontSize="lg" fontWeight="bold" textTransform="none">Ngày</Th>
              <Th w="16%" fontSize="lg" fontWeight="bold" textTransform="none">Ngành</Th>
              <Th w="20%" fontSize="lg" fontWeight="bold" textTransform="none">Tiêu đề</Th>
              <Th w="30%" fontSize="lg" fontWeight="bold" textTransform="none">Tóm tắt</Th>
              <Th w="10%" fontSize="lg" fontWeight="bold" textTransform="none">Ảnh hưởng</Th>
              <Th w="12%" fontSize="lg" fontWeight="bold" textTransform="none">Hashtags</Th>
            </Tr>
          </Thead>
          <Tbody>
            {currentData.map((row, idx) => (
              <Tr key={idx} _hover={{ bg: "gray.50" }} height="110px" minHeight="110px">
                {/* Bookmark */}
                <Td w="2%" textAlign="center">
                  <IconButton
                    icon={bookmarks[startIndex + idx] ? <FaBookmark /> : <FaRegBookmark />}
                    color={bookmarks[startIndex + idx] ? "yellow.400" : "blue.500"}
                    variant="ghost"
                    size="sm"
                    onClick={() => handleBookmark(startIndex + idx)}
                    aria-label={bookmarks[startIndex + idx] ? "Bỏ bookmark" : "Đánh dấu bookmark"}
                  />
                </Td>
                {/* Date */}
                <Td w="10%">{row.date}</Td>
                {/* Industry */}
                <Td w="16%">
                <Tooltip
                  label={Array.isArray(row.industry) ? row.industry.join(", ") : row.industry}
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
                    <Flex direction="column" gap={1} align="flex-start" color="blue.500">
                      {(Array.isArray(row.industry) ? row.industry.slice(0, 2) : [row.industry]).map((item, i) => (
                        <Text key={i} whiteSpace="nowrap" userSelect="none" fontWeight="medium" width="fit-content">
                          {item}
                        </Text>
                      ))}
                      {Array.isArray(row.industry) && row.industry.length > 2 && (
                        <Text fontSize="sm" color="gray.500" width="fit-content">
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
                    <Text fontWeight="medium" noOfLines={2} cursor={row.title.length > 50 ? "pointer" : "default"}>
                      {row.title.length > 50 ? row.title.slice(0, 50) + "..." : row.title}
                    </Text>
                  </Tooltip>
                </Td>
                {/* Summary */}
                <Td w="30%">
                  <Tooltip 
                    label={row.subtitle} 
                    isDisabled={row.subtitle.length <= 80} 
                    placement="top-start" 
                    openDelay={300}
                    bg="blue.50"
                    color="gray.800"
                    borderRadius="md"
                    fontSize="sm"
                    px={4}
                    py={2}
                  >
                    <Text color="gray.600" noOfLines={2} cursor={row.subtitle.length > 80 ? "pointer" : "default"}>
                      {row.subtitle.length > 80 ? row.subtitle.slice(0, 80) + "..." : row.subtitle}
                    </Text>
                  </Tooltip>
                </Td>
                {/* Score */}
                <Td w="10%">
                  <HStack spacing={2}>
                    <Text>{row.score}</Text>
                    <Box w="30px" h="20px" bg={row.color} borderRadius="sm" />
                  </HStack>
                </Td>
                {/* Hashtags */}
                <Td w="12%">
                  <Tooltip
                    label={row.hashtags.join(" ")}
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
                        {row.hashtags.slice(0, 2).map((tag, i) => (
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
                        {row.hashtags.length > 2 && (
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
            {/* Thêm các dòng rỗng để giữ tổng dòng bằng itemsPerPage */}
            {Array(itemsPerPage - currentData.length).fill("").map((_, i) => (
              <Tr key={"empty-" + i} height="110px" minHeight="110px">
                <Td colSpan={7} />
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
      <Flex justify="center" mt={4} gap={2}>
        <Button
          onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
          isDisabled={currentPage === 1}
          size="sm"
        >
          Trang trước
        </Button>
        <Text alignSelf="center">
          Trang {currentPage} / {totalPages}
        </Text>
        <Button
          onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
          isDisabled={currentPage === totalPages}
          size="sm"
        >
          Trang sau
        </Button>
      </Flex>
    </Box>
  );
};

export default NewsTable; 