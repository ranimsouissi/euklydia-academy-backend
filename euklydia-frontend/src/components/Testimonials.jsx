import Container from "./ui/Container";
import avatarSara from "../assets/images/avatar-sara.jpeg";
import avatarKarim from "../assets/images/avatar-karim.jpeg";
import avatarMehdi from "../assets/images/avatar-mehdi.jpeg";
import avatarYasmine from "../assets/images/avatar-yasmine.jpeg"; // ← à ajouter

const scenarios = [
  {
    avatar: avatarMehdi,
    name: "Mehdi Benali",
    role: "Sales Manager",
    company: "B2B SaaS · Tunis",
    roleTag: "AI Sales Specialist",
    roleColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
    borderColor: "#006355",
    rating: 5,
    useCase: "Lead Qualification Automation",
    quote:
      "I was sending the same generic outreach to every lead, with conversion stuck at 12%. After the diagnostic, Euklydia mapped exactly which use cases I needed to master. With the AI Lead Scoring Blueprint, I now qualify 35% more leads in half the time — and my outreach reply rate doubled.",
    highlight: "+35% qualified leads · 2x reply rate",
  },
  {
    avatar: avatarSara,
    name: "Sara Cherni",
    role: "Marketing Manager",
    company: "Fintech · Tunis",
    roleTag: "AI Marketing Strategist",
    roleColor: { bg: "rgba(212,83,126,0.10)", color: "#993556" },
    borderColor: "#993556",
    rating: 5,
    useCase: "Content Strategy Optimization",
    quote:
      "I was using ChatGPT randomly without a real strategy. The Euklydia diagnostic showed me exactly where I had gaps across 3 marketing use cases. With the AI Content Engine blueprint, I rebuilt our editorial calendar — engagement on our LinkedIn campaigns jumped by 40% in 3 weeks.",
    highlight: "+40% engagement in 3 weeks",
  },
  {
    avatar: avatarYasmine,
    name: "Yasmine Khelifi",
    role: "UX Designer",
    company: "Digital agency · Casablanca",
    roleTag: "AI Designer",
    roleColor: { bg: "rgba(127,119,221,0.10)", color: "#534AB7" },
    borderColor: "#534AB7",
    rating: 5,
    useCase: "Rapid Concept Generation",
    quote:
      "As a creative, I was skeptical AI could fit my workflow. The diagnostic broke my assumptions — it pinpointed exactly where AI accelerates ideation without replacing creativity. With the AI Design Ideation System, I now generate 10 concept variations in the time it took me to make 2.",
    highlight: "5x faster concept generation",
  },
  {
    avatar: avatarKarim,
    name: "Karim Aït Yahia",
    role: "Project Manager",
    company: "Consulting firm · Alger",
    roleTag: "AI Project Manager",
    roleColor: { bg: "rgba(56,130,221,0.10)", color: "#1a5fa8" },
    borderColor: "#1a5fa8",
    rating: 5,
    useCase: "Project Planning Automation",
    quote:
      "I used to spend 2 days building project roadmaps. The diagnostic revealed planning was my biggest gap across 3 PM use cases. With the AI Planning Engine blueprint, I now produce complete roadmaps in 4 hours — and my delivery delays dropped by 30%.",
    highlight: "60% time saved · -30% delays",
  },
];

