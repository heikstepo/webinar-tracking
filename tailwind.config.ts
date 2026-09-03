import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0b0d12",
        panel: "#141821",
        edge: "#222836",
        accent: "#5b8cff",
        hyros: "#5348f2",
      },
    },
  },
  plugins: [],
};
export default config;
