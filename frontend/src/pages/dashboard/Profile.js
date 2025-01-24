import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../../config/axiosConfig";
import {
  Container,
  Typography,
  Box,
  CircularProgress,
  Button,
} from "@mui/material";
import UsersList from "../../components/UsersList";

const Profile  = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Assuming the server reads the JWT from cookies
        const response = await axiosInstance.get("/auth/profile");
        setUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        navigate("/login"); // Redirect to login if not authenticated
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = async () => {
   
  };
  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container>
      <Box textAlign="center" mt={4}>
        <Typography variant="h4">
          Welcome, {user?.username || "User"}!
        </Typography>
        <Typography variant="body1" mt={2}>
          Email: {user?.email}
        </Typography>
        <Typography variant="body1" mt={1}>
          Account Created: {new Date(user?.created_at).toLocaleString()}
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={handleLogout}
          sx={{ marginTop: 4 }}
        >
          Logout
        </Button>
      </Box>
      <UsersList />
    </Container>
  );
};

export default Profile;