export default function Testimonials() {
  return (
    <section id="testimonials" style={{ padding: "90px 0", background: "#F2FBF9" }}>
      <Container>

        {/* Header */}
        <div style={{ maxWidth: 720, marginBottom: 48 }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 10,
            padding: "8px 14px", borderRadius: 999,
            border: "1px solid rgba(0,179,160,0.22)",
            background: "rgba(0,179,160,0.10)",
            color: "#006355", fontWeight: 900, fontSize: 13, marginBottom: 12,
          }}>
            🎯 Use Case Scenarios
          </div>

          <h2 style={{
            fontSize: 38, margin: "0 0 12px", lineHeight: 1.1,
            letterSpacing: -0.5, fontWeight: 900, color: "#0B3C3B",
          }}>
            How professionals across North Africa use Euklydia Academy
          </h2>

          <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7, fontSize: 16 }}>
            Projected scenarios based on real business KPIs — see how each role applies use cases to unlock measurable impact.
          </p>
        </div>

        {/* Scenarios grid — 4 cards in 2×2 */}
        <div
          className="testimonialsGrid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 20,
            marginBottom: 40,
          }}
        >
          {scenarios.map((t) => (
            <div
              key={t.name}
              style={{
                background: "#fff",
                border: "1px solid rgba(15,23,42,0.08)",
                borderRadius: 22,
                padding: 28,
                display: "flex",
                flexDirection: "column",
                gap: 18,
                boxShadow: "0 4px 24px rgba(2,6,23,0.06)",
                position: "relative",
                overflow: "hidden",
              }}
            >
              {/* Guillemet décoratif */}
              <div style={{
                position: "absolute", top: 20, right: 24,
                fontSize: 64, lineHeight: 1,
                color: "rgba(0,179,160,0.10)",
                fontFamily: "Georgia, serif",
                fontWeight: 900,
                userSelect: "none",
              }}>
                "
              </div>

              {/* Top row: Role tag + Use case */}
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, alignItems: "center" }}>
                <div style={{
                  display: "inline-flex", padding: "5px 12px", borderRadius: 999,
                  background: t.roleColor.bg,
                  color: t.roleColor.color,
                  fontWeight: 800, fontSize: 11,
                }}>
                  {t.roleTag}
                </div>
                <div style={{
                  display: "inline-flex", alignItems: "center", gap: 6,
                  padding: "5px 10px", borderRadius: 999,
                  background: "#F8FAFC",
                  border: "1px solid #E5E7EB",
                  color: "#64748b",
                  fontWeight: 700, fontSize: 11,
                }}>
                  <span style={{ color: "#00B3A0" }}>📦</span>
                  Use case: {t.useCase}
                </div>
              </div>

              {/* Citation */}
              <p style={{
                fontSize: 14, color: "#334155", lineHeight: 1.75,
                margin: 0, position: "relative", zIndex: 1,
                fontStyle: "italic",
              }}>
                "{t.quote}"
              </p>

              {/* KPI Highlight */}
              <div style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                padding: "8px 14px", borderRadius: 99,
                background: "rgba(0,179,160,0.10)",
                border: "1px solid rgba(0,179,160,0.20)",
                width: "fit-content",
              }}>
                <span style={{ color: "#00B3A0", fontSize: 13 }}>📊</span>
                <span style={{ fontSize: 12, fontWeight: 900, color: "#006355" }}>
                  {t.highlight}
                </span>
              </div>

              {/* Profil avec vraie photo */}
              <div style={{
                display: "flex", alignItems: "center", gap: 12,
                borderTop: "1px solid #F1F5F9", paddingTop: 16, marginTop: "auto",
              }}>
                <img
                  src={t.avatar}
                  alt={t.name}
                  style={{
                    width: 52, height: 52,
                    borderRadius: "50%",
                    objectFit: "cover",
                    objectPosition: "center top",
                    border: `2.5px solid ${t.borderColor}`,
                    flexShrink: 0,
                  }}
                />
                <div>
                  <div style={{ fontWeight: 900, fontSize: 14, color: "#0f172a" }}>
                    {t.name}
                  </div>
                  <div style={{ fontSize: 12, color: "#64748b", fontWeight: 600 }}>
                    {t.role}
                  </div>
                  <div style={{ fontSize: 11, color: "#94a3b8", fontWeight: 600 }}>
                    {t.company}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Disclaimer note */}
        <div style={{
          textAlign: "center",
          fontSize: 12,
          color: "#94a3b8",
          fontStyle: "italic",
          marginBottom: 24,
        }}>
          Scenarios based on use case KPIs from the Euklydia Academy methodology · Pilot phase
        </div>

        {/* CTA final */}
        <div style={{
          background: "#006355",
          borderRadius: 22,
          padding: "32px 36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 20,
          flexWrap: "wrap",
        }}>
          <div>
            <div style={{ fontWeight: 900, color: "#fff", fontSize: 20, marginBottom: 6 }}>
              Ready to build your AI roadmap?
            </div>
            <div style={{ color: "rgba(255,255,255,0.75)", fontSize: 14 }}>
              Start with a free 10-minute diagnostic. Get your personalized learning pathway instantly.
            </div>
          </div>
          <a
            href="/onboarding"
            style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "14px 26px", borderRadius: 12,
              background: "#fff", color: "#006355",
              fontWeight: 900, fontSize: 14,
              textDecoration: "none", whiteSpace: "nowrap",
              transition: "transform 0.2s ease",
            }}
            onMouseEnter={e => e.currentTarget.style.transform = "translateY(-2px)"}
            onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
          >
            Start free diagnostic →
          </a>
        </div>

        <style>{`
          @media (max-width: 1024px) {
            .testimonialsGrid { grid-template-columns: repeat(2, 1fr) !important; }
          }
          @media (max-width: 640px) {
            .testimonialsGrid { grid-template-columns: 1fr !important; }
          }
        `}</style>

      </Container>
    </section>
  );
}