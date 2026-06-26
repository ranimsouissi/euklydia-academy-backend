// src/services/coaching.js
import { apiFetch } from "../utils/api";

// ── Créer une session tuteur ─────────────────────────────────
export async function createSession({ userId, moduleId, sectionType, kpiBaseline, diagnosticScore }) {
  const res = await apiFetch("/api/v1/coaching/sessions", {
    method: "POST",
    body: JSON.stringify({
      user_id: userId,
      module_id: moduleId,
      section_type: sectionType || "execution_content",
      kpi_baseline: kpiBaseline || null,
      diagnostic_score: diagnosticScore || null,
    }),
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec de création de session");
  }
  return res.json();
}

// ── Envoyer un message au tuteur ─────────────────────────────
export async function sendChatMessage(sessionId, { userId, moduleId, sectionType, message }) {
  const res = await apiFetch(`/api/v1/coaching/sessions/${sessionId}/chat`, {
    method: "POST",
    body: JSON.stringify({
      session_id: sessionId,
      user_id: userId,
      module_id: moduleId,
      section_type: sectionType || "execution_content",
      message,
    }),
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec de l'envoi du message");
  }
  return res.json();
}

// ── Feedback post-soumission de l'Execution Task ─────────────
export async function getExecutionTaskFeedback({ moduleId, moduleTitle, kpiBefore, kpiAfter, difficulty, sectionType }) {
  const res = await apiFetch("/api/v1/coaching/execution-task/feedback", {
    method: "POST",
    body: JSON.stringify({
      module_id: moduleId,
      module_title: moduleTitle,
      kpi_before: kpiBefore || null,
      kpi_after: kpiAfter,
      difficulty: difficulty || null,
      section_type: sectionType || "execution_task",
    }),
  });
  if (!res) return null;
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Échec du feedback");
  }
  return res.json();
}

// ── Fermer une session ───────────────────────────────────────
export async function closeSession(sessionId) {
  const res = await apiFetch(`/api/v1/coaching/sessions/${sessionId}/close`, {
    method: "PATCH",
  });
  if (!res) return null;
  return res.json();
}