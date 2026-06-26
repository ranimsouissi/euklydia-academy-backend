import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { setMyCareerPath } from "../services/auth";
import { getCareerPaths } from "../services/careerPaths";
import { apiFetch } from "../utils/api";
import { ROLE_DETAILS, whatYoullGetItems } from "../data/roles";

const OPTION_KEYS = ["A", "B", "C", "D"];
const OPTION_LABELS = { A: "option_a", B: "option_b", C: "option_c", D: "option_d" };

export default function OnboardingPage() {
  const navigate = useNavigate();
  const [careerPaths, setCareerPaths] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [loadingCP, setLoadingCP] = useState(true);
  const [savingCP, setSavingCP] = useState(false);
  const [questionnaire, setQuestionnaire] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loadingQ, setLoadingQ] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [modalRoleId, setModalRoleId] = useState(null); // ← Modal au lieu d'expansion

  useEffect(() => {
    async function load() {
      try {
        setError("");
        setLoadingCP(true);
        const data = await getCareerPaths();
        const activeRoles = Object.keys(ROLE_DETAILS);
        setCareerPaths(data.filter((cp) => activeRoles.includes(cp.name)));
      } catch (e) {
        setError(e?.response?.data?.detail || e.message);
      } finally {
        setLoadingCP(false);
      }
    }
    load();
  }, []);

  // Fermer le modal avec la touche Escape
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") setModalRoleId(null);
    };
    if (modalRoleId) {
      window.addEventListener("keydown", handleEsc);
      document.body.style.overflow = "hidden"; // empêche le scroll en arrière-plan
    }
    return () => {
      window.removeEventListener("keydown", handleEsc);
      document.body.style.overflow = "";
    };
  }, [modalRoleId]);

  const loadQuestionnaire = async () => {
    try {
      setError("");
      setLoadingQ(true);
      const res = await apiFetch("/api/v1/diagnostic/questionnaire");
      if (!res) return;
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.detail || "Failed to load diagnostic");
        return;
      }
      const data = await res.json();
      setQuestionnaire(data);
      setAnswers({});
    } catch (e) {
      setError(e.message || "Error loading diagnostic");
    } finally {
      setLoadingQ(false);
    }
  };

  const handleSelectCareerPath = async (cpId) => {
    try {
      setError("");
      setSelectedId(cpId);
      setSavingCP(true);
      setModalRoleId(null); // ferme le modal s'il est ouvert
      await setMyCareerPath(cpId);
      await loadQuestionnaire();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setSavingCP(false);
    }
  };

  const setAnswer = (questionId, option) =>
    setAnswers((prev) => ({ ...prev, [questionId]: option }));

  const totalQuestions = useMemo(
    () => questionnaire?.skills?.reduce((acc, skill) => acc + (skill?.questions?.length || 0), 0) || 0,
    [questionnaire]
  );
  const answeredCount = useMemo(() => Object.keys(answers).length, [answers]);
  const isComplete = totalQuestions > 0 && answeredCount === totalQuestions;

  const handleSubmit = async () => {
    try {
      setError("");
      if (!questionnaire) { setError("No diagnostic loaded."); return; }
      if (!isComplete) { setError(`Please answer all questions (${answeredCount}/${totalQuestions}).`); return; }
      setSubmitting(true);

      const payload = {
        answers: Object.entries(answers).map(([qid, selected_option]) => ({
          question_id: Number(qid),
          selected_option,
        })),
      };

      const res = await apiFetch("/api/v1/diagnostic/submit", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!res) return;
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.detail?.message || data?.detail || "Submit failed");
        return;
      }
      const data = await res.json();
      localStorage.setItem("diagnostic_results", JSON.stringify(data));
      navigate("/dashboard");
    } catch (e) {
      setError(e.message || "Error");
    } finally {
      setSubmitting(false);
    }
  };

  // Récupère le rôle actif pour le modal
  const modalCareerPath = careerPaths.find((cp) => cp.id === modalRoleId);
  const modalDetails = modalCareerPath ? ROLE_DETAILS[modalCareerPath.name] : null;

  if (loadingCP) {
    return (
      <div className="min-h-screen bg-slate-50 px-6 py-12">
        <div className="max-w-5xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-slate-200 rounded-xl w-1/3" />
            <div className="h-4 bg-slate-200 rounded-xl w-1/2" />
            <div className="grid md:grid-cols-2 gap-4">
              {[1,2,3,4].map(i => <div key={i} className="h-64 bg-slate-200 rounded-2xl" />)}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-6">
      <div className="max-w-5xl mx-auto">

        {/* ─── Header ────────────── */}
        <div className="mb-10">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-teal-700 bg-teal-50 px-3 py-1.5 rounded-full mb-4 border border-teal-100">
            <span className="w-1.5 h-1.5 rounded-full bg-teal-500 inline-block" />
            Welcome to Euklydia Academy
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">
            Choose your role — master 3 business use cases
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed max-w-xl">
            Each role unlocks 3 concrete use cases with measurable KPIs and ready-to-use AI Blueprints. Pick the path that matches your day-to-day.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 text-sm">{error}</div>
        )}

        {/* STEP 1 — Choix du rôle */}
        <section className="mb-12">
          <div className="mb-5">
            <h2 className="text-base font-semibold text-slate-900">
              <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-teal-600 text-white text-xs font-bold mr-2">1</span>
              Choose your role
            </h2>
            <p className="text-sm text-slate-400 mt-1 ml-8">
              Click "See details" for KPIs Before → After and AI Blueprints.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {careerPaths.map((cp) => {
              const selected = selectedId === cp.id;
              const details = ROLE_DETAILS[cp.name];

              return (
                <div key={cp.id} style={{
                  background: "#fff",
                  border: selected ? "2px solid #006355" : "1px solid #E5E7EB",
                  borderRadius: 20,
                  transition: "all 0.2s ease",
                  position: "relative",
                  overflow: "hidden",
                  boxShadow: selected
                    ? "0 0 0 4px rgba(0,99,85,0.08)"
                    : "0 4px 20px rgba(2,6,23,0.06)",
                }}>
                  <div style={{ padding: 20, position: "relative" }}>

                    {/* Cercle décoratif en haut à droite */}
                    {details && (
                      <div style={{
                        position: "absolute",
                        top: -20, right: -20,
                        width: 70, height: 70, borderRadius: "50%",
                        background: details.tagColor.bg,
                        opacity: 0.6,
                      }} />
                    )}

                    {/* Header : Tag + nom + forWho + badge "3 use cases" */}
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12, marginBottom: 12, position: "relative" }}>
                      <div style={{ flex: 1 }}>
                        {details && (
                          <span style={{
                            display: "inline-flex", padding: "5px 10px", borderRadius: 999,
                            background: selected ? "rgba(0,99,85,0.10)" : details.tagColor.bg,
                            color: selected ? "#006355" : details.tagColor.color,
                            fontWeight: 800, fontSize: 11, marginBottom: 8,
                          }}>
                            {details.tag}
                          </span>
                        )}
                        <div style={{ fontSize: 16, fontWeight: 900, color: "#0f172a", marginBottom: 2 }}>
                          {cp.name}
                        </div>
                        {details && (
                          <div style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8" }}>
                            For: {details.forWho}
                          </div>
                        )}
                      </div>

                      {/* Badge 3 use cases */}
                      {details && (
                        <div style={{
                          flexShrink: 0,
                          background: "rgba(0,179,160,0.08)",
                          borderRadius: 12, padding: "6px 10px",
                          textAlign: "center",
                          border: "1px solid rgba(0,179,160,0.15)",
                        }}>
                          <div style={{ fontSize: 16, fontWeight: 900, color: "#006355" }}>3</div>
                          <div style={{ fontSize: 9, fontWeight: 700, color: "#64748b", lineHeight: 1.2 }}>use<br/>cases</div>
                        </div>
                      )}
                    </div>

                    {/* Description */}
                    <p style={{ fontSize: 13, color: "#64748b", lineHeight: 1.6, margin: "0 0 14px" }}>
                      {details ? details.desc : cp.description}
                    </p>

                    {/* Aperçu des 3 use cases */}
                    {details && (
                      <div style={{
                        background: "#F8FAFC",
                        borderRadius: 12,
                        padding: "12px 14px",
                        marginBottom: 14,
                        border: "1px solid #F1F5F9",
                      }}>
                        <div style={{
                          fontSize: 10,
                          fontWeight: 900,
                          color: "#94a3b8",
                          textTransform: "uppercase",
                          letterSpacing: "0.06em",
                          marginBottom: 8,
                        }}>
                          Use cases you'll master
                        </div>
                        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                          {details.useCases.map((uc) => (
                            <div key={uc.name} style={{
                              display: "flex",
                              alignItems: "center",
                              gap: 8,
                              fontSize: 12,
                              color: "#0f172a",
                              fontWeight: 600,
                            }}>
                              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" style={{ flexShrink: 0 }}>
                                <circle cx="12" cy="12" r="11" fill="rgba(0,179,160,0.15)" />
                                <path
                                  d="M7 12.5L10.5 16L17 9"
                                  stroke="#006355"
                                  strokeWidth="2.5"
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                />
                              </svg>
                              <span>{uc.name}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Boutons d'action */}
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <button
                        onClick={() => handleSelectCareerPath(cp.id)}
                        disabled={savingCP}
                        style={{
                          flex: 1,
                          padding: "10px 14px",
                          borderRadius: 12,
                          fontSize: 13,
                          fontWeight: 800,
                          cursor: savingCP ? "not-allowed" : "pointer",
                          opacity: savingCP ? 0.6 : 1,
                          transition: "all 0.2s",
                          border: selected ? "none" : "1px solid #E5E7EB",
                          background: selected ? "#006355" : "#F8FAFC",
                          color: selected ? "#fff" : "#0f172a",
                        }}
                      >
                        {selected ? "Path selected ✓" : "Choose this path"}
                      </button>
                      {details && (
                        <button
                          onClick={() => setModalRoleId(cp.id)}
                          style={{
                            padding: "10px 14px",
                            borderRadius: 12,
                            fontSize: 13,
                            fontWeight: 700,
                            cursor: "pointer",
                            border: "1px solid #E5E7EB",
                            background: "#fff",
                            color: "#64748b",
                            whiteSpace: "nowrap",
                            transition: "all 0.2s",
                          }}
                        >
                          See details →
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* MODAL — Détails du rôle (KPIs + Blueprints + What You'll Get) */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {modalRoleId && modalDetails && modalCareerPath && (
          <div
            onClick={() => setModalRoleId(null)}
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(15, 23, 42, 0.55)",
              backdropFilter: "blur(4px)",
              zIndex: 1000,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 20,
              animation: "fadeIn 0.2s ease",
            }}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              style={{
                background: "#fff",
                borderRadius: 24,
                maxWidth: 720,
                width: "100%",
                maxHeight: "90vh",
                overflowY: "auto",
                position: "relative",
                boxShadow: "0 25px 80px rgba(2,6,23,0.25)",
                animation: "slideUp 0.3s ease",
              }}
            >
              {/* Bouton fermer */}
              <button
                onClick={() => setModalRoleId(null)}
                style={{
                  position: "absolute",
                  top: 16,
                  right: 16,
                  width: 36,
                  height: 36,
                  borderRadius: "50%",
                  background: "#F1F5F9",
                  border: "none",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 18,
                  color: "#64748b",
                  fontWeight: 800,
                  transition: "all 0.2s",
                  zIndex: 2,
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = "#E2E8F0";
                  e.currentTarget.style.color = "#0f172a";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = "#F1F5F9";
                  e.currentTarget.style.color = "#64748b";
                }}
                aria-label="Close modal"
              >
                ✕
              </button>

              {/* Header du modal */}
              <div style={{
                padding: "28px 32px 20px",
                borderBottom: "1px solid #F1F5F9",
                position: "relative",
                overflow: "hidden",
              }}>
                {/* Cercle décoratif */}
                <div style={{
                  position: "absolute",
                  top: -40, right: -40,
                  width: 120, height: 120, borderRadius: "50%",
                  background: modalDetails.tagColor.bg,
                  opacity: 0.5,
                }} />

                <div style={{ position: "relative" }}>
                  <span style={{
                    display: "inline-flex", padding: "5px 12px", borderRadius: 999,
                    background: modalDetails.tagColor.bg,
                    color: modalDetails.tagColor.color,
                    fontWeight: 800, fontSize: 11, marginBottom: 10,
                  }}>
                    {modalDetails.tag}
                  </span>
                  <h2 style={{
                    fontSize: 24,
                    fontWeight: 900,
                    color: "#0f172a",
                    margin: "0 0 6px",
                    paddingRight: 40,
                  }}>
                    {modalCareerPath.name}
                  </h2>
                  <div style={{ fontSize: 12, color: "#006355", fontWeight: 700, marginBottom: 12 }}>
                    For: {modalDetails.forWho}
                  </div>
                  <p style={{
                    fontSize: 13,
                    color: "#64748b",
                    lineHeight: 1.7,
                    margin: 0,
                    fontStyle: "italic",
                  }}>
                    {modalDetails.roleContext}
                  </p>
                </div>
              </div>

              {/* Corps du modal */}
              <div style={{ padding: "24px 32px 28px" }}>

                {/* Section : 3 Use Cases — KPIs & Blueprints */}
                <div style={{ marginBottom: 24 }}>
                  <div style={{
                    fontSize: 10,
                    fontWeight: 900,
                    color: "#94a3b8",
                    textTransform: "uppercase",
                    letterSpacing: "0.07em",
                    marginBottom: 12,
                  }}>
                    3 Use Cases — KPIs &amp; Blueprints
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    {modalDetails.useCases.map((uc, idx) => (
                      <div key={uc.name} style={{
                        background: "rgba(0,179,160,0.04)",
                        border: "1px solid rgba(0,179,160,0.18)",
                        borderRadius: 14,
                        padding: "14px 16px",
                      }}>
                        {/* Numéro + nom */}
                        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                          <span style={{
                            width: 22, height: 22, borderRadius: "50%",
                            background: "rgba(0,179,160,0.20)", color: "#006355",
                            display: "inline-flex", alignItems: "center", justifyContent: "center",
                            fontSize: 11, fontWeight: 900, flexShrink: 0,
                          }}>
                            {idx + 1}
                          </span>
                          <span style={{ fontSize: 14, fontWeight: 900, color: "#0f172a" }}>
                            {uc.name}
                          </span>
                        </div>

                        {/* KPI Before → After */}
                        <div style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 8,
                          flexWrap: "wrap",
                          background: "#fff",
                          borderRadius: 10,
                          padding: "8px 12px",
                          marginBottom: 8,
                        }}>
                          <span style={{
                            fontSize: 10,
                            fontWeight: 700,
                            color: "#94a3b8",
                            textTransform: "uppercase",
                            letterSpacing: "0.05em",
                          }}>
                            Before:
                          </span>
                          <span style={{ fontSize: 12, color: "#64748b" }}>{uc.kpiBefore}</span>
                          <span style={{ color: "#00B3A0", fontSize: 14, fontWeight: 900 }}>→</span>
                          <span style={{
                            fontSize: 10,
                            fontWeight: 700,
                            color: "#006355",
                            textTransform: "uppercase",
                            letterSpacing: "0.05em",
                          }}>
                            After:
                          </span>
                          <span style={{ fontSize: 12, fontWeight: 800, color: "#0f172a" }}>
                            {uc.kpiAfter}
                          </span>
                        </div>

                        {/* Blueprint */}
                        <div style={{
                          display: "inline-flex",
                          alignItems: "center",
                          gap: 6,
                          fontSize: 11,
                          fontWeight: 800,
                          color: "#534AB7",
                          background: "rgba(127,119,221,0.10)",
                          padding: "4px 10px",
                          borderRadius: 999,
                        }}>
                          <span>📦</span>
                          <span>{uc.blueprint}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Section : What You'll Get */}
                <div style={{ marginBottom: 24 }}>
                  <div style={{
                    fontSize: 10,
                    fontWeight: 900,
                    color: "#94a3b8",
                    textTransform: "uppercase",
                    letterSpacing: "0.07em",
                    marginBottom: 12,
                  }}>
                    What You'll Get
                  </div>
                  <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(2, 1fr)",
                    gap: 10,
                  }} className="modalWhatGrid">
                    {whatYoullGetItems.map((item) => (
                      <div key={item.label} style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        background: "#F8FAFC",
                        border: "1px solid #E5E7EB",
                        borderRadius: 12,
                        padding: "12px 14px",
                      }}>
                        <span style={{ fontSize: 18, flexShrink: 0 }}>{item.icon}</span>
                        <span style={{
                          fontSize: 12,
                          fontWeight: 700,
                          color: "#0f172a",
                          lineHeight: 1.4,
                        }}>
                          {item.label}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CTA */}
                <button
                  onClick={() => handleSelectCareerPath(modalCareerPath.id)}
                  disabled={savingCP}
                  style={{
                    width: "100%",
                    padding: "14px 20px",
                    borderRadius: 14,
                    background: "#006355",
                    color: "#fff",
                    fontWeight: 900,
                    fontSize: 14,
                    border: "none",
                    cursor: savingCP ? "not-allowed" : "pointer",
                    opacity: savingCP ? 0.6 : 1,
                    transition: "all 0.2s",
                    boxShadow: "0 4px 16px rgba(0,99,85,0.20)",
                  }}
                  onMouseEnter={(e) => !savingCP && (e.currentTarget.style.background = "#004d42")}
                  onMouseLeave={(e) => !savingCP && (e.currentTarget.style.background = "#006355")}
                >
                  Choose this path →
                </button>
              </div>
            </div>

            <style>{`
              @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
              }
              @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px) scale(0.96); }
                to { opacity: 1; transform: translateY(0) scale(1); }
              }
              @media (max-width: 640px) {
                .modalWhatGrid { grid-template-columns: 1fr !important; }
              }
            `}</style>
          </div>
        )}

        {/* STEP 2 — Diagnostic */}
        <section>
          <div className="mb-5">
            <h2 className="text-base font-semibold text-slate-900">
              <span className={[
                "inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold mr-2",
                selectedId ? "bg-teal-600 text-white" : "bg-slate-200 text-slate-400",
              ].join(" ")}>2</span>
              Diagnose your current AI skills
            </h2>
            <p className="text-sm text-slate-400 mt-1 ml-8">
              A 9-question diagnostic to personalize your path. Takes about 10 minutes.
            </p>
          </div>

          {!selectedId ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center">
              <div className="text-slate-300 text-3xl mb-3">🔒</div>
              <div className="text-slate-500 text-sm">Select your role first to access the diagnostic.</div>
            </div>
          ) : loadingQ ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200">
              <div className="animate-pulse space-y-3">
                <div className="h-4 bg-slate-200 rounded w-1/2" />
                <div className="h-16 bg-slate-200 rounded-xl" />
                <div className="h-16 bg-slate-200 rounded-xl" />
              </div>
            </div>
          ) : !questionnaire ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 text-slate-500 text-sm">No diagnostic loaded.</div>
          ) : (
            <div className="space-y-6">
              <div className="bg-white p-4 rounded-2xl border border-slate-200">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-500">Progress</span>
                  <span className="font-bold text-slate-900">{answeredCount} / {totalQuestions}</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-2 rounded-full bg-teal-500 transition-all duration-500"
                    style={{ width: `${totalQuestions > 0 ? (answeredCount / totalQuestions) * 100 : 0}%` }} />
                </div>
              </div>

              {questionnaire.skills.map((skill) => {
                const answeredInSkill = skill.questions.filter((q) => answers[q.id] !== undefined).length;
                const skillComplete = answeredInSkill === skill.questions.length;
                return (
                  <div key={skill.id} className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="px-6 pt-6 pb-4 flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-base font-bold text-slate-900">{skill.name}</h3>
                        {skill.description && <p className="text-sm text-slate-400 mt-0.5">{skill.description}</p>}
                      </div>
                      <span className={["text-xs font-bold px-2.5 py-1 rounded-full shrink-0",
                        skillComplete ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-400"].join(" ")}>
                        {answeredInSkill}/{skill.questions.length}
                      </span>
                    </div>
                    <div className="px-6 mb-4">
                      <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                        <div className={`h-1 rounded-full transition-all duration-400 ${skillComplete ? "bg-teal-400" : "bg-teal-300"}`}
                          style={{ width: `${skill.questions.length > 0 ? (answeredInSkill / skill.questions.length) * 100 : 0}%` }} />
                      </div>
                    </div>
                    <div className="divide-y divide-slate-100">
                      {skill.questions.map((q, idx) => {
                        const selected = answers[q.id];
                        return (
                          <div key={q.id} className="px-6 py-5">
                            <p className="text-sm font-medium text-slate-800 leading-relaxed mb-4">
                              <span className="text-slate-400 font-medium mr-2">{idx + 1}.</span>{q.text}
                            </p>
                            <div className="space-y-2">
                              {OPTION_KEYS.map((key) => {
                                const active = selected === key;
                                const optionText = q[OPTION_LABELS[key]];
                                if (!optionText) return null;
                                return (
                                  <button key={key} type="button" onClick={() => setAnswer(q.id, key)}
                                    className={["w-full text-left px-4 py-3 rounded-xl border transition-all duration-150 flex items-start gap-3",
                                      active ? "bg-teal-600 border-teal-600 text-white shadow-sm" : "bg-white border-slate-200 text-slate-600 hover:border-teal-300 hover:bg-teal-50"].join(" ")}>
                                    <span className={["shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border",
                                      active ? "bg-white text-teal-600 border-white" : "bg-slate-100 text-slate-500 border-slate-200"].join(" ")}>
                                      {key}
                                    </span>
                                    <span className="text-sm leading-relaxed">{optionText}</span>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}

              <div className="sticky bottom-4 bg-white border border-slate-200 px-6 py-4 rounded-2xl shadow-lg flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <div className="text-sm text-slate-600">
                    <span className="font-bold text-slate-900">{answeredCount}</span>
                    <span className="text-slate-400"> / {totalQuestions} questions answered</span>
                  </div>
                  {isComplete
                    ? <div className="text-xs text-teal-600 font-semibold mt-0.5">✓ Diagnostic complete — ready to submit</div>
                    : <div className="text-xs text-slate-400 mt-0.5">Answer all questions to generate your path.</div>
                  }
                </div>
                <button onClick={handleSubmit} disabled={!isComplete || submitting}
                  className={["px-6 py-3 rounded-xl font-bold text-sm text-white transition-all duration-200 whitespace-nowrap",
                    isComplete && !submitting ? "bg-teal-600 hover:bg-teal-700 shadow-sm hover:-translate-y-0.5" : "bg-slate-300 cursor-not-allowed"].join(" ")}>
                  {submitting ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                      </svg>
                      Generating...
                    </span>
                  ) : "Generate my personalized path →"}
                </button>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}