import { useEffect, useMemo, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";

const OPTION_KEYS = ["A", "B", "C", "D"];
const OPTION_LABELS = {
  A: "option_a",
  B: "option_b",
  C: "option_c",
  D: "option_d",
};

// ─── Mapping career_path_id → détails du rôle ────────────────────────────────
const ROLE_MAP = {
  79: {
    name: "AI Sales Specialist",
    tag: "Sales",
    tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
  },
  80: {
    name: "AI Marketing Strategist",
    tag: "Go-to-Market",
    tagColor: { bg: "rgba(212,83,126,0.10)", color: "#993556" },
  },
  81: {
    name: "AI Designer",
    tag: "Creativity",
    tagColor: { bg: "rgba(127,119,221,0.10)", color: "#534AB7" },
  },
  82: {
    name: "AI Project Manager",
    tag: "Delivery",
    tagColor: { bg: "rgba(56,130,221,0.10)", color: "#1a5fa8" },
  },
};

// ─── Formatage de date lisible ───────────────────────────────────────────────
// Transforme "2026-08-08T12:23:51.661745" → "8 août 2026 à 12:23"
const formatCooldownDate = (isoString, lang) => {
  if (!isoString) return "—";
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return isoString;

    const locale = lang === "fr" ? "fr-FR" : "en-US";
    const dateStr = date.toLocaleDateString(locale, {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
    const timeStr = date.toLocaleTimeString(locale, {
      hour: "2-digit",
      minute: "2-digit",
      hour12: lang !== "fr",
    });
    const connector = lang === "fr" ? " à " : " at ";
    return `${dateStr}${connector}${timeStr}`;
  } catch {
    return isoString;
  }
};

export default function DiagnosticPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext() || {};
  const lang = language || "en";

  const [status, setStatus] = useState(null);
  const [questionnaire, setQuestionnaire] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  // ═══════════════════════════════════════════════════════════════════
  // Traductions UI
  // ═══════════════════════════════════════════════════════════════════
  const t = {
    en: {
      // Cooldown screen
      cooldownTitle: "Diagnostic not available",
      cooldownMessage: "You can retake the diagnostic from",
      backToRoadmap: "← Back to roadmap",
      // Header
      diagnosticBadge: "AI Diagnostic",
      diagnosticTitle: "Assess your AI skills",
      diagnosticSubtitle: "For each question, choose the best answer among the 4 options.",
      // Role banner
      yourSelectedRole: "Your selected role",
      changeRole: "Change role →",
      // Recommended banner
      updateRecommended: "Update recommended — your last diagnostic was more than 90 days ago.",
      // Progress
      progress: "Progress",
      // Empty state
      noQuestionnaire: "No questionnaire loaded.",
      // Footer
      questionsAnswered: "questions answered",
      diagnosticComplete: "✓ Diagnostic complete — ready to submit",
      answerAllQuestions: "Answer all questions to generate your path.",
      generateBtn: "Generate my personalized path →",
      generating: "Generating...",
      // Errors
      errStatusLoad: "Unable to load status",
      errQuestionnaireLoad: "Unable to load questionnaire",
      errQuestionnaireNotLoaded: "Questionnaire not loaded.",
      errAnswerAll: (a, t) => `Please answer all questions (${a}/${t}).`,
      errSubmit: "Submission failed",
      errGeneric: "Error",
    },
    fr: {
      // Cooldown screen
      cooldownTitle: "Diagnostic non disponible",
      cooldownMessage: "Vous pourrez refaire le diagnostic à partir du",
      backToRoadmap: "← Retour à la feuille de route",
      // Header
      diagnosticBadge: "Diagnostic IA",
      diagnosticTitle: "Évaluez vos compétences IA",
      diagnosticSubtitle: "Pour chaque question, choisissez la meilleure réponse parmi les 4 options.",
      // Role banner
      yourSelectedRole: "Votre rôle sélectionné",
      changeRole: "Changer de rôle →",
      // Recommended banner
      updateRecommended: "Mise à jour recommandée — votre dernier diagnostic date de plus de 90 jours.",
      // Progress
      progress: "Progression",
      // Empty state
      noQuestionnaire: "Aucun questionnaire chargé.",
      // Footer
      questionsAnswered: "questions répondues",
      diagnosticComplete: "✓ Diagnostic complet — prêt à soumettre",
      answerAllQuestions: "Répondez à toutes les questions pour générer votre parcours.",
      generateBtn: "Générer mon parcours personnalisé →",
      generating: "Génération en cours...",
      // Errors
      errStatusLoad: "Impossible de charger le statut",
      errQuestionnaireLoad: "Impossible de charger le questionnaire",
      errQuestionnaireNotLoaded: "Questionnaire non chargé.",
      errAnswerAll: (a, t) => `Veuillez répondre à toutes les questions (${a}/${t}).`,
      errSubmit: "Échec de la soumission",
      errGeneric: "Erreur",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        setError("");
        setLoading(true);

        const sRes = await apiFetch(`/api/v1/diagnostic/status`);
        if (!sRes) return;
        const sData = await sRes.json().catch(() => ({}));
        if (!sRes.ok) throw new Error(sData?.detail || t[lang].errStatusLoad);
        setStatus(sData);

        if (sData.has_scores && !sData.eligible) {
          setQuestionnaire(null);
          return;
        }

        const qRes = await apiFetch(`/api/v1/diagnostic/questionnaire`);
        if (!qRes) return;
        const qData = await qRes.json().catch(() => ({}));
        if (!qRes.ok) {
          const msg =
            typeof qData?.detail === "string"
              ? qData.detail
              : qData?.detail?.message || qData?.detail || t[lang].errQuestionnaireLoad;
          throw new Error(msg);
        }

        setQuestionnaire(qData);
        setAnswers({});
      } catch (e) {
        setError(e.message || t[lang].errGeneric);
      } finally {
        setLoading(false);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const totalQuestions = useMemo(
    () => questionnaire?.skills?.reduce((acc, s) => acc + (s?.questions?.length || 0), 0) || 0,
    [questionnaire]
  );
  const answeredCount = useMemo(() => Object.keys(answers).length, [answers]);
  const isComplete = totalQuestions > 0 && answeredCount === totalQuestions;

  const currentRole = questionnaire?.career_path_id
    ? ROLE_MAP[questionnaire.career_path_id]
    : null;

  const setAnswer = (questionId, option) =>
    setAnswers((prev) => ({ ...prev, [questionId]: option }));

  const submit = async () => {
    try {
      setError("");
      if (!questionnaire) { setError(t[lang].errQuestionnaireNotLoaded); return; }
      if (!isComplete) { setError(t[lang].errAnswerAll(answeredCount, totalQuestions)); return; }
      setSubmitting(true);

      const payload = {
        answers: Object.entries(answers).map(([qid, selected_option]) => ({
          question_id: Number(qid),
          selected_option,
        })),
      };

      const res = await apiFetch(`/api/v1/diagnostic/submit`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!res) return;

      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail?.message || data?.detail || t[lang].errSubmit);

      localStorage.setItem("diagnostic_results", JSON.stringify(data));
      navigate("/dashboard");
    } catch (e) {
      setError(e.message || t[lang].errGeneric);
    } finally {
      setSubmitting(false);
    }
  };

  // ── Loading ──
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 px-6 py-12">
        <div className="max-w-3xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-slate-200 rounded-xl w-1/2" />
            <div className="h-4 bg-slate-200 rounded-xl w-2/3" />
            <div className="h-48 bg-slate-200 rounded-2xl" />
          </div>
        </div>
      </div>
    );
  }

  // ── Cooldown ──
  if (status?.has_scores && status?.eligible === false) {
    return (
      <div className="min-h-screen bg-slate-50 px-6 py-12">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm text-center">
            <div className="w-14 h-14 rounded-full bg-amber-50 flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6v6l4 2m-4-8a9 9 0 110 18A9 9 0 0112 3z" />
              </svg>
            </div>
            <div className="text-lg font-semibold text-slate-900 mb-2">
              {t[lang].cooldownTitle}
            </div>
            <div className="text-slate-500 text-sm mb-6">
              {t[lang].cooldownMessage}{" "}
              <span className="font-semibold text-slate-900">
                {formatCooldownDate(status.next_allowed_at, lang)}
              </span>.
            </div>
            <button
              onClick={() => navigate("/roadmap")}
              className="px-5 py-2.5 rounded-xl border border-slate-200 bg-white font-semibold text-slate-700 hover:bg-slate-50 transition text-sm"
            >
              {t[lang].backToRoadmap}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-6">
      <div className="max-w-3xl mx-auto">

        {/* En-tête */}
        <div className="mb-6">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-teal-700 bg-teal-50 px-3 py-1.5 rounded-full mb-4 border border-teal-100">
            <span className="w-1.5 h-1.5 rounded-full bg-teal-500 inline-block" />
            {t[lang].diagnosticBadge}
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">
            {t[lang].diagnosticTitle}
          </h1>
          <p className="text-slate-500 text-sm leading-relaxed max-w-xl">
            {t[lang].diagnosticSubtitle}
          </p>
        </div>

        {/* ── Bandeau rappel du rôle ── */}
        {currentRole && (
          <div className="bg-white border border-slate-200 rounded-2xl px-5 py-4 mb-6 flex items-center justify-between gap-4 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-teal-50 flex items-center justify-center shrink-0">
                <svg className="w-4 h-4 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <div className="text-xs text-slate-400 font-medium mb-0.5">
                  {t[lang].yourSelectedRole}
                </div>
                <div className="flex items-center gap-2">
                  <span
                    style={{
                      display: "inline-flex", padding: "2px 8px", borderRadius: 999,
                      background: currentRole.tagColor.bg,
                      color: currentRole.tagColor.color,
                      fontWeight: 700, fontSize: 10,
                    }}
                  >
                    {currentRole.tag}
                  </span>
                  <span className="text-sm font-bold text-slate-900">
                    {currentRole.name}
                  </span>
                </div>
              </div>
            </div>
            <button
              onClick={() => navigate("/onboarding")}
              className="text-xs text-slate-400 hover:text-slate-600 font-medium transition whitespace-nowrap"
            >
              {t[lang].changeRole}
            </button>
          </div>
        )}

        {/* Recommended banner */}
        {status?.recommended && (
          <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 text-amber-800 px-4 py-3 rounded-xl text-sm mb-6">
            <svg className="w-4 h-4 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01M12 3a9 9 0 100 18A9 9 0 0012 3z" />
            </svg>
            {t[lang].updateRecommended}
          </div>
        )}

        {/* Barre de progression globale */}
        <div className="bg-white p-4 rounded-2xl border border-slate-200 mb-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-slate-500">{t[lang].progress}</span>
            <span className="font-bold text-slate-900">{answeredCount} / {totalQuestions}</span>
          </div>
          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-2 rounded-full bg-teal-500 transition-all duration-500"
              style={{ width: `${totalQuestions > 0 ? (answeredCount / totalQuestions) * 100 : 0}%` }}
            />
          </div>
        </div>

        {/* Erreur */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 text-sm flex items-center gap-2">
            <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
            {error}
          </div>
        )}

        {!questionnaire ? (
          <div className="bg-white p-6 rounded-2xl border border-slate-200 text-slate-500 text-sm">
            {t[lang].noQuestionnaire}
          </div>
        ) : (
          <div className="space-y-6">
            {questionnaire.skills.map((skill) => {
              const answeredInSkill = skill.questions.filter((q) => answers[q.id] !== undefined).length;
              const skillComplete = answeredInSkill === skill.questions.length;

              return (
                <div key={skill.id} className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                  <div className="px-6 pt-6 pb-4 flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-base font-bold text-slate-900">{skill.name}</h3>
                      {skill.description && (
                        <p className="text-sm text-slate-400 mt-0.5">{skill.description}</p>
                      )}
                    </div>
                    <span className={[
                      "text-xs font-bold px-2.5 py-1 rounded-full shrink-0",
                      skillComplete ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-400",
                    ].join(" ")}>
                      {answeredInSkill}/{skill.questions.length}
                    </span>
                  </div>

                  <div className="px-6 mb-4">
                    <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className={`h-1 rounded-full transition-all duration-400 ${skillComplete ? "bg-teal-400" : "bg-teal-300"}`}
                        style={{ width: `${skill.questions.length > 0 ? (answeredInSkill / skill.questions.length) * 100 : 0}%` }}
                      />
                    </div>
                  </div>

                  <div className="divide-y divide-slate-100">
                    {skill.questions.map((q, idx) => {
                      const selected = answers[q.id];
                      return (
                        <div key={q.id} className="px-6 py-5">
                          <p className="text-sm font-medium text-slate-800 leading-relaxed mb-4">
                            <span className="text-slate-400 font-medium mr-2">{idx + 1}.</span>
                            {q.text}
                          </p>
                          <div className="space-y-2">
                            {OPTION_KEYS.map((key) => {
                              const active = selected === key;
                              const optionText = q[OPTION_LABELS[key]];
                              if (!optionText) return null;
                              return (
                                <button
                                  key={key}
                                  type="button"
                                  onClick={() => setAnswer(q.id, key)}
                                  className={[
                                    "w-full text-left px-4 py-3 rounded-xl border transition-all duration-150 flex items-start gap-3",
                                    active
                                      ? "bg-teal-600 border-teal-600 text-white shadow-sm"
                                      : "bg-white border-slate-200 text-slate-600 hover:border-teal-300 hover:bg-teal-50",
                                  ].join(" ")}
                                >
                                  <span className={[
                                    "shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border",
                                    active
                                      ? "bg-white text-teal-600 border-white"
                                      : "bg-slate-100 text-slate-500 border-slate-200",
                                  ].join(" ")}>
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

            {/* Footer sticky */}
            <div className="sticky bottom-4 bg-white border border-slate-200 px-6 py-4 rounded-2xl shadow-lg flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <div className="text-sm text-slate-600">
                  <span className="font-bold text-slate-900">{answeredCount}</span>
                  <span className="text-slate-400"> / {totalQuestions} {t[lang].questionsAnswered}</span>
                </div>
                {isComplete
                  ? <div className="text-xs text-teal-600 font-semibold mt-0.5">{t[lang].diagnosticComplete}</div>
                  : <div className="text-xs text-slate-400 mt-0.5">{t[lang].answerAllQuestions}</div>
                }
              </div>
              <button
                onClick={submit}
                disabled={!isComplete || submitting}
                className={[
                  "px-6 py-3 rounded-xl font-bold text-sm text-white transition-all duration-200 whitespace-nowrap",
                  isComplete && !submitting
                    ? "bg-teal-600 hover:bg-teal-700 shadow-sm hover:-translate-y-0.5"
                    : "bg-slate-300 cursor-not-allowed",
                ].join(" ")}
              >
                {submitting ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                    {t[lang].generating}
                  </span>
                ) : (
                  t[lang].generateBtn
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}