import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const API = process.env.REACT_APP_API_URL;

export default function AuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      const params = new URLSearchParams(window.location.search);
      const token = params.get("token");

      if (!token) {
        navigate("/auth", { replace: true });
        return;
      }

      localStorage.setItem("token", token);

      const meRes = await fetch(`${API}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!meRes.ok) {
        localStorage.removeItem("token");
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
        headers: { Authorization: `Bearer ${token}` },
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
    })();
  }, [navigate]);

  return <div style={{ padding: 40 }}>Connexion en cours...</div>;
}