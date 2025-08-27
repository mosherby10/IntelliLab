const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function login(username, password) {
  const data = new URLSearchParams();
  data.append('username', username);
  data.append('password', password);
  const resp = await fetch(`${API_URL}/auth/token`, {
    method: 'POST',
    body: data
  });
  if (!resp.ok) throw new Error('Login failed');
  return resp.json();
}

export async function askQA(token, question, context) {
  const resp = await fetch(`${API_URL}/nlp/qa`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ question, context })
  });
  if (!resp.ok) throw new Error('NLP request failed');
  return resp.json();
}
