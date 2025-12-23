import axios from "axios";
import { API_BASE_URL } from "./config";

const API = `${API_BASE_URL}/auth`;

// Configurar axios per enviar cookies
axios.defaults.withCredentials = true;

export const register = async (name, username, email, password) => {
  const res = await axios.post(`${API}/register`, {
    name,
    username,
    email,
    password,
  });
  return res.data;
};

export const login = async (username, password) => {
  const res = await axios.post(`${API}/login`, {
    username,
    password,
  });
  return res.data;
};

export const logout = async () => {
  const res = await axios.post(`${API}/logout`, {});
  return res.data;
};

export const checkAuth = async () => {
  const res = await axios.get(`${API}/me`);
  return res.data;
};