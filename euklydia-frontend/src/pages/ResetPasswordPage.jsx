import { useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Container from "../components/ui/Container";

const API = process.env.REACT_APP_API_URL;

export default function ResetPasswordPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const token = useMemo(() => searchParams.get("token") || "", [searchParams]);

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    try {
      if (!token) {
        throw new Error("Missing reset token");
      }

      if (!newPassword || !confirmPassword) {
        throw new Error("Please fill in both password fields");
      }

      if (newPassword.length < 8) {
        throw new Error("Password must contain at least 8 characters");
      }

      if (newPassword !== confirmPassword) {
        throw new Error("Passwords do not match");
      }

      setLoading(true);

      const res = await fetch(`${API}/api/v1/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token,
          new_password: newPassword,
        }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || "Reset password failed");
      }

      alert("Password updated successfully");

setTimeout(() => {
  navigate("/auth", { replace: true });
}, 1500);
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
                Reset password
              </div>

              <div
                style={{
                  color: "var(--muted)",
                  marginTop: 10,
                  fontSize: 15,
                  lineHeight: 1.6,
                }}
              >
                Create a new password for your account.
              </div>
            </div>

            <label style={labelStyle}>New password</label>
            <PasswordField
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter your new password"
              visible={showNewPassword}
              onToggle={() => setShowNewPassword((v) => !v)}
            />

            <div
              style={{
                fontSize: 12,
                color: "var(--muted)",
                marginTop: 6,
              }}
            >
              Password must contain at least 8 characters.
            </div>

            <label style={labelStyle}>Confirm password</label>
            <PasswordField
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your new password"
              visible={showConfirmPassword}
              onToggle={() => setShowConfirmPassword((v) => !v)}
            />

            <div style={{ marginTop: 24 }}>
              <button onClick={submit} style={primaryBtnStyle} disabled={loading}>
                {loading ? "Updating..." : "Reset password"}
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

function EyeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M2 12C3.8 8.5 7.3 6 12 6C16.7 6 20.2 8.5 22 12C20.2 15.5 16.7 18 12 18C7.3 18 3.8 15.5 2 12Z"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.8" />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M3 3L21 21" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      <path
        d="M10.6 10.7C10.2 11.1 10 11.5 10 12C10 13.1 10.9 14 12 14C12.5 14 12.9 13.8 13.3 13.4"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M6.7 6.8C4.7 8 3.1 9.8 2 12C3.8 15.5 7.3 18 12 18C14 18 15.8 17.5 17.4 16.5"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M9.9 5.2C10.6 5.1 11.3 5 12 5C16.7 5 20.2 7.5 22 11C21.4 12.2 20.6 13.3 19.7 14.2"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
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

const eyeBtnStyle = {
  position: "absolute",
  right: 16,
  top: "50%",
  transform: "translateY(-50%)",
  background: "none",
  border: "none",
  color: "var(--muted)",
  cursor: "pointer",
  padding: 0,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};