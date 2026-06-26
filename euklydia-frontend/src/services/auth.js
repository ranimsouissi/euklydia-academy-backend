// src/services/auth.js

import { apiFetch } from "../utils/api";

export async function register(fullName, email, password, confirmPassword) {
  const res = await apiFetch("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify({
      full_name: fullName,
      email,
      password,
      confirm_password: confirmPassword,
    }),
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Registration failed");
  }
  return res.json();
}

export async function login(email, password) {
  const res = await apiFetch("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Login failed");
  }
  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  return data;
}

export async function me() {
  const res = await apiFetch("/api/v1/auth/me");
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Failed to fetch user");
  }
  const data = await res.json();
  localStorage.setItem("auth_user", JSON.stringify(data));
  return data;
}

export async function setMyCareerPath(careerPathId) {
  const res = await apiFetch(`/api/v1/auth/me/career-path/${careerPathId}`, {
    method: "PATCH",
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Failed to set career path");
  }
  return res.json();
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("auth_user");
  localStorage.removeItem("diagnostic_results");
  localStorage.removeItem("diagnostic_status");
}