/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",
        secondary: "#1f2937",
        dark: "#0f172a",
        light: "#f8fafc",
      },
      backgroundColor: {
        base: "#000000",
      },
    },
  },
  plugins: [],
}