import axios from "axios";
import { API_BASE_URL } from "./config";

const API = `${API_BASE_URL}/analyze`;

// Configurar axios per enviar cookies
axios.defaults.withCredentials = true;

export const analyzePhrase = async (text) => {
  const res = await axios.post(`${API}`, { text });
  return res.data;
};