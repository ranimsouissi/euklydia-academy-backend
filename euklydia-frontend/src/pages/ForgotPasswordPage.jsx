import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API = process.env.REACT_APP_API_URL;

export default function ForgotPasswordPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const submit = async () => {
    try {
      if (!email.trim()) {
        throw new Error("Email is required");
      }

      setLoading(true);
      setMessage("");

      const res = await fetch(`${API}/api/v1/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setMessage(data.message || "If the email exists, a reset link has been sent");
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="authPage" style={{
      minHeight: "100vh",
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      background: "#fff",
    }}>

      {/* ═══ PANNEAU GAUCHE : TEAL BRAND ════════════════════════════ */}
      <div className="authLeftPanel" style={{
        background: "linear-gradient(135deg, #0B3C3B 0%, #064C45 50%, #0B3C3B 100%)",
        color: "#fff",
        padding: "32px 48px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        position: "relative",
        overflow: "hidden",
        minHeight: "100vh",
      }}>

        {/* Pattern de points subtil */}
        <div style={{
          position: "absolute",
          inset: 0,
          backgroundImage: "radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px)",
          backgroundSize: "28px 28px",
          opacity: 0.5,
          pointerEvents: "none",
        }} />

        {/* Vague organique décorative en bas-droite */}
        <svg
          width="500"
          height="500"
          viewBox="0 0 500 500"
          style={{
            position: "absolute",
            bottom: -150,
            right: -150,
            opacity: 0.15,
            pointerEvents: "none",
          }}
        >
          <path
            fill="#00B3A0"
            d="M421.5,323Q387,396,304,420.5Q221,445,148.5,402Q76,359,72,279.5Q68,200,128,151.5Q188,103,266,89Q344,75,397.5,137.5Q451,200,448,275Q445,350,421.5,323Z"
          />
          <path
            fill="#00B3A0"
            opacity="0.6"
            d="M395,310Q360,370,295,400Q230,430,170,395Q110,360,90,290Q70,220,125,165Q180,110,255,95Q330,80,375,140Q420,200,415,260Q410,320,395,310Z"
          />
        </svg>

        {/* TOP : Logo */}
        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{ fontSize: 24, fontWeight: 900, marginBottom: 4, letterSpacing: "-0.5px" }}>
            Euklydia <span style={{ color: "#00B3A0" }}>Academy</span>
          </div>
          <div style={{ fontSize: 12, opacity: 0.7, fontWeight: 600 }}>
            AI Learning Pathway
          </div>
        </div>

        {/* CENTRE : Tagline */}
        <div style={{ position: "relative", zIndex: 1, maxWidth: 460 }}>
          <div style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            padding: "5px 12px",
            background: "rgba(0,179,160,0.18)",
            border: "1px solid rgba(0,179,160,0.35)",
            borderRadius: 99,
            fontSize: 11,
            fontWeight: 700,
            marginBottom: 18,
          }}>
            <span style={{ color: "#00B3A0" }}>●</span>
            Use case-driven AI learning
          </div>

          <h2 style={{
            fontSize: 38,
            fontWeight: 900,
            lineHeight: 1.1,
            margin: "0 0 16px",
            letterSpacing: "-1px",
          }}>
            Master AI through real <span style={{ color: "#00B3A0" }}>business use cases</span>.
          </h2>

          <p style={{
            fontSize: 14,
            lineHeight: 1.65,
            opacity: 0.85,
            margin: 0,
          }}>
            Diagnose your gaps, follow a personalized pathway by role, and unlock measurable KPI improvements.
          </p>
        </div>

        {/* BOTTOM : Stats */}
        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{
            fontSize: 12,
            fontWeight: 800,
            opacity: 0.85,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 12,
          }}>
            What you'll get
          </div>
          <div style={{
            paddingTop: 12,
            borderTop: "1px solid rgba(255,255,255,0.18)",
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: 12,
          }}>
            <Stat value="4" label="Professional roles" />
            <Stat value="3" label="Use cases per role" />
            <Stat value="9" label="Diagnostic questions" />
            <Stat value="10 min" label="To your roadmap" />
          </div>
        </div>
      </div>

      {/* ═══ PANNEAU DROIT : FORMULAIRE ═════════════════════════════ */}
      <div className="authRightPanel" style={{
        background: "#fff",
        padding: "32px 48px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
        minHeight: "100vh",
      }}>

        {/* Back to home */}
        <button
          type="button"
          onClick={() => navigate("/")}
          style={{
            position: "absolute",
            top: 24,
            right: 48,
            background: "none",
            border: "none",
            color: "#64748b",
            fontWeight: 700,
            fontSize: 13,
            cursor: "pointer",
            padding: 0,
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
        >
          ← Back to home
        </button>

        <div style={{ maxWidth: 420, width: "100%" }}>

          {/* Header du form */}
          <div style={{ marginBottom: 24 }}>
            <h1 style={{
              fontSize: 28,
              fontWeight: 900,
              color: "#0B3C3B",
              margin: "0 0 8px",
              lineHeight: 1.2,
              letterSpacing: "-0.5px",
            }}>
              Forgot your <span style={{ color: "#006355" }}>password?</span>
            </h1>
            <p style={{ color: "#64748b", fontSize: 14, lineHeight: 1.6, margin: 0 }}>
              Enter your work email and we'll send you a secure reset link.
            </p>
          </div>

          {/* Email */}
          <label style={labelStyle}>Work email</label>
          <input
            style={inputStyle}
            type="email"
            placeholder="name@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          {/* Message de confirmation */}
          {message && (
            <div
              style={{
                marginTop: 14,
                padding: "12px 14px",
                borderRadius: 10,
                background: "rgba(0,179,160,0.08)",
                border: "1px solid rgba(0,179,160,0.25)",
                color: "#0B3C3B",
                fontSize: 13,
                lineHeight: 1.5,
                fontWeight: 600,
              }}
            >
              ✓ {message}
            </div>
          )}

          {/* Bouton */}
          <div style={{ marginTop: 20 }}>
            <button onClick={submit} style={primaryBtnStyle} disabled={loading}>
              {loading ? "Sending..." : "Send reset link"}
            </button>
          </div>

          {/* Lien retour login */}
          <div
            style={{
              marginTop: 18,
              textAlign: "center",
              color: "#64748b",
              fontSize: 13,
            }}
          >
            Remember your password?{" "}
            <button type="button" style={linkBtnStyle} onClick={() => navigate("/auth")}>
              Back to login
            </button>
          </div>
        </div>
      </div>

      {/* Responsive */}
      <style>{`
        @media (max-width: 980px) {
          .authPage {
            grid-template-columns: 1fr !important;
          }
          .authLeftPanel {
            padding: 32px 24px !important;
            min-height: auto !important;
          }
          .authLeftPanel h2 {
            font-size: 26px !important;
          }
          .authRightPanel {
            padding: 32px 24px !important;
          }
        }
      `}</style>
    </div>
  );
}

// ═══ Composants internes ════════════════════════════════════════

function Stat({ value, label }) {
  return (
    <div>
      <div style={{
        fontSize: 22,
        fontWeight: 900,
        color: "#00B3A0",
        lineHeight: 1,
        marginBottom: 4,
      }}>
        {value}
      </div>
      <div style={{
        fontSize: 10,
        opacity: 0.75,
        fontWeight: 600,
        lineHeight: 1.3,
      }}>
        {label}
      </div>
    </div>
  );
}

// ═══ Styles ══════════════════════════════════════════════════════

const labelStyle = {
  display: "block",
  fontWeight: 800,
  marginBottom: 6,
  marginTop: 12,
  color: "#0B3C3B",
  fontSize: 12,
};

const inputStyle = {
  width: "100%",
  padding: "11px 14px",
  borderRadius: 10,
  border: "1px solid #E5E7EB",
  outline: "none",
  fontSize: 14,
  background: "#F8FAFC",
  boxSizing: "border-box",
  transition: "border-color 0.2s, background 0.2s",
};

const primaryBtnStyle = {
  width: "100%",
  padding: "12px 18px",
  borderRadius: 10,
  border: "none",
  background: "#0B3C3B",
  color: "#fff",
  fontWeight: 900,
  fontSize: 14,
  cursor: "pointer",
  transition: "background 0.2s",
};

const linkBtnStyle = {
  background: "none",
  border: "none",
  color: "#006355",
  fontWeight: 800,
  cursor: "pointer",
  padding: 0,
  fontSize: 13,
};