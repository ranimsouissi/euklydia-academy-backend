// src/services/modules.js
import { apiFetch } from "../utils/api";

// ── Récupérer un module complet ──────────────────────────────
export async function getModule(moduleId) {
  const res = await apiFetch(`/api/v1/modules/${moduleId}`);
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Module introuvable");
  }
  return res.json();
}

// ── Démarrer un module ───────────────────────────────────────
export async function startModule(moduleId) {
  const res = await apiFetch(`/api/v1/modules/${moduleId}/start`, {
    method: "POST",
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec du démarrage");
  }
  return res.json();
}

// ── Mettre à jour une section ────────────────────────────────
export async function updateSection(moduleId, sectionType, status) {
  const res = await apiFetch(
    `/api/v1/modules/${moduleId}/section/${sectionType}`,
    {
      method: "POST",
      body: JSON.stringify({ status }),
    }
  );
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec de la mise à jour de la section");
  }
  return res.json();
}

// ── Soumettre l'Execution Task ───────────────────────────────
export async function submitExecutionTask(moduleId, { url, kpiAfter, difficulty }) {
  const res = await apiFetch(
    `/api/v1/modules/${moduleId}/execution-task/submit`,
    {
      method: "POST",
      body: JSON.stringify({
        url,
        kpi_after: kpiAfter,
        difficulty: difficulty || null,
      }),
    }
  );
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec de la soumission");
  }
  return res.json();
}

// ── Compléter un module ──────────────────────────────────────
export async function completeModule(moduleId) {
  const res = await apiFetch(`/api/v1/modules/${moduleId}/complete`, {
    method: "POST",
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec de la complétion");
  }
  return res.json();
}