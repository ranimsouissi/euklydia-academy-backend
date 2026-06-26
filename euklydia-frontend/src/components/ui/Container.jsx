// src/components/ui/Container.jsx
export default function Container({ children }) {
  return (
    <div
      style={{
        maxWidth: 1440,
        margin: "0 auto",
        width: "100%",
        boxSizing: "border-box",
        // Padding horizontal responsive : 16px mobile → 48px desktop
        padding: "0 clamp(16px, 4vw, 48px)",
      }}
    >
      {children}
    </div>
  );
}