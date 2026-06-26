/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      // ─── Couleurs Euklydia ──────────────────────────────────────────
      colors: {
        euk: {
          dark: "#0B3C3B",
          deep: "#004E4C",
          primary: "#006355",
          mid: "#39A193",
          accent: "#00B3A0",
          soft: "#F0F9F7",
          border: "#D6EAE5",
        },
      },

      // ─── Largeur maximale du contenu ────────────────────────────────
      maxWidth: {
        page: "1440px",
        content: "1200px",
      },

      // ─── Échelle typographique RECALIBRÉE ───────────────────────────
      // Plus équilibrée pour écrans 1920px — titres moins écrasants
      fontSize: {
        // Hero — 3 breakpoints progressifs, plafonné à 64px sur large screen
        "hero-sm": ["2rem",    { lineHeight: "1.15", letterSpacing: "-0.02em", fontWeight: "800" }],   // 32px mobile
        "hero-md": ["2.75rem", { lineHeight: "1.1",  letterSpacing: "-0.02em", fontWeight: "800" }],   // 44px tablet
        "hero-lg": ["4rem",    { lineHeight: "1.05", letterSpacing: "-0.02em", fontWeight: "800" }],   // 64px desktop ← était 80px

        // Titres de page secondaires
        "display": ["2.5rem",  { lineHeight: "1.15", letterSpacing: "-0.01em", fontWeight: "800" }],   // 40px ← était 56px
        "section": ["2rem",    { lineHeight: "1.2",  letterSpacing: "-0.01em", fontWeight: "800" }],   // 32px ← était 40px
      },

      // ─── Espacements verticaux ──────────────────────────────────────
      spacing: {
        "section-y": "5rem",
        "section-y-lg": "7rem",
      },

      // ─── Shadows ────────────────────────────────────────────────────
      boxShadow: {
        "soft": "0 1px 3px rgba(11, 60, 59, 0.04), 0 1px 2px rgba(11, 60, 59, 0.03)",
        "card": "0 4px 12px rgba(11, 60, 59, 0.06), 0 2px 4px rgba(11, 60, 59, 0.04)",
        "elevated": "0 12px 32px rgba(11, 60, 59, 0.10), 0 4px 8px rgba(11, 60, 59, 0.05)",
      },
    },
  },
  plugins: [],
};