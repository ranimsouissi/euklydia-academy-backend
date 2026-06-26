import Container from "./ui/Container";
import { roles } from "../data/roles";

export default function ProfessionalRoles() {
  return (
    <section id="paths" style={{ padding: "80px 0", background: "#ffffff" }}>
      <Container>

        {/* Header — repositionné sur les use cases */}
        <div style={{ marginBottom: 32 }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 10,
            padding: "8px 14px", borderRadius: 999,
            border: "1px solid #E5E7EB", background: "rgba(0,179,160,0.08)",
            color: "#006355", fontWeight: 900, fontSize: 13, marginBottom: 12,
          }}>
            🎯 Use Cases by Role
          </div>
          <h2 style={{ fontSize: 36, margin: "0 0 10px", lineHeight: 1.12, letterSpacing: -0.5, fontWeight: 900, color: "#0f172a" }}>
            12 use cases organized in 4 professional roles
          </h2>
          <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7, fontSize: 16, maxWidth: 620 }}>
            Each role unlocks 3 measurable use cases with KPIs and ready-to-use AI blueprints. Pick the role that matches your day-to-day work.
          </p>
        </div>

        {/* Grid — 4 roles, 2×2 */}
        <div className="pathsGrid" style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
          {roles.map((r) => (
            <div
              key={r.id}
              className="pathCard"
              style={{
                background: "#fff",
                border: "1px solid #E5E7EB",
                borderRadius: 20, padding: 24,
                transition: "all 0.2s ease", position: "relative", overflow: "hidden",
                boxShadow: "0 4px 20px rgba(2,6,23,0.06)",
              }}
            >
              <div style={{
                position: "absolute", top: -20, right: -20,
                width: 70, height: 70, borderRadius: "50%",
                background: r.tagColor.bg, opacity: 0.6,
              }} />

              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <div style={{
                    display: "inline-flex", padding: "5px 10px", borderRadius: 999, marginBottom: 12,
                    background: r.tagColor.bg,
                    color: r.tagColor.color,
                    fontWeight: 800, fontSize: 11,
                  }}>
                    {r.tag}
                  </div>

                  <h3 style={{ margin: "0 0 4px", fontSize: 17, fontWeight: 900, color: "#0f172a" }}>
                    {r.title}
                  </h3>

                  <div style={{ fontSize: 12, fontWeight: 700, marginBottom: 8, color: "#94a3b8" }}>
                    {r.forWho}
                  </div>

                  <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "#64748b" }}>
                    {r.desc}
                  </p>
                </div>

                <div style={{
                  flexShrink: 0,
                  background: "rgba(0,179,160,0.08)",
                  borderRadius: 12, padding: "6px 10px",
                  textAlign: "center",
                  border: "1px solid rgba(0,179,160,0.15)",
                }}>
                  <div style={{ fontSize: 16, fontWeight: 900, color: "#006355" }}>3</div>
                  <div style={{ fontSize: 9, fontWeight: 700, color: "#64748b", lineHeight: 1.2 }}>use<br/>cases</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <style>{`
          .pathCard:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(2,6,23,0.10) !important; }
          @media (max-width: 768px) {
            .pathsGrid { grid-template-columns: 1fr !important; }
          }
        `}</style>

      </Container>
    </section>
  );
}