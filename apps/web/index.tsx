import React from "react";
import App from "./src/App";
import { createRoot } from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';

// @ts-ignore
createRoot(document.getElementById("root")).render(<App />);
const rootElement = document.getElementById('root');
// @ts-ignore
const root = createRoot(rootElement);
root.render(<App />);