import Container from "./ui/Container";

export default function Footer() {
  const colTitle = { fontWeight: 900, marginBottom: 12 };
  const link = { margin: "10px 0", opacity: 0.85, cursor: "pointer" };

  return (
    <footer style={{ background: "#0B3C3B", color: "#fff", padding: "70px 0 28px" }}>
      <Container>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "2fr 1fr 1fr 1fr",
            gap: 40,
          }}
        >
          <div>
            <div style={{ fontWeight: 900, fontSize: 22, marginBottom: 10 }}>
              Euklydia <span style={{ color: "#00B3A0" }}>Academy</span>
            </div>
            <div style={{ opacity: 0.85, lineHeight: 1.7, maxWidth: 420 }}>
              AI maturity and decision intelligence for leaders and enterprises.
            </div>

            <div style={{ marginTop: 18, fontWeight: 900, opacity: 0.9 }}>Follow us</div>
            <div style={{ display: "flex", gap: 14, marginTop: 10 }}>
              {["in", "𝕏", "▶", "⎋"].map((i) => (
                <div
                  key={i}
                  style={{
                    width: 38,
                    height: 38,
                    borderRadius: 12,
                    background: "rgba(255,255,255,0.10)",
                    display: "grid",
                    placeItems: "center",
                    fontWeight: 900,
                  }}
                >
                  {i}
                </div>
              ))}
            </div>
          </div>

          <div>
            <div style={colTitle}>Product</div>
            <div style={link}>Platform</div>
            <div style={link}>AI Assessment</div>
            <div style={link}>Learning Paths</div>
            <div style={link}>Dashboard</div>
          </div>

          <div>
            <div style={colTitle}>Company</div>
            <div style={link}>About</div>
            <div style={link}>FAQ</div>
            <div style={link}>Contact</div>
          </div>

          <div>
            <div style={colTitle}>Legal</div>
            <div style={link}>Privacy Policy</div>
            <div style={link}>Terms of Service</div>
            <div style={link}>Cookie Policy</div>
          </div>
        </div>

        <div
          style={{
            marginTop: 40,
            paddingTop: 18,
            borderTop: "1px solid rgba(255,255,255,0.18)",
            display: "flex",
            justifyContent: "space-between",
            gap: 18,
            flexWrap: "wrap",
            opacity: 0.85,
          }}
        >
          <div>
            Made by <span style={{ color: "#00B3A0", fontWeight: 900 }}>EUKLYDIA</span> | AI Scaling Agency
          </div>
          <div>© 2026 Euklydia Academy</div>
        </div>

        <style>{`
          @media (max-width: 980px) {
            footer > div > div:first-child {
              grid-template-columns: 1fr 1fr !important;
            }
          }
          @media (max-width: 620px) {
            footer > div > div:first-child {
              grid-template-columns: 1fr !important;
            }
          }
        `}</style>
      </Container>
    </footer>
  );
}