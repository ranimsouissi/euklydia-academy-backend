import Container from "./ui/Container";

const metrics = [
  {
    icon: "↗",
    value: "4",
    label: "AI Focus Areas",
    sub: "Literacy · Prompting · Evaluation · Integration",
  },
  {
    icon: "+",
    value: "12",
    label: "Core AI Skills",
    sub: "Across all professional roles",
  },
  {
    icon: "+",
    value: "3–4",
    label: "Modules per Skill",
    sub: "20–30 min sessions, at your pace",
  },
  {
    icon: "↗",
    value: "10 min",
    label: "To your roadmap",
    sub: "Personalized · Not generic · Ready instantly",
  },
];

export default function Metrics() {
  return (
    <section style={{ padding: "0 0 24px", background: "transparent" }}>
      <Container>
        <div
          style={{
            position: "relative",
            zIndex: 5,
            background: "#004E4C",
            borderRadius: 28,
            padding: 24,
            boxShadow: "0 20px 60px rgba(0,0,0,0.18)",
            overflow: "hidden",
          }}
        >
          <div
            className="metricsGrid"
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: 18,
            }}
          >
            {metrics.map((m, index) => (
              <div
                key={m.label}
                style={{
                  background: index === 0 ? "#006355" : "#ffffff",
                  color: index === 0 ? "#fff" : "#111",
                  borderRadius: 18,
                  padding: "22px 18px",
                  textAlign: "center",
                  boxShadow: index === 0 ? "0 10px 30px rgba(0,99,85,0.35)" : "none",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                {/* Icône */}
                <div
                  style={{
                    width: 34, height: 34, borderRadius: 10,
                    display: "grid", placeItems: "center",
                    marginBottom: 10,
                    background: index === 0 ? "rgba(255,255,255,0.18)" : "rgba(0,179,160,0.15)",
                    color: index === 0 ? "#fff" : "#006355",
                    fontWeight: 900, fontSize: 18,
                  }}
                >
                  {m.icon}
                </div>

                {/* Valeur */}
                <div style={{
                  fontSize: index === 3 ? 24 : 30,
                  fontWeight: 900,
                  marginBottom: 4,
                  lineHeight: 1,
                }}>
                  {m.value}
                </div>

                {/* Label */}
                <div style={{
                  fontWeight: 700,
                  fontSize: 13,
                  opacity: 0.85,
                  marginBottom: 6,
                }}>
                  {m.label}
                </div>

                {/* Sous-texte */}
                <div style={{
                  fontSize: 11,
                  fontWeight: 500,
                  opacity: 0.55,
                  lineHeight: 1.5,
                }}>
                  {m.sub}
                </div>
              </div>
            ))}
          </div>
        </div>

        <style>{`
          @media (max-width: 900px) {
            .metricsGrid { grid-template-columns: repeat(2, 1fr) !important; }
          }
          @media (max-width: 520px) {
            .metricsGrid { grid-template-columns: 1fr !important; }
          }
        `}</style>
      </Container>
    </section>
  );
}
