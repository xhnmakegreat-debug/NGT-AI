import { setAuthToken } from './api.js';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

async function request(endpoint, payload) {
  const headers = { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const error = new Error(errorBody.detail || `Auth request failed: ${response.status}`);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

export async function registerWithEmail({ email, password, nickname }) {
  const data = await request('/auth/register', { email, password, nickname });
  setAuthToken(data.access_token);
  return data;
}

export async function loginWithEmail({ email, password }) {
  const data = await request('/auth/login', { email, password });
  setAuthToken(data.access_token);
  return data;
}
