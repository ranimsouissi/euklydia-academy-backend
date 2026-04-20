import { api } from "./api";

export async function getQuestionnaire() {
  const res = await api.get("/assessment/questionnaire");
  return res.data;
}

export async function submitAnswers(answers) {
  // answers: [{question_id: 1, selected_option: "A"}, ...]
  const res = await api.post("/assessment/submit", { answers });
  return res.data; // [{skill_id, skill_name, score, level, priority}, ...]
}

export async function getResults() {
  const res = await api.get("/assessment/results");
  return res.data;
}

export async function getStatus() {
  const res = await api.get("/assessment/status");
  return res.data;
}