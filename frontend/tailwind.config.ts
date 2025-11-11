import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#2E3EBB",
          secondary: "#C9F8E3",
          background: "#F8F9FB"
        }
      },
      fontFamily: {
        vazir: ["Vazirmatn", "sans-serif"]
      }
    }
  },
  plugins: [require("@tailwindcss/forms"),
    plugin(function ({ addBase }) {
      addBase({
        body: {
          direction: "rtl",
          backgroundColor: "#F8F9FB"
        }
      });
    })
  ]
};

export default config;
