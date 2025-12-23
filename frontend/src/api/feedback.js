import axios from "axios";
import { API_BASE_URL } from "./config";

const API = `${API_BASE_URL}/feedback`;

// Configurar axios per enviar cookies
axios.defaults.withCredentials = true;

export const saveFeedback = async (feedbackData) => {
  const res = await axios.post(`${API}/`, feedbackData);
  return res.data;
};

export const getFeedbackStats = async () => {
  const res = await axios.get(`${API}/stats`);
  return res.data;
};
