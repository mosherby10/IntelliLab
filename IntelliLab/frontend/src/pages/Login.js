import React, { useState } from 'react';
import { login } from '../api';

export default function Login({ setToken }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);
    try {
      const data = await login(email, password);
      setToken(data.access_token);
    } catch (error) {
      setErr(error.message);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label><br />
          <input value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Password</label><br />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
        {err && <div style={{ color: 'red' }}>{err}</div>}
      </form>
    </div>
  );
}
