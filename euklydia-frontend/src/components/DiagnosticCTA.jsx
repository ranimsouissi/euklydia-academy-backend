import Container from "./ui/Container";
import Button from "./ui/Button";

export default function DiagnosticCTA() {
  return (
    <section
      id="diagnostic"
      style={{
        padding: "72px 0",
        background:
          "linear-gradient(180deg, rgba(37,99,235,0.08) 0%, rgba(241,245,249,1) 65%)",
      }}
    >
      <Container>
        <div
          style={{
            borderRadius: "var(--radius)",
            border: "1px solid var(--border)",
            background: "#fff",
            boxShadow: "var(--shadow)",
            padding: 26,
            display: "grid",
            gridTemplateColumns: "1.2fr 0.8fr",
            gap: 18,
            alignItems: "center",
          }}
        >
          {/* Left */}
          <div>
            <div style={{ color: "var(--primary)", fontWeight: 900, marginBottom: 10 }}>
              AI Diagnostic
            </div>

            <h2 style={{ fontSize: 34, margin: "0 0 10px", lineHeight: 1.1 }}>
              Measure your AI maturity in minutes
            </h2>

            <p style={{ margin: 0, color: "var(--muted)", lineHeight: 1.6 }}>
              Identify gaps, get a maturity score, and receive an adaptive learning pathway aligned
              to your role and goals.
            </p>

            <div style={{ display: "flex", gap: 12, marginTop: 18, flexWrap: "wrap" }}>
              <Button>Take the AI Diagnostic</Button>
              <Button variant="outline">See sample report</Button>
            </div>

            <div style={{ display: "flex", gap: 14, marginTop: 16, color: "var(--muted)", fontSize: 14 }}>
              <span>✔ Skill gap mapping</span>
              <span>✔ Scoring model</span>
              <span>✔ Personalized pathway</span>
            </div>
          </div>

          {/* Right mock card */}
          <div
            style={{
              borderRadius: "var(--radius)",
              border: "1px solid var(--border)",
              background: "var(--soft)",
              padding: 18,
              minHeight: 180,
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div style={{ fontWeight: 800, color: "var(--text)" }}>Sample Outcome</div>

            <div style={{ display: "grid", gap: 10 }}>
              <div
                style={{
                  background: "#fff",
                  border: "1px solid var(--border)",
                  borderRadius: 14,
                  padding: 12,
                  display: "flex",
                  justifyContent: "space-between",
                  fontWeight: 700,
                }}
              >
                <span style={{ color: "var(--muted)" }}>AI Maturity</span>
                <span style={{ color: "var(--primary)" }}>Level 2</span>
              </div>

              <div
                style={{
                  background: "#fff",
                  border: "1px solid var(--border)",
                  borderRadius: 14,
                  padding: 12,
                  display: "flex",
                  justifyContent: "space-between",
                  fontWeight: 700,
                }}
              >
                <span style={{ color: "var(--muted)" }}>Top Gap</span>
                <span style={{ color: "var(--text)" }}>AI Strategy</span>
              </div>

              <div
                style={{
                  background: "#fff",
                  border: "1px solid var(--border)",
                  borderRadius: 14,
                  padding: 12,
                  display: "flex",
                  justifyContent: "space-between",
                  fontWeight: 700,
                }}
              >
                <span style={{ color: "var(--muted)" }}>Recommended Path</span>
                <span style={{ color: "var(--text)" }}>Business Leader</span>
              </div>
            </div>
          </div>
        </div>

        {/* responsive */}
        <style>{`
          @media (max-width: 900px) {
            section#diagnostic > div > div {
              grid-template-columns: 1fr !important;
            }
          }
        `}</style>
      </Container>
    </section>
  );
}