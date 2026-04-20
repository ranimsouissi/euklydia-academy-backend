import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "../components/ui/Container";

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

      const stRes = await fetch(`${API}/api/v1/assessment/status`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      if (!stRes.ok) {
        navigate("/dashboard", { replace: true });
        return;
      }

      const st = await stRes.json();
      localStorage.setItem("assessment_status", JSON.stringify(st));

      if (st.required) {
        navigate("/assessment", { replace: true });
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
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(180deg, var(--bg-subtle) 0%, var(--bg-soft) 100%)",
        display: "flex",
        alignItems: "center",
        padding: "40px 0",
      }}
    >
      <Container>
        <div style={{ maxWidth: 560, margin: "0 auto" }}>
          <div style={{ padding: "24px 20px" }}>
            <div style={{ marginBottom: 28 }}>
              <div style={{ fontSize: 16, fontWeight: 800, color: "var(--primary)", marginBottom: 12 }}>
                Euklydia Academy
              </div>
              <div style={{ fontSize: 38, fontWeight: 900, color: "var(--text)", lineHeight: 1.05 }}>
                {mode === "login" ? "Welcome back" : "Create your account"}
              </div>
              <div style={{ color: "var(--muted)", marginTop: 10, fontSize: 15, lineHeight: 1.6 }}>
                {mode === "login"
                  ? "Sign in to continue your AI learning journey."
                  : "Join Euklydia Academy and start building your AI maturity."}
              </div>
            </div>

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

            <label style={labelStyle}>Work email</label>
            <input
              style={inputStyle}
              type="email"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <label style={labelStyle}>Password</label>
              {mode === "login" && (
                <button type="button" style={linkBtnStyle} onClick={() => navigate("/forgot-password")}>
                  Forgot password?
                </button>
              )}
            </div>

            <PasswordField
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={mode === "login" ? "Enter your password" : "Create your password"}
              visible={showPassword}
              onToggle={() => setShowPassword((v) => !v)}
            />
            <div style={{ fontSize: 12, color: "var(--muted)", marginTop: 6 }}>
              Password must contain at least 8 characters.
            </div>

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

            <div style={{ marginTop: 24 }}>
              <button onClick={submit} style={primaryBtnStyle}>
                {mode === "login" ? "Log in" : "Create account"}
              </button>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 12, margin: "28px 0 20px" }}>
              <div style={{ flex: 1, height: 1, background: "var(--border)" }} />
              <div style={{ color: "var(--muted)", fontSize: 12, fontWeight: 800 }}>OR</div>
              <div style={{ flex: 1, height: 1, background: "var(--border)" }} />
            </div>

            <OauthBtn onClick={googleLogin}>
              <GoogleIcon />
              <span>{mode === "login" ? "Continue with Google" : "Sign up with Google"}</span>
            </OauthBtn>

            <div style={{ marginTop: 24, textAlign: "center", color: "var(--muted)", fontSize: 14 }}>
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
      </Container>
    </div>
  );
}

function PasswordField({ value, onChange, placeholder, visible, onToggle }) {
  return (
    <div style={{ position: "relative" }}>
      <input
        style={{ ...inputStyle, paddingRight: 56, marginBottom: 0 }}
        type={visible ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <button type="button" onClick={onToggle} style={eyeBtnStyle} aria-label={visible ? "Hide password" : "Show password"}>
        {visible ? <EyeOffIcon /> : <EyeIcon />}
      </button>
    </div>
  );
}

function OauthBtn({ children, onClick }) {
  return (
    <button type="button" onClick={onClick} style={{
      width: "100%", padding: "15px 18px", borderRadius: "var(--radius-md)",
      border: "1px solid var(--border)", background: "#F3F4F6", fontWeight: 800,
      cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
      gap: 12, color: "var(--text)",
    }}>
      {children}
    </button>
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

const labelStyle = { display: "block", fontWeight: 800, marginBottom: 8, marginTop: 14, color: "var(--text)", fontSize: 15 };
const inputStyle = { width: "100%", padding: "16px 18px", borderRadius: "20px", border: "1px solid var(--border)", outline: "none", fontSize: 16, background: "rgba(255,255,255,0.75)", boxSizing: "border-box" };
const primaryBtnStyle = { width: "100%", padding: "16px 18px", borderRadius: "20px", border: "none", background: "var(--primary)", color: "#fff", fontWeight: 900, fontSize: 16, cursor: "pointer" };
const linkBtnStyle = { background: "none", border: "none", color: "var(--primary)", fontWeight: 900, cursor: "pointer", padding: 0 };
const eyeBtnStyle = { position: "absolute", right: 16, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", color: "var(--muted)", cursor: "pointer", padding: 0, display: "flex", alignItems: "center", justifyContent: "center" };