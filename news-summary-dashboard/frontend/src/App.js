import React from "react";
import { Box, Container } from "@chakra-ui/react";
import NewsSummary from "./components/NewsSummary";
import Sidebar from "./components/Sidebar";

function App() {
  return (
    <Box display="flex" minH="100vh" bg="gray.50">
      <Sidebar />
      <Box flex="1" display="flex" flexDirection="column" minH="100vh">
        <Container maxW="container.xl" py={8} flex="1">
          <NewsSummary />
        </Container>
      </Box>
    </Box>
  );
}

export default App;
