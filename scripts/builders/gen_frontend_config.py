import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    # 1. package.json
    write_file("frontend/package.json", """{
  "name": "sentinel-grid-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.344.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.6"
  }
}""")

    # 2. vite.config.ts
    write_file("frontend/vite.config.ts", """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, host: true }
});""")

    # 3. tailwind.config.js
    write_file("frontend/tailwind.config.js", """/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        sentinel: {
          dark: "#0a0d14",
          surface: "#111726",
          card: "#161f36",
          border: "#243254",
          cyan: "#00f0ff"
        }
      }
    }
  },
  plugins: []
};""")

    # 4. index.html
    write_file("frontend/index.html", """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SENTINEL GRID — 2D Adaptive Tower Defense</title>
  </head>
  <body class="bg-[#0a0d14] text-slate-100 overflow-hidden">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>""")

    # 5. src/main.tsx
    write_file("frontend/src/main.tsx", """import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""")

    # 6. src/index.css
    write_file("frontend/src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  padding: 0;
  user-select: none;
}""")

if __name__ == "__main__":
    generate()
