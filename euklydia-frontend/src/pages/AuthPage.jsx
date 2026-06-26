import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API = process.env.REACT_APP_API_URL;

export default function AuthPage() {
  const navigate = useNavigate();

  const [mode, setMode] = useState("login");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const resetForm = (nextMode) => {
    setMode(nextMode);
    setFullName("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  const submit = async () => {
    try {
      if (!email || !password) throw new Error("Email et mot de passe requis");

      if (mode === "register") {
        if (!fullName.trim()) throw new Error("Le nom est requis");
        if (!confirmPassword) throw new Error("Veuillez confirmer le mot de passe");
        if (password !== confirmPassword) throw new Error("Les mots de passe ne correspondent pas");

        const r1 = await fetch(`${API}/api/v1/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: fullName.trim(),
            email,
            password,
            confirm_password: confirmPassword,
          }),
        });

        if (!r1.ok) {
          const err = await r1.json().catch(() => ({}));
          let message = "Register failed";
          if (Array.isArray(err.detail)) {
            message = err.detail.map(e => e.msg).join(", ");
          } else if (typeof err.detail === "string") {
            message = err.detail;
          }
          throw new Error(message);
        }
      }

      const r2 = await fetch(`${API}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!r2.ok) {
        const err = await r2.json().catch(() => ({}));
        throw new Error(err.detail || "Login failed");
      }

      const data = await r2.json();
      localStorage.setItem("token", data.access_token);

      const meRes = await fetch(`${API}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      if (!meRes.ok) {
        navigate("/auth", { replace: true });
        return;
      }

      const me = await meRes.json();
      localStorage.setItem("auth_user", JSON.stringify(me));

      if (!me.career_path_id) {
        navigate("/onboarding", { replace: true });
        return;
      }

      const stRes = await fetch(`${API}/api/v1/diagnostic/status`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      if (!stRes.ok) {
        navigate("/dashboard", { replace: true });
        return;
      }

      const st = await stRes.json();
      localStorage.setItem("diagnostic_status", JSON.stringify(st));

      if (st.required) {
        navigate("/diagnostic", { replace: true });
        return;
      }

      navigate("/dashboard", { replace: true });
    } catch (e) {
      alert(e.message);
    }
  };

  const googleLogin = () => {
    window.location.href = `${API}/api/v1/auth/google/start`;
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
        justifyContent: "center",
        gap: 48,
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

        {/* ─── CENTRE : Tagline impactant ──────────────────────────── */}
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

        {/* ─── BOTTOM : Section "What you'll get" + 4 stats ───────── */}
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

        {/* Back to home — top right */}
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

          {/* ─── Header du form ──────────────────────────────────── */}
          <div style={{ marginBottom: 16 }}>
            <h1 style={{
              fontSize: 26,
              fontWeight: 900,
              color: "#0B3C3B",
              margin: "0 0 6px",
              lineHeight: 1.2,
              letterSpacing: "-0.5px",
            }}>
              {mode === "login" ? (
                <>Welcome back to <span style={{ color: "#006355" }}>Euklydia Academy</span></>
              ) : (
                <>Create your <span style={{ color: "#006355" }}>account</span></>
              )}
            </h1>
            <p style={{ color: "#64748b", fontSize: 13, lineHeight: 1.5, margin: 0 }}>
              {mode === "login"
                ? "Sign in to continue your AI learning journey."
                : "Join Euklydia Academy and start mastering AI use cases."}
            </p>
          </div>

          {/* ─── Google OAuth EN PREMIER ─────────────────────────── */}
          <button type="button" onClick={googleLogin} style={googleBtnStyle}>
            <GoogleIcon />
            <span>{mode === "login" ? "Continue with Google" : "Sign up with Google"}</span>
          </button>

          {/* ─── Séparateur ──────────────────────────────────────── */}
          <div style={{ display: "flex", alignItems: "center", gap: 12, margin: "14px 0" }}>
            <div style={{ flex: 1, height: 1, background: "#E5E7EB" }} />
            <div style={{ color: "#94a3b8", fontSize: 11, fontWeight: 700 }}>
              Or continue with email
            </div>
            <div style={{ flex: 1, height: 1, background: "#E5E7EB" }} />
          </div>

          {/* ─── Full name (register only) ───────────────────────── */}
          {mode === "register" && (
            <>
              <label style={labelStyle}>Full name</label>
              <input
                style={inputStyle}
                type="text"
                placeholder="Enter your full name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </>
          )}

          {/* ─── Email ───────────────────────────────────────────── */}
          <label style={labelStyle}>Work email</label>
          <input
            style={inputStyle}
            type="email"
            placeholder="name@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          {/* ─── Password ────────────────────────────────────────── */}
          <label style={labelStyle}>Password</label>
          <PasswordField
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={mode === "login" ? "Enter your password" : "Min 8 characters"}
            visible={showPassword}
            onToggle={() => setShowPassword((v) => !v)}
          />

          {/* Forgot password (login only) — alignée droite */}
          {mode === "login" && (
            <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 6 }}>
              <button type="button" style={linkBtnStyle} onClick={() => navigate("/forgot-password")}>
                Forgot password?
              </button>
            </div>
          )}

          {/* ─── Confirm password (register only) ────────────────── */}
          {mode === "register" && (
            <>
              <label style={labelStyle}>Confirm password</label>
              <PasswordField
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                visible={showConfirmPassword}
                onToggle={() => setShowConfirmPassword((v) => !v)}
              />
            </>
          )}

          {/* ─── Submit button ───────────────────────────────────── */}
          <div style={{ marginTop: 18 }}>
            <button onClick={submit} style={primaryBtnStyle}>
              {mode === "login" ? "Log in" : "Create account"}
            </button>
          </div>

          {/* ─── Toggle Login / Sign up ──────────────────────────── */}
          <div style={{ marginTop: 16, textAlign: "center", color: "#64748b", fontSize: 13 }}>
            {mode === "login" ? (
              <>
                Don't have an account?{" "}
                <button type="button" style={linkBtnStyle} onClick={() => resetForm("register")}>Sign up</button>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <button type="button" style={linkBtnStyle} onClick={() => resetForm("login")}>Log in</button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* ─── Responsive ──────────────────────────────────────────── */}
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

function PasswordField({ value, onChange, placeholder, visible, onToggle }) {
  return (
    <div style={{ position: "relative" }}>
      <input
        style={{ ...inputStyle, paddingRight: 50, marginBottom: 0 }}
        type={visible ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <button
        type="button"
        onClick={onToggle}
        style={eyeBtnStyle}
        aria-label={visible ? "Hide password" : "Show password"}
      >
        {visible ? <EyeOffIcon /> : <EyeIcon />}
      </button>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303C33.654 32.657 29.243 36 24 36c-6.627 0-12-5.373-12-12S17.373 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.27 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z" />
      <path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.27 4 24 4c-7.682 0-14.347 4.337-17.694 10.691z" />
      <path fill="#4CAF50" d="M24 44c5.145 0 9.824-1.977 13.373-5.197l-6.186-5.238C29.111 35.091 26.715 36 24 36c-5.222 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z" />
      <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303c-.792 2.237-2.231 4.166-4.116 5.565l.003-.002 6.186 5.238C36.938 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z" />
    </svg>
  );
}

function EyeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M2 12C3.8 8.5 7.3 6 12 6C16.7 6 20.2 8.5 22 12C20.2 15.5 16.7 18 12 18C7.3 18 3.8 15.5 2 12Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.8" />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M3 3L21 21" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      <path d="M10.6 10.7C10.2 11.1 10 11.5 10 12C10 13.1 10.9 14 12 14C12.5 14 12.9 13.8 13.3 13.4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M6.7 6.8C4.7 8 3.1 9.8 2 12C3.8 15.5 7.3 18 12 18C14 18 15.8 17.5 17.4 16.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M9.9 5.2C10.6 5.1 11.3 5 12 5C16.7 5 20.2 7.5 22 11C21.4 12.2 20.6 13.3 19.7 14.2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
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

const googleBtnStyle = {
  width: "100%",
  padding: "11px 18px",
  borderRadius: 10,
  border: "1px solid #E5E7EB",
  background: "#fff",
  fontWeight: 800,
  fontSize: 13,
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: 12,
  color: "#0B3C3B",
  transition: "background 0.2s, border-color 0.2s",
};

const linkBtnStyle = {
  background: "none",
  border: "none",
  color: "#006355",
  fontWeight: 800,
  cursor: "pointer",
  padding: 0,
  fontSize: 12,
};

const eyeBtnStyle = {
  position: "absolute",
  right: 12,
  top: "50%",
  transform: "translateY(-50%)",
  background: "none",
  border: "none",
  color: "#94a3b8",
  cursor: "pointer",
  padding: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};