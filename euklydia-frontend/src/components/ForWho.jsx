import Container from "./ui/Container";

export default function ForWho() {
  const cards = [
    {
      title: "For Leaders",
      bullets: [
        "Maturity score & priorities",
        "Governance & operating model",
        "ROI and KPI measurement",
        "Decision-ready frameworks",
      ],
    },
    {
      title: "For Teams",
      bullets: [
        "Role-based learning paths",
        "Workflow automation and playbooks",
        "Execution templates & deliverables",
        "Progress tracking by skills",
      ],
    },
  ];

  return (
    <section id="enterprise" style={{ padding: "84px 0", background: "#f8fafc" }}>
      <Container>
        <div style={{ maxWidth: 920, margin: "0 auto", textAlign: "center" }}>
          <div style={{ color: "#006355", fontWeight: 900, marginBottom: 10 }}>
            Built for impact
          </div>
          <h2 style={{ fontSize: 38, fontWeight: 900, margin: "0 0 12px", lineHeight: 1.1, color: "#0B3C3B" }}>
            Built for leaders and teams
          </h2>
          <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7 }}>
            Whether you drive strategy or execute delivery, Euklydia adapts to your responsibilities.
          </p>
        </div>

        <div style={{ marginTop: 34, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
          {cards.map((c) => (
            <div
              key={c.title}
              style={{
                background: "#fff",
                border: "1px solid rgba(15,23,42,0.06)",
                borderRadius: 24,
                padding: 26,
                boxShadow: "0 18px 55px rgba(2,6,23,0.06)",
              }}
            >
              <div style={{ fontWeight: 900, fontSize: 18, color: "#0B3C3B", marginBottom: 14 }}>
                {c.title}
              </div>
              <div style={{ display: "grid", gap: 10 }}>
                {c.bullets.map((b) => (
                  <div
                    key={b}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 10,
                      padding: "10px 12px",
                      borderRadius: 16,
                      background: "#f8fafc",
                      border: "1px solid rgba(15,23,42,0.06)",
                      fontWeight: 800,
                      color: "#0B3C3B",
                    }}
                  >
                    <span style={{ color: "#00B3A0", fontWeight: 900 }}>•</span>
                    {b}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <style>{`
          @media (max-width: 980px) {
            section#enterprise > div > div:last-of-type {
              grid-template-columns: 1fr !important;
            }
          }
        `}</style>
      </Container>
    </section>
  );
}