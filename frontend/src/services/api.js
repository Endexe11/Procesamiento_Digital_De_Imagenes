import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api"; // Base URL del backend
const API_TIMEOUT = 5000; // Timeout en milisegundos

const apiService = {
  async connectDevice() {
    try {
      const response = await axios.post(`${API_BASE_URL}/devices/connect`, {}, { timeout: API_TIMEOUT });
      return response.data;
    } catch (error) {
      console.error("Error connecting device:", error);
      throw error;
    }
  },

  async uploadImage(imageData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/images/upload`, { image: imageData }, { timeout: API_TIMEOUT });
      return response.data;
    } catch (error) {
      console.error("Error uploading image:", error);
      throw error;
    }
  },

  async downloadImage(imageUrl) {
    try {
      const response = await axios.post(`${API_BASE_URL}/images/download`, { imageUrl }, { timeout: API_TIMEOUT });
      return response.data;
    } catch (error) {
      console.error("Error downloading image:", error);
      throw error;
    }
  },

  async processImage() {
    try {
      const response = await axios.post(`${API_BASE_URL}/images/process`, {}, { timeout: API_TIMEOUT });
      return response.data;
    } catch (error) {
      console.error("Error processing image:", error);
      throw error;
    }
  },
};

export default apiService;