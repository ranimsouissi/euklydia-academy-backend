import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "../components/ui/Container";

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
              <div
                style={{
                  fontSize: 16,
                  fontWeight: 800,
                  color: "var(--primary)",
                  marginBottom: 12,
                }}
              >
                Euklydia Academy
              </div>

              <div
                style={{
                  fontSize: 38,
                  fontWeight: 900,
                  color: "var(--text)",
                  lineHeight: 1.05,
                }}
              >
                Forgot password
              </div>

              <div
                style={{
                  color: "var(--muted)",
                  marginTop: 10,
                  fontSize: 15,
                  lineHeight: 1.6,
                }}
              >
                Enter your work email and we’ll send you a reset link.
              </div>
            </div>

            <label style={labelStyle}>Work email</label>
            <input
              style={inputStyle}
              type="email"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            {message && (
              <div
                style={{
                  marginTop: 14,
                  padding: "12px 14px",
                  borderRadius: 16,
                  background: "rgba(255,255,255,0.75)",
                  border: "1px solid var(--border)",
                  color: "var(--text)",
                  fontSize: 14,
                  lineHeight: 1.5,
                }}
              >
                {message}
              </div>
            )}

            <div style={{ marginTop: 24 }}>
              <button onClick={submit} style={primaryBtnStyle} disabled={loading}>
                {loading ? "Sending..." : "Send reset link"}
              </button>
            </div>

            <div
              style={{
                marginTop: 24,
                textAlign: "center",
                color: "var(--muted)",
                fontSize: 14,
              }}
            >
              Remember your password?{" "}
              <button type="button" style={linkBtnStyle} onClick={() => navigate("/auth")}>
                Back to login
              </button>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
}

const labelStyle = {
  display: "block",
  fontWeight: 800,
  marginBottom: 8,
  marginTop: 14,
  color: "var(--text)",
  fontSize: 15,
};

const inputStyle = {
  width: "100%",
  padding: "16px 18px",
  borderRadius: "20px",
  border: "1px solid var(--border)",
  outline: "none",
  fontSize: 16,
  background: "rgba(255,255,255,0.75)",
  boxSizing: "border-box",
};

const primaryBtnStyle = {
  width: "100%",
  padding: "16px 18px",
  borderRadius: "20px",
  border: "none",
  background: "var(--primary)",
  color: "#fff",
  fontWeight: 900,
  fontSize: 16,
  cursor: "pointer",
};

const linkBtnStyle = {
  background: "none",
  border: "none",
  color: "var(--primary)",
  fontWeight: 900,
  cursor: "pointer",
  padding: 0,
};