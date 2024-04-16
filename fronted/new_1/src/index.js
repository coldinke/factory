import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

const robotoFont = document.createElement('link');
robotoFont.rel = 'stylesheet';
robotoFont.href = 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap';
document.head.appendChild(robotoFont);

const root = createRoot(document.getElementById("root"))
root.render(
    <StrictMode>
        <App />
    </StrictMode>
);