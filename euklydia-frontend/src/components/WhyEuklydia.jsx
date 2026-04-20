import Section from "./ui/Section";
import SectionHeader from "./ui/SectionHeader";

const problems = [
  {
    emoji: "📉",
    iconBg: "#FEE2E2",
    tagBg: "#FEE2E2",
    tagColor: "#991B1B",
    tag: "Visibility",
    title: "No clear AI maturity baseline",
    desc: "Leaders launch AI initiatives without knowing where their teams actually stand — no skill map, no gaps identified, no readiness across functions.",
  },
  {
    emoji: "🧩",
    iconBg: "#FEF3C7",
    tagBg: "#FEF3C7",
    tagColor: "#92400E",
    tag: "Strategy",
    title: "Too many tools, no operating model",
    desc: "AI tools multiply but nobody owns the workflows. Governance is missing, accountability is unclear, and adoption stalls before creating value.",
  },
  {
    emoji: "🎓",
    iconBg: "#DBEAFE",
    tagBg: "#DBEAFE",
    tagColor: "#1E40AF",
    tag: "Learning",
    title: "Training is generic, not role-based",
    desc: "One-size-fits-all courses teach concepts but skip execution. No deliverables, no frameworks, no connection to the actual job to be done.",
  },
  {
    emoji: "⚖️",
    iconBg: "rgba(127,119,221,0.12)",
    tagBg: "rgba(127,119,221,0.12)",
    tagColor: "#534AB7",
    tag: "Governance",
    title: "AI ethics & governance ignored",
    desc: "Teams adopt AI fast but ignore compliance, ethics and risk. Governance frameworks are unknown — until something goes wrong.",
  },
];

const benchmarkGaps = [
  {
    icon: "💰",
    problem: "Expensive & inaccessible",
    desc: "Most platforms charge premium prices — built for large Western enterprises, not for growing businesses.",
    solution: "Accessible & progressive pricing",
  },
  {
    icon: "📈",
    problem: "Built for experts, not leaders in transition",
    desc: "Existing courses assume advanced technical knowledge. Business leaders are left behind before they even start.",
    solution: "Designed for business leaders at every level",
  },
  {
    icon: "🔧",
    problem: "Tools & frameworks from Europe & the US",
    desc: "Trainings are built around tools and market realities that don't reflect the local business context.",
    solution: "Adapted to your real business environment",
  },
  {
    icon: "🌍",
    problem: "Content in English only",
    desc: "Most platforms offer content in English or academic French — disconnected from local professional realities.",
    solution: "Built for your professional context",
  },
];

export default function WhyEuklydia() {
  return (
    <Section id="platform" bg="#F2FBF9">
      <SectionHeader
        kicker="Why Euklydia Academy ?"
        subtitle="Euklydia Academy helps leaders assess AI maturity, prioritize the right skills, and turn learning into measurable business execution."
      />

      {/* ── 4 Problem cards ── */}
      <div
        className="whyGrid"
        style={{
          marginTop: 28,
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 16,
        }}
      >
        {problems.map((it) => (
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

      {/* ── Benchmarking section ── */}
      <div style={{ marginTop: 40 }}>
        {/* Header benchmarking */}
        <div style={{ marginBottom: 20 }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "6px 14px", borderRadius: 999,
            border: "1px solid #E5E7EB",
            background: "rgba(0,179,160,0.08)",
            color: "#006355", fontWeight: 800, fontSize: 12,
            marginBottom: 12,
          }}>
            📊 Benchmarking insight
          </div>
          <h3 style={{
            fontSize: 22, fontWeight: 900, color: "#0f172a",
            marginBottom: 8, lineHeight: 1.3,
          }}>
            Why existing platforms don't work for you 
          </h3>
          <p style={{ color: "#64748b", fontSize: 14, lineHeight: 1.7, maxWidth: 580 }}>
            Our benchmarking of available AI training platforms reveals a systematic gap — none of them are built for the realities of business leaders in our market.
          </p>
        </div>

        {/* Gap comparison grid */}
        <div
          className="benchGrid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: 12,
          }}
        >
          {benchmarkGaps.map((gap) => (
            <div
              key={gap.problem}
              style={{
                background: "#fff",
                border: "1px solid #E5E7EB",
                borderRadius: 18, padding: "20px 22px",
                display: "flex", gap: 16, alignItems: "flex-start",
              }}
            >
              <div style={{
                fontSize: 24, flexShrink: 0,
                width: 44, height: 44, borderRadius: 12,
                background: "#F8FAFC",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                {gap.icon}
              </div>
              <div>
                <div style={{
                  fontSize: 13, fontWeight: 900, color: "#991B1B",
                  marginBottom: 4,
                  display: "flex", alignItems: "center", gap: 6,
                }}>
                  <span style={{
                    display: "inline-block", width: 6, height: 6,
                    borderRadius: "50%", background: "#991B1B", flexShrink: 0,
                  }} />
                  {gap.problem}
                </div>
                <div style={{ fontSize: 12, color: "#64748b", lineHeight: 1.65, marginBottom: 8 }}>
                  {gap.desc}
                </div>
                <div style={{
                  fontSize: 12, fontWeight: 800, color: "#006355",
                  display: "flex", alignItems: "center", gap: 6,
                }}>
                  <span style={{
                    display: "inline-block", width: 6, height: 6,
                    borderRadius: "50%", background: "#006355", flexShrink: 0,
                  }} />
                  Euklydia: {gap.solution}
                </div>
              </div>
            </div>
          ))}
        </div>
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
              Euklydia is the first AI learning platform built for your business reality.
            </div>
            <div style={{ color: "rgba(255,255,255,0.70)", fontSize: 13, marginTop: 3 }}>
              Assess → Prioritize → Execute. Role-based, practical, and accessible.
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
          .benchGrid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </Section>
  );
}