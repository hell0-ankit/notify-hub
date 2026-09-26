import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/notifications';

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getSettings = () => client.get('/settings/');
export const toggleChannel = (data) => client.post('/settings/toggle/', data);
export const getLogs = () => client.get('/logs/');
export const triggerEvent = (data) => client.post('/dispatch/', data);
export const registerDevice = (data) => client.post('/devices/', data);

export default client;