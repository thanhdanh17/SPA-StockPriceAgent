import React, { useState, useEffect } from "react";
import {
  Box,
  Heading,
  Select,
  Input,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Button,
  FormControl,
  FormLabel,
  HStack,
  VStack,
  Text,
  useColorModeValue,
  SliderMark,
  Container,
  Flex,
  ButtonGroup
} from "@chakra-ui/react";
import NewsTable from "../components/dashboard/NewsTable";
import IndustryDistributionChart from "../components/dashboard/IndustryDistributionChart";
import InfluenceTrendsChart from "../components/dashboard/InfluenceTrendsChart";
import TopbarIcons from "../components/layout/TopbarIcons";

const industryMap = {
  "Công nghệ": "Technology",
  "Sức khỏe": "Healthcare",
  "Tài chính": "Finance",
  "Năng lượng": "Energy",
  "Khác": "Other"
};

const translateIndustryToEnglish = (vietnameseName) => {
  // Nếu tìm thấy tên trong bộ từ điển thì trả về, nếu không thì trả về chính nó
  return industryMap[vietnameseName] || vietnameseName;
};

const industries = ["Công nghệ", "Sức khỏe", "Tài chính", "Năng lượng", "Khác"];

const DEFAULT_INDUSTRY = "";
const DEFAULT_DATE = new Date().toISOString().split('T')[0];
const DEFAULT_SENTIMENT = "";
const DEFAULT_SEARCH = "";

