// src/services/sequencing.js
import { apiFetch } from "../utils/api";

// -- Recommandation du module suivant -------------------------
export async function getNextRecommendation(moduleId) {
  const res = await apiFetch(`/api/v1/sequencing/next/${moduleId}`);
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Echec de la recommandation");
  }
  return res.json();
}

// -- Roadmap complet de l'apprenant ---------------------------
export async function getRoadmap() {
  const res = await apiFetch("/api/v1/sequencing/roadmap");
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Echec du roadmap");
  }
  return res.json();
}

// -- Recommandation adaptative complete (V2) ------------------
export async function getFullRecommendation(moduleId) {
  const res = await apiFetch(`/api/v1/recommendation/full/${moduleId}`);
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Echec de la recommandation complete");
  }
  return res.json();
}