/** @type {import("tailwindcss").Config} */
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
};