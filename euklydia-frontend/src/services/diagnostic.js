import { api } from "./api";

export async function getQuestionnaire() {
  const res = await api.get("/diagnostic/questionnaire");
  return res.data;
}

export async function submitAnswers(answers) {
  const res = await api.post("/diagnostic/submit", { answers });
  return res.data;
}

export async function getResults() {
  const res = await api.get("/diagnostic/results");
  return res.data;
}

export async function getStatus() {
  const res = await api.get("/diagnostic/status");
  return res.data;
}