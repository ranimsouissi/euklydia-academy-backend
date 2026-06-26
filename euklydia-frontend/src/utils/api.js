// src/utils/api.js

const API = process.env.REACT_APP_API_URL;

/**
 * Helper centralisé pour tous les appels API.
 * Gère automatiquement :
 * - L'ajout du token Authorization
 * - La redirection vers /auth si token expiré (401)
 * - Le nettoyage du localStorage
 */
export async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem("token");

  const headers = {
    ...(options.body && !(options.body instanceof FormData)
      ? { "Content-Type": "application/json" }
      : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };
  try {
    const res = await fetch(`${API}${endpoint}`, {
      ...options,
      headers,
    });

    // ✅ Token expiré ou invalide → nettoyage + redirect
    if (res.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("auth_user");
      localStorage.removeItem("diagnostic_status");
      localStorage.removeItem("diagnostic_results");
      window.location.replace("/auth");
      return null;
    }

    return res;
  } catch (error) {
    console.error(`API error on ${endpoint}:`, error);
    throw error;
  }
}