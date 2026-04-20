/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        euk: {
          dark: "#0B3C3B",
          deep: "#004E4C",
          primary: "#006355",
          mid: "#39A193",
          accent: "#00B3A0",
        },
      },
    },
  },
  plugins: [],
};