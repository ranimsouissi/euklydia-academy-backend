import { apiFetch } from "../utils/api";

export async function getCareerPaths() {
  const res = await apiFetch("/api/v1/career-paths");
  if (!res) return [];
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Failed to fetch career paths");
  }
  return res.json();
}