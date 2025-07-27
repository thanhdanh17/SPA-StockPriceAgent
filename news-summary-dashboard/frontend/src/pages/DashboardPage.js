import React, { useState } from "react";
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
  Flex
} from "@chakra-ui/react";
import NewsTable from "../components/dashboard/NewsTable";
import IndustryDistributionChart from "../components/dashboard/IndustryDistributionChart";
import InfluenceTrendsChart from "../components/dashboard/InfluenceTrendsChart";
import TopbarIcons from "../components/layout/TopbarIcons";


const industries = ["Công nghệ", "Sức khỏe", "Tài chính", "Năng lượng"];

const DEFAULT_INDUSTRY = "Công nghệ";
const DEFAULT_DATE = new Date().toISOString().split('T')[0];
const SCORE_MARKS = [0, 20, 40, 60, 80, 100];
const DEFAULT_SCORE = 0;
const DEFAULT_SEARCH = "";

const NewsSummary = () => {
  const [industry, setIndustry] = useState(DEFAULT_INDUSTRY);
  const [date, setDate] = useState(DEFAULT_DATE);
  const [score, setScore] = useState(DEFAULT_SCORE);
  const [search, setSearch] = useState(DEFAULT_SEARCH);
  const [showMark, setShowMark] = useState(false);

  const handleReset = () => {
    setIndustry(DEFAULT_INDUSTRY);
    setDate(DEFAULT_DATE);
    setScore(DEFAULT_SCORE);
    setSearch(DEFAULT_SEARCH);
  };

  const bgColor = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");

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
            <FormLabel fontSize="lg" mb={1}>Ngành</FormLabel>
            <Select value={industry} onChange={e => setIndustry(e.target.value)} bg="white" borderRadius="md" fontWeight="semibold" size="sm" h="40px" minH="40px" maxH="40px">
              {industries.map((ind) => (
                <option value={ind} key={ind}>{ind}</option>
              ))}
            </Select>
          </FormControl>
          {/*-----------------Date Range-----------------*/}
          <FormControl minW="220px" maxW="220px">
            <FormLabel fontSize="lg" mb={1}>Ngày</FormLabel>
            <Input type="date" value={date} onChange={e => setDate(e.target.value)} bg="white" borderRadius="md" size="sm" h="40px" minH="40px" maxH="40px" />
          </FormControl>
          
          {/*-----------------Influence Score-----------------*/} 
          <FormControl minW="320px" maxW="320px">
            <FormLabel fontSize="lg" mb={1}>Điểm ảnh hưởng</FormLabel>
            <Box
              position="relative"
              borderWidth="1px"
              borderRadius="md"
              bg="white"
              h="40px"
              px={4}
            >
              <Slider
                pos="absolute"
                top="0"
                left="0"
                right="0"
                bottom="0"
                value={score}
                onChange={val =>
                  setScore(
                    SCORE_MARKS.reduce(
                      (prev, curr) =>
                        Math.abs(curr - val) < Math.abs(prev - val) ? curr : prev
                    )
                  )
                }
                min={0}
                max={100}
                step={null}
                colorScheme="blue"
                size="sm"
                h="100%"
                onChangeStart={() => setShowMark(true)}
                onChangeEnd={() => setShowMark(false)}
              >
                <SliderTrack borderRadius="md" bg="gray.100">
                  <SliderFilledTrack />
                </SliderTrack>
                <SliderThumb boxSize={4} />

                {SCORE_MARKS.map(mark => (
                  <SliderMark
                    key={mark}
                    value={mark}
                    pos="absolute"
                    bottom="-1px"                  // Kéo sát đáy khung
                    left={`${mark}%`}            // Đặt ngang theo % giá trị
                    transform="translateX(-50%)" // Căn giữa ngang
                    fontSize="xs"
                    color="gray.500"
                    userSelect="none"
                  >
                    {mark}
                  </SliderMark>
                ))}
              </Slider>
            </Box>
          </FormControl>
          {/*-----------------Search-----------------*/}
          <FormControl minW="140px" maxW="200px">
            <FormLabel fontSize="sm" mb={1} color="transparent">Tìm kiếm</FormLabel>
            <Input placeholder="Tìm kiếm" value={search} onChange={e => setSearch(e.target.value)} bg="white" borderRadius="md" size="sm" h="40px" minH="40px" maxH="40px" />
          </FormControl>
          <Button colorScheme="blue" minW="90px" h="40px" fontWeight="bold" fontSize="md" bgGradient="linear(to-r, blue.500, blue.600)" transition="all 0.2s cubic-bezier(.08,.52,.52,1)" boxShadow="sm" _hover={{ bgGradient: "linear(to-r, blue.600, blue.500)", boxShadow: "md", transform: "translateY(-2px) scale(1.04)" }} _active={{ transform: "scale(0.96)", boxShadow: "xs" }}>Áp dụng</Button>
          <Button variant="outline" minW="90px" h="40px" fontWeight="bold" fontSize="md" color="gray.700" borderColor="gray.200" transition="all 0.2s cubic-bezier(.08,.52,.52,1)" boxShadow="sm" _hover={{ bg: "gray.50", borderColor: "gray.300", boxShadow: "md", transform: "translateY(-2px) scale(1.04)" }} _active={{ transform: "scale(0.96)", boxShadow: "xs" }} onClick={handleReset}>Đặt lại</Button>
        </Flex>
      </Container>

      <NewsTable />

      <HStack spacing={6} mt={6}>
        <IndustryDistributionChart />
        <InfluenceTrendsChart />
      </HStack>
    </Box>
  );
};

export default NewsSummary; 