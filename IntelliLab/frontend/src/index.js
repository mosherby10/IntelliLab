import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Find the root element in public/index.html (create-react-app has it by default)
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
