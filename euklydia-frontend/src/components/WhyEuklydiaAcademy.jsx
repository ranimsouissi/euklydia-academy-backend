import Section from "./ui/Section";
import SectionHeader from "./ui/SectionHeader";

const pillars = [
  {
    emoji: "🔍",
    iconBg: "#DBEAFE",
    tagBg: "#DBEAFE",
    tagColor: "#1E40AF",
    tag: "Diagnostic",
    title: "Know exactly where you stand",
    desc: "Most leaders launch AI initiatives without knowing their real gaps. Our 9-question diagnostic maps your maturity across 3 business use cases per role — no guesswork, no generic scoring.",
  },
  {
    emoji: "💼",
    iconBg: "rgba(127,119,221,0.12)",
    tagBg: "rgba(127,119,221,0.12)",
    tagColor: "#534AB7",
    tag: "Use Cases",
    title: "Learn through real business scenarios",
    desc: "Generic courses teach AI concepts. We start from the actual problems you face: lead qualification, campaign optimization, project planning, design ideation — and the workflows that solve them.",
  },
  {
    emoji: "📈",
    iconBg: "#FEF3C7",
    tagBg: "#FEF3C7",
    tagColor: "#92400E",
    tag: "Execution",
    title: "From learning to measurable impact",
    desc: "Every use case ships with Initial KPI → Projected KPI. Templates, prompts, and AI agent blueprints you apply on Day 1 — not theoretical frameworks that stay on the shelf.",
  },
  {
    emoji: "🌍",
    iconBg: "#FEE2E2",
    tagBg: "#FEE2E2",
    tagColor: "#991B1B",
    tag: "Context",
    title: "Built for North African business reality",
    desc: "Tools, examples, and KPIs adapted to North African business environment — not Silicon Valley playbooks translated into French. Real scenarios for real markets.",
  },
];

export default function WhyEuklydiaAcademy() {
  return (
    <Section id="platform" bg="#F2FBF9">
      <SectionHeader
        kicker="Why Euklydia Academy ?"
        subtitle="Most platforms teach AI concepts. We diagnose your gaps, activate the right skills on real business use cases, and turn learning into measurable KPI impact."
      />

      {/* ── 4 Pillar cards ── */}
      <div
        className="whyGrid"
        style={{
          marginTop: 28,
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 16,
        }}
      >
        {pillars.map((it) => (
          <div
            key={it.title}
            style={{
              background: "#fff",
              border: "1px solid rgba(15,23,42,0.08)",
              borderRadius: 22, padding: 26,
              boxShadow: "0 18px 55px rgba(2,6,23,0.06)",
              display: "flex", flexDirection: "column", gap: 14,
              position: "relative", overflow: "hidden",
            }}
          >
            <div style={{
              position: "absolute", top: -24, right: -24,
              width: 80, height: 80, borderRadius: "50%",
              background: it.iconBg, opacity: 0.5,
            }} />

            <div style={{ display: "flex", alignItems: "flex-start", gap: 14, position: "relative" }}>
              <div style={{
                width: 48, height: 48, borderRadius: 14,
                background: it.iconBg,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 22, flexShrink: 0,
              }}>
                {it.emoji}
              </div>
              <div style={{
                display: "inline-flex", padding: "4px 10px",
                borderRadius: 999, marginTop: 4,
                background: it.tagBg, color: it.tagColor,
                fontWeight: 800, fontSize: 11,
              }}>
                {it.tag}
              </div>
            </div>

            <div style={{ position: "relative" }}>
              <div style={{ fontWeight: 900, color: "#0B3C3B", marginBottom: 8, fontSize: 15, lineHeight: 1.4 }}>
                {it.title}
              </div>
              <div style={{ color: "#64748b", lineHeight: 1.75, fontSize: 14 }}>
                {it.desc}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Banner teal ── */}
      <div style={{
        marginTop: 28,
        background: "#006355",
        borderRadius: 18,
        padding: "22px 28px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: 16,
        flexWrap: "wrap",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div style={{
            width: 38, height: 38, borderRadius: 10,
            background: "rgba(255,255,255,0.15)",
            display: "flex", alignItems: "center", justifyContent: "center",
            flexShrink: 0, fontSize: 18,
          }}>
            ✦
          </div>
          <div>
            <div style={{ fontWeight: 800, color: "#fff", fontSize: 15 }}>
              The first use case-driven AI learning platform built for North African leaders.
            </div>
            <div style={{ color: "rgba(255,255,255,0.70)", fontSize: 13, marginTop: 3 }}>
              Diagnose → Learn → Execute → Measure. Role-based, practical, and accessible.
            </div>
          </div>
        </div>
        <a
          href="#how"
          style={{
            display: "inline-flex", alignItems: "center", gap: 6,
            padding: "10px 18px", borderRadius: 10,
            background: "rgba(255,255,255,0.15)",
            border: "1px solid rgba(255,255,255,0.25)",
            color: "#fff", fontWeight: 800, fontSize: 13,
            textDecoration: "none", whiteSpace: "nowrap",
            transition: "background 0.2s",
          }}
          onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.25)"}
          onMouseLeave={e => e.currentTarget.style.background = "rgba(255,255,255,0.15)"}
        >
          See how it works →
        </a>
      </div>

      <style>{`
        @media (max-width: 768px) {
          .whyGrid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </Section>
  );
}