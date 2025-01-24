// axiosConfig.js
import axios from "axios";

// Get the base URL from the environment variable
const baseURL = process.env.REACT_APP_API_URL;

// Create an Axios instance with the base URL
const axiosInstance = axios.create({
  baseURL: baseURL, // Use the value from the .env file
  withCredentials: true,
});

export default axiosInstance;