const DashboardPage = () => {
  // State cho các bộ lọc
  const [industry, setIndustry] = useState(DEFAULT_INDUSTRY);
  const [date, setDate] = useState(DEFAULT_DATE);
  const [sentiment, setSentiment] = useState(DEFAULT_SENTIMENT);
  const [search, setSearch] = useState(DEFAULT_SEARCH);

  // === Nâng state quản lý dữ liệu từ NewsTable lên đây ===
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // =======================================================

  const handleApplyFilters = async () => {
    setLoading(true);
    setError(null);

    // 1. "Dịch" tên ngành sang Tiếng Anh
    const industryInEnglish = translateIndustryToEnglish(industry);
    // Xây dựng URL với tham số industry
    const apiUrl = `http://127.0.0.1:5000/api/news?industry=${industryInEnglish}`;

    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error("Lỗi mạng hoặc server không phản hồi");
      }
      const data = await response.json();
      // console.log("Dữ liệu nhận được từ API:", data);
      setNewsData(data || []);
    } catch (err) {
      console.error("Error fetching data from API:", err.message);
      setError("Không thể tải dữ liệu tin tức. Vui lòng thử lại sau.");
    } finally {
      setLoading(false);
    }
  };

  // Tự động gọi API lần đầu khi trang được tải
  useEffect(() => {
    handleApplyFilters();
  }, []);

  const handleReset = async () => {
    setIndustry(DEFAULT_INDUSTRY);
    setDate(DEFAULT_DATE);
    setSentiment(DEFAULT_SENTIMENT);
    setSearch(DEFAULT_SEARCH);

    // 2. Tải lại toàn bộ dữ liệu gốc bằng cách gọi API không có filter
    setLoading(true);
    setError(null);
    // Sử dụng URL gốc, không thêm bất kỳ tham số nào
    const apiUrl = `http://127.0.0.1:5000/api/news`;

    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error("Lỗi mạng hoặc server không phản hồi");
      }
      const data = await response.json();
      setNewsData(data || []);
    } catch (err) {
      console.error("Error fetching data from API:", err.message);
      setError("Không thể tải dữ liệu tin tức. Vui lòng thử lại sau.");
    } finally {
      setLoading(false);
    }
  };

  const bgColor = useColorModeValue("white", "gray.800");

  return (
    <Box
      borderRadius="3xl"
      boxShadow="xl"
      bg={bgColor}
      maxW="container.2xl"
      w="100%"
      mx="auto"
      px={[2, 4, 8]}
      py={6}
    >
      <HStack justify="space-between" mb={8}>
        <Heading
          size="2xl"
          fontWeight="extrabold"
          color="gray.800"
          letterSpacing="tight"
        >
          Tin tức tổng hợp
        </Heading>
        <TopbarIcons />
      </HStack>

      <Container maxW="container.2xl" px={0} mb={6}>
        <Flex w="100%" align="flex-end" justify="space-between" gap={2}>
          {/*-----------------Industry-----------------*/}
          <FormControl minW="220px" maxW="220px">
            <FormLabel fontSize="lg" mb={1}>
              Ngành
            </FormLabel>
            <Select
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              bg="white"
              borderRadius="md"
              fontWeight="semibold"
              size="sm"
              h="40px"
              minH="40px"
              maxH="40px"
              placeholder="Tất cả"
            >
              {industries.map((ind) => (
                <option value={ind} key={ind}>
                  {ind}
                </option>
              ))}
            </Select>
          </FormControl>
          {/*-----------------Date Range-----------------*/}
          <FormControl minW="220px" maxW="220px">
            <FormLabel fontSize="lg" mb={1}>
              Ngày
            </FormLabel>
            <Input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              bg="white"
              borderRadius="md"
              size="sm"
              h="40px"
              minH="40px"
              maxH="40px"
            />
          </FormControl>

          {/*-----------------Influence-----------------*/}
          <FormControl minW="280px" maxW="280px">
            <FormLabel fontSize="lg" mb={1}>
              Ảnh hưởng
            </FormLabel>
            {/* isAttached nối các nút lại với nhau */}
            <ButtonGroup variant="outline" isAttached size="sm" h="40px">
              <Button
                onClick={() => setSentiment("positive")}
                // Làm nổi bật nút đang được chọn
                isActive={sentiment === "positive"}
                _active={{ bg: "blue.500", color: "white" }}
                minW="90px"
                h="40px"
              >
                Tích cực
              </Button>
              <Button
                onClick={() => setSentiment("negative")}
                isActive={sentiment === "negative"}
                _active={{ bg: "blue.500", color: "white" }}
                minW="90px"
                h="40px"
              >
                Tiêu cực
              </Button>
              <Button
                onClick={() => setSentiment("neutral")}
                isActive={sentiment === "neutral"}
                _active={{ bg: "blue.500", color: "white" }}
                minW="90px"
                h="40px"
              >
                Trung tính
              </Button>
            </ButtonGroup>
          </FormControl>
          {/*-----------------Search-----------------*/}
          <FormControl minW="220px" maxW="300px">
            <FormLabel fontSize="sm" mb={1} color="transparent">
              Tìm kiếm
            </FormLabel>
            <Input
              placeholder="Tìm kiếm"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              bg="white"
              borderRadius="md"
              size="sm"
              h="40px"
              minH="40px"
              maxH="40px"
            />
          </FormControl>
          <Button
            colorScheme="blue"
            minW="90px"
            h="40px"
            fontWeight="bold"
            fontSize="md"
            bgGradient="linear(to-r, blue.500, blue.600)"
            transition="all 0.2s cubic-bezier(.08,.52,.52,1)"
            boxShadow="sm"
            _hover={{
              bgGradient: "linear(to-r, blue.600, blue.500)",
              boxShadow: "md",
              transform: "translateY(-2px) scale(1.04)",
            }}
            _active={{ transform: "scale(0.96)", boxShadow: "xs" }}
            onClick={handleApplyFilters}
          >
            Áp dụng
          </Button>
          <Button
            variant="outline"
            minW="90px"
            h="40px"
            fontWeight="bold"
            fontSize="md"
            color="gray.700"
            borderColor="gray.200"
            transition="all 0.2s cubic-bezier(.08,.52,.52,1)"
            boxShadow="sm"
            _hover={{
              bg: "gray.50",
              borderColor: "gray.300",
              boxShadow: "md",
              transform: "translateY(-2px) scale(1.04)",
            }}
            _active={{ transform: "scale(0.96)", boxShadow: "xs" }}
            onClick={handleReset}
          >
            Đặt lại
          </Button>
        </Flex>
      </Container>

      <NewsTable newsData={newsData} loading={loading} error={error} />

      <HStack spacing={6} mt={6}>
        <IndustryDistributionChart />
        <InfluenceTrendsChart />
      </HStack>
    </Box>
  );
};

export default DashboardPage; 