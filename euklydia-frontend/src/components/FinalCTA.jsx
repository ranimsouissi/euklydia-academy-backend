import Container from "./ui/Container";
import Button from "./ui/Button";

export default function FinalCTA() {
  return (
    <section style={{ padding: "86px 0", background: "#0b1220" }}>
      <Container>
        <div
          style={{
            borderRadius: "var(--radius)",
            padding: 28,
            background: "linear-gradient(180deg, rgba(37,99,235,0.22), rgba(11,18,32,1))",
            border: "1px solid rgba(226,232,240,0.15)",
            boxShadow: "var(--shadow)",
          }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1.2fr 0.8fr",
              gap: 22,
              alignItems: "center",
            }}
          >
            {/* Left */}
            <div>
              <div style={{ color: "rgba(255,255,255,0.85)", fontWeight: 900, marginBottom: 10 }}>
                Ready to start?
              </div>

              <h2 style={{ color: "#fff", fontSize: 40, margin: "0 0 12px", lineHeight: 1.08 }}>
                Accelerate your AI transformation with Euklydia
              </h2>

              <p style={{ color: "rgba(255,255,255,0.75)", margin: 0, lineHeight: 1.7, fontSize: 16 }}>
                Run the diagnostic, generate the right learning path, and track progress with a clear maturity dashboard.
              </p>

              <div style={{ display: "flex", gap: 12, marginTop: 22, flexWrap: "wrap" }}>
                <Button>Start AI diagnostic</Button>
                <Button variant="outline">Request a demo</Button>
              </div>

              <div style={{ marginTop: 14, color: "rgba(255,255,255,0.65)", fontSize: 14 }}>
                No commitment • Clear roadmap • Designed for leaders & organizations
              </div>
            </div>

            {/* Right mini card */}
            <div
              style={{
                borderRadius: "var(--radius)",
                border: "1px solid rgba(226,232,240,0.15)",
                background: "rgba(255,255,255,0.06)",
                padding: 18,
              }}
            >
              <div style={{ color: "#fff", fontWeight: 900, marginBottom: 12 }}>
                What you get
              </div>

              <div style={{ display: "grid", gap: 10 }}>
                {[
                  "AI maturity score",
                  "Top skill gaps",
                  "Personalized pathway",
                  "Progress dashboard",
                ].map((x) => (
                  <div
                    key={x}
                    style={{
                      borderRadius: 14,
                      padding: "10px 12px",
                      border: "1px solid rgba(226,232,240,0.12)",
                      background: "rgba(255,255,255,0.05)",
                      color: "rgba(255,255,255,0.85)",
                      fontWeight: 700,
                    }}
                  >
                    ✔ {x}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* responsive */}
          <style>{`
            @media (max-width: 900px) {
              section > div > div {
                grid-template-columns: 1fr !important;
              }
            }
          `}</style>
        </div>
      </Container>
    </section>
  );
}