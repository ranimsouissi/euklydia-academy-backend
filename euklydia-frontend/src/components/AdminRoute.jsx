import { Navigate } from "react-router-dom";

export default function AdminRoute({ children }) {
  const isAdmin = (() => {
    try {
      const raw = localStorage.getItem("auth_user");
      if (!raw) return false;
      const user = JSON.parse(raw);
      return user?.role_id === 2 || user?.role === "admin";
    } catch {
      return false;
    }
  })();

  if (!isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}