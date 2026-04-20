import { useState } from "react";

export default function Button({ children, variant = "primary", ...props }) {
  const [hover, setHover] = useState(false);

  const base = {
    padding: "12px 20px",
    borderRadius: 14,
    fontWeight: 800,
    fontSize: 14,
    border: "1px solid transparent",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 10,
    transition: "all 0.25s ease",
  };

  const variants = {
    primary: {
      background: hover ? "#004E4C" : "var(--primary)",
      color: "#fff",
      boxShadow: hover
        ? "0 10px 25px rgba(0, 99, 85, 0.25)"
        : "0 6px 16px rgba(0, 99, 85, 0.18)",
      transform: hover ? "translateY(-2px)" : "translateY(0)",
    },

    outline: {
      background: hover ? "#F5F7F7" : "#fff",
      color: "var(--text)",
      border: "1px solid var(--border)",
      boxShadow: hover ? "0 6px 14px rgba(2, 6, 23, 0.08)" : "none",
      transform: hover ? "translateY(-2px)" : "translateY(0)",
    },
  };

  return (
    <button
      style={{ ...base, ...variants[variant] }}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      {...props}
    >
      {children}
    </button>
  );
}