import React, { useState } from 'react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

function App() {
  const [token, setToken] = useState(null);

  // If not logged in show login page. After login we get a token.
  if (!token) return <Login setToken={setToken} />;

  return <Dashboard token={token} />;
}

export default App;
