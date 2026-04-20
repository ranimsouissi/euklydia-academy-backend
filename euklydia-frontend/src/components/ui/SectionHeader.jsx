export default function SectionHeader({ kicker, title, subtitle }) {
  return (
    <div style={{ maxWidth: 860 }}>
      {kicker && (
        <div style={{ color: "#006355", fontWeight: 900, marginBottom: 10 }}>
          {kicker}
        </div>
      )}

      <h2
        style={{
          fontSize: 42,
          fontWeight: 900,
          margin: "0 0 14px",
          lineHeight: 1.08,
          letterSpacing: -0.6,
          color: "#0B3C3B",
        }}
      >
        {title}
      </h2>

      {subtitle && (
        <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7, fontSize: 16 }}>
          {subtitle}
        </p>
      )}
    </div>
  );
}