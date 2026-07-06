// src/services/sequencing.js
import { apiFetch } from "../utils/api";

// -- Recommandation adaptative complète (Agent 3) ------------------
export async function getFullRecommendation(moduleId) {
  const res = await apiFetch(`/api/v1/recommendation/full/${moduleId}`);
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Echec de la recommandation complete");
  }
  return res.json();
}
// -- Historique des recommandations ---------------------------
export async function getRecommendationHistory() {
  const res = await apiFetch("/api/v1/recommendation/history");
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Echec de l'historique");
  }
  return res.json();
}