const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

let authToken = null;

export function setAuthToken(token) {
  authToken = token ?? null;
}

function withAuth(headers = {}) {
  if (authToken) {
    return { ...headers, Authorization: `Bearer ${authToken}` };
  }
  return headers;
}

async function request(path, { method = 'GET', headers = {}, body } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: withAuth(headers),
    body,
  });

  let data = null;
  const isJson = response.headers.get('content-type')?.includes('application/json');

  if (isJson) {
    data = await response.json().catch(() => null);
  }

  if (!response.ok) {
    const detail = data?.detail || data?.message || `Request failed: ${response.status}`;
    throw new Error(detail);
  }

  return data;
}

function jsonBody(payload) {
  return JSON.stringify(payload);
}

export function fetchWorkspace() {
  return request('/workspace');
}

export function createProject(payload) {
  return request('/workspace/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonBody(payload),
  });
}

export function updateProject(projectId, payload) {
  return request(`/workspace/projects/${projectId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: jsonBody(payload),
  });
}

export function deleteProject(projectId) {
  return request(`/workspace/projects/${projectId}`, {
    method: 'DELETE',
  });
}

export function createTask(projectId, payload) {
  return request(`/workspace/projects/${projectId}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonBody(payload),
  });
}

export function deleteTask(taskId) {
  return request(`/workspace/tasks/${taskId}`, {
    method: 'DELETE',
  });
}

export function runDecisionTask(payload) {
  return request('/decision/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonBody(payload),
  });
}

export function fetchDecisionStatus(runId) {
  return request(`/decision/status/${runId}`);
}

export function fetchDecisionResult(runId) {
  return request(`/decision/result/${runId}`);
}
