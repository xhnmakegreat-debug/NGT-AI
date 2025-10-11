const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

export async function runDecisionTask(payload) {
  const response = await fetch(`${API_BASE_URL}/decision/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to create decision task: ${response.status}`);
  }

  return response.json();
}

export async function fetchDecisionStatus(decisionId) {
  const response = await fetch(`${API_BASE_URL}/decision/status/${decisionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch decision status: ${response.status}`);
  }
  return response.json();
}

export async function fetchDecisionResult(decisionId) {
  const response = await fetch(`${API_BASE_URL}/decision/result/${decisionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch decision result: ${response.status}`);
  }
  return response.json();
}
