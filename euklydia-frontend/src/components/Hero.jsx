import { useNavigate } from "react-router-dom";
import leadersImg from "../assets/leaders.jpg";

export default function Hero() {
  const navigate = useNavigate();

  return (
    <section style={{ background: "#fff", overflow: "hidden" }}>

      {/* ── HERO SPLIT ── */}
      <div
        className="heroGrid"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          minHeight: 580,
          maxWidth: 1280,
          margin: "0 auto",
        }}
      >
        {/* LEFT */}
        <div style={{
          padding: "72px 56px 72px 64px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}>
          {/* Badge */}
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 8,
            padding: "6px 14px", borderRadius: 999,
            border: "1px solid #E5E7EB",
            background: "rgba(0,179,160,0.08)",
            color: "#006355", fontWeight: 800, fontSize: 11,
            marginBottom: 26, width: "fit-content",
          }}>
            ⚡ AI-powered learning for leaders
          </div>

          {/* Titre */}
          <h1 style={{
            fontSize: 50, fontWeight: 900, color: "#0B3C3B",
            lineHeight: 1.08, letterSpacing: -1, marginBottom: 20,
          }}>
            Build <span style={{ color: "#00B3A0" }}>AI maturity</span><br />
            for better decisions.
          </h1>

          {/* Sous-titre */}
          <p style={{
            color: "#64748b", fontSize: 15, lineHeight: 1.8,
            marginBottom: 34, maxWidth: 400,
          }}>
            Assess your AI capabilities by role, follow personalized learning paths,
            and apply practical frameworks for real business impact.
          </p>

          {/* CTAs */}
          <div style={{
            display: "flex", alignItems: "center",
            gap: 10, marginBottom: 20, flexWrap: "wrap",
          }}>
            <button
              onClick={() => navigate("/onboarding")}
              style={{
                padding: "13px 24px", borderRadius: 12,
                background: "#006355", color: "#fff",
                fontWeight: 800, fontSize: 14, border: "none",
                cursor: "pointer",
                boxShadow: "0 6px 20px rgba(0,99,85,0.22)",
                transition: "all 0.2s ease",
              }}
              onMouseEnter={e => { e.currentTarget.style.background = "#004d42"; e.currentTarget.style.transform = "translateY(-2px)"; }}
              onMouseLeave={e => { e.currentTarget.style.background = "#006355"; e.currentTarget.style.transform = "translateY(0)"; }}
            >
              Start free assessment →
            </button>
            <a
              href="#paths"
              style={{
                padding: "13px 20px", borderRadius: 12,
                background: "transparent", color: "#006355",
                fontWeight: 700, fontSize: 14,
                border: "1.5px solid rgba(0,99,85,0.25)",
                textDecoration: "none", transition: "all 0.2s ease",
              }}
              onMouseEnter={e => { e.currentTarget.style.background = "rgba(0,99,85,0.06)"; }}
              onMouseLeave={e => { e.currentTarget.style.background = "transparent"; }}
            >
              Explore learning paths
            </a>
          </div>

          {/* Réassurance */}
          <div style={{
            color: "#94a3b8", fontSize: 11, fontWeight: 600,
            display: "flex", alignItems: "center", gap: 5,
          }}>
            <span style={{ color: "#00B3A0" }}>✓</span>
            10 minutes · No credit card required · Instant roadmap
          </div>
        </div>

        {/* RIGHT — photo pleine hauteur, cadrée sur les personnes */}
        <div style={{
          position: "relative",
          background: "linear-gradient(135deg, #f0faf8 0%, #e2f5f2 100%)",
          overflow: "hidden",
          minHeight: 480,
        }}>
          <img
            src={leadersImg}
            alt="Business leaders collaborating"
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
              objectFit: "cover",
              objectPosition: "center 65%",  /* cadre sur les visages/personnes */
            }}
          />

          {/* Badge haut gauche */}
          <div style={{
            position: "absolute", top: 24, left: 24, zIndex: 3,
            background: "#fff",
            borderRadius: 14, padding: "10px 16px",
            boxShadow: "0 8px 28px rgba(0,0,0,0.10)",
            display: "flex", alignItems: "center", gap: 10,
          }}>
            <div style={{
              width: 8, height: 8, borderRadius: "50%",
              background: "#00B3A0",
              boxShadow: "0 0 0 3px rgba(0,179,160,0.18)",
            }} />
            <span style={{ fontSize: 11, fontWeight: 800, color: "#0B3C3B" }}>
              AI Assessment · Role-based
            </span>
          </div>

          {/* Badge bas droite */}
          <div style={{
            position: "absolute", bottom: 28, right: 24, zIndex: 3,
            background: "#006355",
            borderRadius: 16, padding: "14px 20px",
            boxShadow: "0 8px 28px rgba(0,99,85,0.28)",
            textAlign: "center",
          }}>
            <div style={{ fontSize: 24, fontWeight: 900, color: "#fff", lineHeight: 1 }}>
              10 min
            </div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.72)", fontWeight: 600, marginTop: 4 }}>
              To your roadmap
            </div>
          </div>
        </div>
      </div>

      {/* ── KPI BAND ── */}
      <div
        className="kpiGrid"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          borderTop: "1px solid #E5E7EB",
          maxWidth: 1280,
          margin: "0 auto",
        }}
      >
        {[
          { value: "4",    label: "Professional Roles",   sub: "Sales · Marketing · Design · PM" },
          { value: "5",    label: "Skills per Role",      sub: "Role-specific AI competencies" },
          { value: "10",   label: "Assessment Questions", sub: "5 skills × 2 questions each" },
          { value: "100%", label: "Role-based learning",  sub: "Tailored to your actual job" },
        ].map((kpi, i) => (
          <div
            key={kpi.label}
            style={{
              padding: "26px 20px",
              textAlign: "center",
              borderRight: i < 3 ? "1px solid #E5E7EB" : "none",
              background: "#fff",
            }}
          >
            <div style={{ fontSize: 30, fontWeight: 900, color: "#006355", marginBottom: 5 }}>
              {kpi.value}
            </div>
            <div style={{ fontSize: 12, fontWeight: 800, color: "#0B3C3B", marginBottom: 3 }}>
              {kpi.label}
            </div>
            <div style={{ fontSize: 10, color: "#94a3b8", fontWeight: 600 }}>
              {kpi.sub}
            </div>
          </div>
        ))}
      </div>

      <style>{`
        @media (max-width: 900px) {
          .heroGrid { grid-template-columns: 1fr !important; }
          .heroGrid > div:last-child { min-height: 360px !important; }
          .kpiGrid { grid-template-columns: repeat(2, 1fr) !important; }
        }
        @media (max-width: 480px) {
          .heroGrid > div:first-child { padding: 48px 24px !important; }
          h1 { font-size: 34px !important; }
          .kpiGrid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </section>
  );
}