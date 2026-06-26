import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";

import {
  getModule,
  startModule,
  submitExecutionTask,
  completeModule,
} from "../services/modules";
import { getFullRecommendation } from "../services/sequencing";
import {
  createSession,
  sendChatMessage,
  getExecutionTaskFeedback,
} from "../services/coaching";

// ─────────────────────────────────────────────────────────────────────────
// TutorChat — Coaching Agent flottant (Agent 1)
// Utilise module_id + section_type (plus de lesson_id)
// ─────────────────────────────────────────────────────────────────────────
function TutorChat({ moduleId, userId, kpiBaseline, lang }) {
  const [open, setOpen] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionLoading, setSessionLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Section active du tuteur — par défaut execution_content
  const sectionType = "execution_content";

  const l = lang === "en" ? {
    btn: "Ask the tutor", title: "Euklydia Tutor",
    subtitle: "Ask your questions about this module",
    placeholder: "Ask your question...",
    welcome: "Hello! I'm your tutor for this module. Feel free to ask me anything.",
    error: "Error — please retry.",
  } : {
    btn: "Demander au tuteur", title: "Tuteur Euklydia",
    subtitle: "Posez vos questions sur ce module",
    placeholder: "Posez votre question...",
    welcome: "Bonjour ! Je suis votre tuteur pour ce module. Posez-moi vos questions.",
    error: "Erreur — réessayez.",
  };

  const handleOpen = async () => {
    setOpen(true);
    if (sessionId) return;
    try {
      setSessionLoading(true);
      const data = await createSession({
        userId,
        moduleId,
        sectionType,
        kpiBaseline,
      });
      if (data?.session_id) {
        setSessionId(data.session_id);
        setMessages([{ role: "assistant", content: l.welcome }]);
      }
    } catch { /* non-blocking */ }
    finally { setSessionLoading(false); }
  };

  const sendMessage = async () => {
    if (!input.trim() || !sessionId || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    try {
      const data = await sendChatMessage(sessionId, {
        userId,
        moduleId,
        sectionType,
        message: userMsg,
      });
      if (data?.answer) {
        setMessages(prev => [...prev, {
          role: "assistant",
          content: data.answer,
          citations: data.citations,
        }]);
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: l.error }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: l.error }]);
    } finally { setLoading(false); }
  };

  useEffect(() => {
    if (open) messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  return (
    <>
      <button onClick={handleOpen}
  className={`fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-2xl bg-euk-primary px-4 py-3 text-sm font-bold text-white shadow-lg transition hover:bg-euk-deep active:scale-95 ${open ? "hidden" : ""}`}
        style={{ boxShadow: "0 4px 24px rgba(0,0,0,0.15)" }}>
        <span className="text-base">💬</span>{l.btn}
      </button>
      {open && (
        <div className="fixed bottom-6 right-6 z-50 flex w-72 flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl md:w-80"
  style={{ height: "420px", maxHeight: "60vh", boxShadow: "0 8px 40px rgba(0,0,0,0.18)" }}>
          <div className="flex items-center justify-between border-b border-slate-100 bg-euk-primary px-4 py-3">
            <div>
              <div className="text-sm font-bold text-white">{l.title}</div>
              <div className="text-xs text-white/70">{l.subtitle}</div>
            </div>
            <button onClick={() => setOpen(false)}
              className="flex h-7 w-7 items-center justify-center rounded-xl bg-white/20 text-white transition hover:bg-white/30">✕</button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50/50">
            {sessionLoading ? (
              <div className="flex items-center justify-center h-full">
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  {msg.role === "assistant" && (
                    <div className="mr-2 flex h-7 w-7 shrink-0 items-center justify-center rounded-xl bg-euk-primary/10 text-sm">🤖</div>
                  )}
                  <div className={`max-w-[80%] rounded-2xl px-3 py-2 text-sm leading-6 ${msg.role === "user" ? "bg-euk-primary text-white rounded-br-sm" : "bg-white border border-slate-200 text-slate-700 rounded-bl-sm"}`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.citations?.length > 0 && (
                      <div className="mt-1.5 flex flex-wrap gap-1">
                        {msg.citations.map((c, i) => (
                          <span key={i} className="rounded-full bg-euk-primary/10 px-2 py-0.5 text-xs font-semibold text-euk-primary">[{c}]</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="mr-2 flex h-7 w-7 shrink-0 items-center justify-center rounded-xl bg-euk-primary/10 text-sm">🤖</div>
                <div className="rounded-2xl rounded-bl-sm border border-slate-200 bg-white px-3 py-2">
                  <div className="flex items-center gap-1.5">
                    <div className="h-1.5 w-1.5 animate-bounce rounded-full bg-euk-primary" style={{ animationDelay: "0ms" }} />
                    <div className="h-1.5 w-1.5 animate-bounce rounded-full bg-euk-primary" style={{ animationDelay: "150ms" }} />
                    <div className="h-1.5 w-1.5 animate-bounce rounded-full bg-euk-primary" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="border-t border-slate-100 bg-white p-3">
            <div className="flex items-end gap-2">
              <textarea value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown}
                placeholder={l.placeholder} rows={1} disabled={!sessionId || loading}
                className="flex-1 resize-none rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-euk-primary focus:ring-1 focus:ring-euk-primary disabled:opacity-50"
                style={{ maxHeight: "100px" }} />
              <button onClick={sendMessage} disabled={!input.trim() || !sessionId || loading}
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-euk-primary text-white transition hover:bg-euk-deep disabled:cursor-not-allowed disabled:opacity-40">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="h-4 w-4">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ─────────────────────────────────────────────────────────────────────────
// Sous-composants utilitaires
// ─────────────────────────────────────────────────────────────────────────

function SectionHeader({ title, subtitle }) {
  return (
    <div className="mb-5">
      <h2 className="text-lg font-bold text-euk-dark md:text-xl">{title}</h2>
      {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
    </div>
  );
}

function ProgramItem({ icon, label, content, accent, iconBg, labelColor }) {
  return (
    <div className={["flex items-start gap-3 rounded-2xl border p-4", accent].join(" ")}>
      <div className={["flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-lg", iconBg].join(" ")}>{icon}</div>
      <div className="min-w-0 flex-1">
        <div className={["text-xs font-bold uppercase tracking-wide", labelColor].join(" ")}>{label}</div>
        <div className="mt-1.5 text-sm leading-6 text-slate-700">{content}</div>
      </div>
    </div>
  );
}

function PromptCard({ prompt, isCopied, onCopy }) {
  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50/50">
      <header className="border-b border-slate-200 bg-white p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <h3 className="text-base font-bold text-euk-dark">{prompt.title}</h3>
            {prompt.use_case && (
              <p className="mt-1 text-sm text-slate-500"><span className="font-medium">Cas d'usage :</span> {prompt.use_case}</p>
            )}
          </div>
          <button onClick={onCopy}
            className={`shrink-0 rounded-xl px-3 py-2 text-xs font-bold transition ${isCopied ? "bg-emerald-500 text-white" : "bg-euk-primary text-white hover:bg-euk-deep"}`}>
            {isCopied ? "Copié ✓" : "📋 Copier"}
          </button>
        </div>
        {prompt.tags?.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {prompt.tags.map((tag, i) => (
              <span key={i} className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs font-medium text-slate-600">{tag}</span>
            ))}
          </div>
        )}
      </header>
      <div className="p-5">
        <pre className="overflow-x-auto rounded-xl border border-slate-200 bg-white p-4 text-xs leading-6 text-slate-700 whitespace-pre-wrap font-mono">{prompt.content}</pre>
        {prompt.variables?.length > 0 && (
          <div className="mt-4">
            <div className="text-xs font-bold uppercase tracking-wide text-slate-500">Variables</div>
            <div className="mt-2 flex flex-wrap gap-1.5">
              {prompt.variables.map((v, i) => (
                <code key={i} className="rounded-md border border-amber-200 bg-amber-50 px-2 py-0.5 text-xs font-mono text-amber-800">[{v}]</code>
              ))}
            </div>
          </div>
        )}
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {prompt.tools?.length > 0 && (
            <div className="rounded-xl border border-slate-200 bg-white p-3">
              <div className="text-xs font-bold uppercase tracking-wide text-slate-500">Outils</div>
              <div className="mt-1.5 flex flex-wrap gap-1">
                {prompt.tools.map((tool, i) => (
                  <span key={i} className="rounded-full border border-sky-200 bg-sky-50 px-2 py-0.5 text-xs font-semibold text-sky-700">{tool}</span>
                ))}
              </div>
            </div>
          )}
          {prompt.expected_output && (
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3">
              <div className="text-xs font-bold uppercase tracking-wide text-emerald-700">Résultat attendu</div>
              <div className="mt-1.5 text-xs text-emerald-900">{prompt.expected_output}</div>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}

function ComparisonTableCard({ table }) {
  if (!table?.headers || !table?.rows) return null;
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
      {table.title && (
        <header className="border-b border-slate-100 px-4 py-3 bg-slate-50">
          <h3 className="text-sm font-bold text-slate-700">{table.title}</h3>
        </header>
      )}
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50">
              {table.headers.map((h, i) => (
                <th key={i} className="px-4 py-3 text-left text-xs font-bold uppercase tracking-wide text-slate-600">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row, rIdx) => (
              <tr key={rIdx} className={`border-b border-slate-100 last:border-0 ${rIdx % 2 === 0 ? "bg-white" : "bg-slate-50/50"}`}>
                {row.map((cell, cIdx) => (
                  <td key={cIdx} className={`px-4 py-3 text-slate-700 ${cIdx === 0 ? "font-semibold text-euk-dark" : ""}`}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────
// ModulePage — composant principal
// ─────────────────────────────────────────────────────────────────────────
export default function ModulePage() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { language } = useOutletContext();

  const [moduleData, setModuleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copiedPromptId, setCopiedPromptId] = useState(null);
  const [missionSteps, setMissionSteps] = useState({});
  const [progressDone, setProgressDone] = useState(false);

  // ── Execution Task submission (nouvelle structure) ──────────────────────
  const [taskForm, setTaskForm] = useState({
    url: "",
    kpi_after: "",
    difficulty: "",
  });
  const [taskSubmitting, setTaskSubmitting] = useState(false);
  const [taskFeedback, setTaskFeedback] = useState(null);
  const [taskError, setTaskError] = useState("");
  const [nextRecommendation, setNextRecommendation] = useState(null);
  const [loadingRec, setLoadingRec] = useState(false);

  const USER_ID = (() => {
    try {
      const raw = localStorage.getItem("auth_user");
      if (!raw) return null;
      return JSON.parse(raw)?.id || null;
    } catch { return null; }
  })();

  const lang = language || "fr";

  const t = {
    fr: {
      loading: "Chargement du module...",
      back: "Retour apprentissage",
      notFound: "Module introuvable",
      notFoundDesc: "Ce module n'a pas pu être chargé.",
      min: "min", completed: "Terminé", inProgress: "En cours", notStarted: "Non commencé",
      yourProgress: "Votre progression",
      promptsLabel: "prompts", workflowsLabel: "workflows",
      scenarioTitle: "Scénario",
      scenarioSubtitle: "Un cas concret basé sur votre contexte métier.",
      useCaseTitle: "Le problème business",
      useCaseSubtitle: "Les défis réels que vous allez résoudre avec l'IA.",
      kpiTitle: "KPI — Avant / Après",
      kpiSubtitle: "L'impact business concret que vous allez générer.",
      programTitle: "Au programme",
      programSubtitle: "La promesse de ce module et ce que vous saurez livrer.",
      learningObjective: "Objectif d'apprentissage",
      expectedOutcome: "Résultat attendu",
      whyThisModule: "Pourquoi ce module",
      conceptsTitle: "Compétences clés",
      conceptsSubtitle: "Les notions essentielles que vous allez maîtriser.",
      executionContentLabel: "Contenu d'exécution",
      promptsTitle: "Prompts ChatGPT",
      promptsSubtitle: "Des prompts prêts à l'emploi pour accélérer votre travail.",
      toolsTitle: "Outils",
      toolsSubtitle: "Comparez les outils et leurs alternatives Maghreb.",
      workflowsTitle: "Workflows",
      workflowsSubtitle: "Choisissez le workflow adapté à votre niveau.",
      tutorialsTitle: "Tutoriels",
      tutorialsSubtitle: "Vidéos guidées pour démarrer rapidement.",
      tutorialWatch: "Voir le tutoriel",
      tutorialTemplate: "Template à dupliquer",
      missionLabel: "Mission terrain",
      missionTitle: "Execution Task",
      missionObjective: "Objectif",
      missionDuration: "Durée",
      missionTools: "Outils requis",
      missionStepsLabel: "Étapes",
      missionSuccess: "Critères de réussite",
      missionMaghreb: "Note régionale",
      stepsCompleted: "étapes complétées",
      kpiMeasurementTitle: "KPI Measurement",
      kpiMeasurementSubtitle: "Comment mesurer votre impact dans le temps.",
      kpiPatternTitle: "Pattern temporel des KPIs",
      milestonesTitle: "Jalons de mesure",
      progressTitle: "Progress Update",
      submitTitle: "Soumettre ma mission",
      submitSubtitle: "Partagez votre livrable réel et mesurez votre impact.",
      taskUrl: "Lien du livrable *",
      taskUrlPlaceholder: "https://figma.com/... ou Google Drive, Notion...",
      taskKpiAfter: "KPI après (mesuré) *",
      taskKpiAfterPlaceholder: "Ex: 10 concepts en 30 min (vs 3 avant)",
      taskDifficulty: "Difficulté ressentie",
      diffEasy: "Facile", diffMedium: "Moyenne", diffHard: "Élevée",
      submitBtn: "Soumettre ma mission →",
      submitting: "Envoi en cours...",
      submitted: "✓ Mission soumise",
      feedbackTitle: "Feedback du coach",
      nextStep: "Prochaine étape",
      progressSubtitle: "Bilan de votre module et prochaine étape recommandée.",
      progressModuleDone: "Module terminé",
      progressNextStep: "Prochaine étape",
      progressMarkDone: "Marquer comme terminé",
      progressDoneLabel: "✓ Module complété",
      maghrebSpecifics: "Spécificités Maghreb",
      masteryUpdated: "Mis à jour après soumission de la mission",
      masteryCompleted: "Mis à jour après complétion du module",
      recommendedModule: "Module recommandé",
      goToModule: "Aller au module →",
      resourcesTitle: "Ressources complémentaires",
      resourcesSubtitle: "Outils, articles et vidéos pour aller plus loin.",
      resourceTypeVideo: "Vidéo",
      resourceTypeArticle: "Article",
      resourceTypeTool: "Outil",
      resourceTypeTemplate: "Template",
      resourceOpen: "Accéder →",
    },
    en: {
      loading: "Loading module...",
      back: "Back to Learning",
      notFound: "Module not found",
      notFoundDesc: "This module could not be loaded.",
      min: "min", completed: "Completed", inProgress: "In progress", notStarted: "Not started",
      yourProgress: "Your progress",
      promptsLabel: "prompts", workflowsLabel: "workflows",
      scenarioTitle: "Scenario",
      scenarioSubtitle: "A concrete case based on your business context.",
      useCaseTitle: "The business problem",
      useCaseSubtitle: "The real challenges you will solve with AI.",
      kpiTitle: "KPI — Before / After",
      kpiSubtitle: "The concrete business impact you will generate.",
      programTitle: "What you'll learn",
      programSubtitle: "The promise of this module and what you'll be able to deliver.",
      learningObjective: "Learning objective",
      expectedOutcome: "Expected outcome",
      whyThisModule: "Why this module",
      conceptsTitle: "Key concepts",
      conceptsSubtitle: "The essential ideas you'll master.",
      executionContentLabel: "Execution Content",
      promptsTitle: "ChatGPT prompts",
      promptsSubtitle: "Ready-to-use prompts to accelerate your work.",
      toolsTitle: "Tools",
      toolsSubtitle: "Compare tools and their Maghreb alternatives.",
      workflowsTitle: "Workflows",
      workflowsSubtitle: "Choose the workflow that matches your level.",
      tutorialsTitle: "Tutorials",
      tutorialsSubtitle: "Guided videos to get started quickly.",
      tutorialWatch: "Watch tutorial",
      tutorialTemplate: "Duplicate template",
      missionLabel: "Field mission",
      missionTitle: "Execution Task",
      missionObjective: "Objective",
      missionDuration: "Duration",
      missionTools: "Tools required",
      missionStepsLabel: "Steps",
      missionSuccess: "Success criteria",
      missionMaghreb: "Regional note",
      stepsCompleted: "steps completed",
      kpiMeasurementTitle: "KPI Measurement",
      kpiMeasurementSubtitle: "How to measure your impact over time.",
      kpiPatternTitle: "KPI temporal pattern",
      milestonesTitle: "Measurement milestones",
      progressTitle: "Progress Update",
      submitTitle: "Submit my mission",
      submitSubtitle: "Share your real deliverable and measure your impact.",
      taskUrl: "Deliverable link *",
      taskUrlPlaceholder: "https://figma.com/... or Google Drive, Notion...",
      taskKpiAfter: "KPI after (measured) *",
      taskKpiAfterPlaceholder: "Ex: 10 concepts in 30 min (vs 3 before)",
      taskDifficulty: "Perceived difficulty",
      diffEasy: "Easy", diffMedium: "Medium", diffHard: "Hard",
      submitBtn: "Submit my mission →",
      submitting: "Submitting...",
      submitted: "✓ Mission submitted",
      feedbackTitle: "Coach feedback",
      nextStep: "Next step",
      progressSubtitle: "Module recap and recommended next step.",
      progressModuleDone: "Module completed",
      progressNextStep: "Next step",
      progressMarkDone: "Mark as completed",
      progressDoneLabel: "✓ Module completed",
      maghrebSpecifics: "Maghreb specifics",
      masteryUpdated: "Updated after mission submission",
      masteryCompleted: "Updated after module completion",
      recommendedModule: "Recommended module",
      goToModule: "Go to module →",
      resourcesTitle: "Additional resources",
      resourcesSubtitle: "Tools, articles and videos to go further.",
      resourceTypeVideo: "Video",
      resourceTypeArticle: "Article",
      resourceTypeTool: "Tool",
      resourceTypeTemplate: "Template",
      resourceOpen: "Open →",
    },
  };

  // ── Chargement du module ────────────────────────────────────────────────
  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const data = await getModule(moduleId);
        if (!data) return;
        setModuleData(data);
        if (data.module_status === "completed") setProgressDone(true);

        // Auto-start si module not_started
        if (data.module_status === "not_started") {
          try {
            await startModule(moduleId);
          } catch { /* non-bloquant */ }
        }
      } catch {
        setError(t[lang].notFoundDesc);
      } finally {
        setLoading(false);
      }
    })();
  }, [moduleId, lang]); // eslint-disable-line react-hooks/exhaustive-deps

  const pick = (frValue, enValue) => lang === "fr" ? frValue || enValue : enValue || frValue;

  const statusBadgeClass = (status) => {
    if (status === "completed") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (status === "in_progress") return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-slate-200 bg-slate-50 text-slate-600";
  };

  const statusLabel = (status) => {
    if (status === "completed") return t[lang].completed;
    if (status === "in_progress") return t[lang].inProgress;
    return t[lang].notStarted;
  };

  const copyPrompt = async (id, content) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedPromptId(id);
      setTimeout(() => setCopiedPromptId(null), 2000);
    } catch { /* non-blocking */ }
  };

  const fetchRecommendation = async () => {
    if (loadingRec || nextRecommendation) return;
    setLoadingRec(true);
    try {
      const data = await getFullRecommendation(moduleId);
      if (data) setNextRecommendation(data);
    } catch { /* non-blocking */ }
    finally { setLoadingRec(false); }
  };

  // ── Soumettre l'Execution Task ──────────────────────────────────────────
  const submitTask = async () => {
    if (!taskForm.url || !taskForm.kpi_after) {
      setTaskError(lang === "fr"
        ? "Veuillez remplir le lien du livrable et le KPI après."
        : "Please fill in the deliverable link and KPI after.");
      return;
    }
    setTaskSubmitting(true);
    setTaskError("");
    try {
      // 1. Soumettre l'Execution Task → met à jour mastery
      await submitExecutionTask(moduleId, {
        url: taskForm.url,
        kpiAfter: taskForm.kpi_after,
        difficulty: taskForm.difficulty || null,
      });

      // 2. Récupérer le feedback du coach
      const kpiBefore = pick(moduleData?.kpi_before_fr, moduleData?.kpi_before_en);
      const feedback = await getExecutionTaskFeedback({
        moduleId: parseInt(moduleId, 10),
        moduleTitle: pick(moduleData?.title_fr, moduleData?.title_en),
        kpiBefore,
        kpiAfter: taskForm.kpi_after,
        difficulty: taskForm.difficulty || null,
        sectionType: "execution_task",
      });
      setTaskFeedback(feedback);

      // 3. Recharger le module pour mettre à jour la mastery
      const fresh = await getModule(moduleId);
      if (fresh) setModuleData(fresh);

      // 4. Déclencher la recommandation
      fetchRecommendation();
    } catch {
      setTaskError(lang === "fr" ? "Erreur lors de la soumission." : "Submission failed.");
    } finally {
      setTaskSubmitting(false);
    }
  };

  const handleMarkComplete = async () => {
    try {
      setProgressDone(true);
      await completeModule(moduleId);
      const fresh = await getModule(moduleId);
      if (fresh) setModuleData(fresh);
      fetchRecommendation();
    } catch { /* non-blocking */ }
  };

  const progressPercent = moduleData?.progress_percent || 0;
  const moduleStatus = moduleData?.module_status || "not_started";
  const kpiBaseline = pick(moduleData?.kpi_before_fr, moduleData?.kpi_before_en);

  // ── Données JSON du module ──
  const promptExamples    = pick(moduleData?.prompt_examples_fr, moduleData?.prompt_examples_en) || [];
  const comparisonTables  = pick(moduleData?.comparison_tables_fr, moduleData?.comparison_tables_en) || {};
  const sectionContent    = pick(moduleData?.section_content_fr, moduleData?.section_content_en) || {};
  const useCaseDetail     = sectionContent?.use_case_detail || null;
  const kpiPattern        = sectionContent?.kpi_pattern || null;
  const kpiMeasurement    = sectionContent?.kpi_measurement_method || null;
  const kpiTargets        = comparisonTables?.kpi_targets || null;
  const toolsTable        = comparisonTables?.tools || null;
  const workflowsTable    = comparisonTables?.workflows || null;
  const tutorials = moduleData?.tutorials_fr?.length > 0
  ? moduleData.tutorials_fr
  : [];
  const resources = moduleData?.references_fr || [];
  const practicalExercise = pick(moduleData?.practical_exercise_fr, moduleData?.practical_exercise_en);
  const progressUpdate    = moduleData?.progress_update_fr || null;
  const roleBasedExample  = pick(moduleData?.role_based_example_fr, moduleData?.role_based_example_en);

  const hasProgramContent = !!(
    moduleData?.learning_objective_fr || moduleData?.learning_objective_en ||
    moduleData?.expected_outcome_fr   || moduleData?.expected_outcome_en   ||
    moduleData?.why_this_module_fr    || moduleData?.why_this_module_en
  );

  const keyConceptsList = (() => {
    const raw = pick(moduleData?.key_concepts_fr, moduleData?.key_concepts_en);
    if (!raw) return [];
    if (Array.isArray(raw)) return raw.filter(Boolean);
    if (typeof raw === "string") return raw.split(/[,\n;]+/).map(s => s.trim()).filter(Boolean);
    return [];
  })();

  const hasExecutionContent = promptExamples.length > 0 || toolsTable || workflowsTable || tutorials.length > 0;

  if (loading) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-4xl p-6">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
            <span className="text-sm text-slate-500">{t[lang].loading}</span>
          </div>
        </div>
      </div>
    </div>
  );

  if (!moduleData || error) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-4xl p-6">
        <button onClick={() => navigate("/learning")}
          className="mb-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50">
          ← {t[lang].back}
        </button>
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h1 className="text-xl font-bold text-euk-dark">{t[lang].notFound}</h1>
          <p className="mt-2 text-sm text-slate-500">{error || t[lang].notFoundDesc}</p>
        </div>
      </div>
    </div>
  );

  const title       = pick(moduleData.title_fr, moduleData.title_en);
  const description = pick(moduleData.description_fr, moduleData.description_en);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-4xl p-6">

        <button onClick={() => navigate("/learning")}
          className="mb-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50">
          ← {t[lang].back}
        </button>

        {/* ══ 1. HEADER ══ */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
          <div className="flex flex-wrap items-center gap-2">
            {moduleData.journey_stage && (
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{moduleData.journey_stage}</span>
            )}
            {moduleData.role && (
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{moduleData.role}</span>
            )}
            <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${statusBadgeClass(moduleStatus)}`}>{statusLabel(moduleStatus)}</span>
          </div>
          <h1 className="mt-4 text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{title}</h1>
          {description && <p className="mt-3 text-sm leading-6 text-slate-600 md:text-base md:leading-7">{description}</p>}
          <div className="mt-6 grid grid-cols-3 gap-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">{promptExamples.length || 0}</div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].promptsLabel}</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">
                {(comparisonTables?.workflows?.rows?.length) || 0}
              </div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].workflowsLabel}</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">{moduleData.estimated_duration_min || 0}</div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].min}</div>
            </div>
          </div>
          

          {/* ── Votre progression — deux indicateurs clairs ── */}
<div className="mt-5 rounded-2xl border border-slate-100 bg-slate-50 p-4 space-y-4">
  <div className="text-xs font-bold uppercase tracking-wide text-slate-400">
    {lang === "fr" ? "Votre progression" : "Your progress"}
  </div>

  {/* Ligne 1 — Contenu parcouru */}
  <div>
    <div className="flex items-center justify-between text-sm mb-1.5">
      <div>
        <span className="font-semibold text-euk-dark">
          📚 {lang === "fr" ? "Contenu parcouru" : "Content progress"}
        </span>
        <span className="block text-xs text-slate-400 mt-0.5">
          {lang === "fr"
            ? "Sections du module complétées"
            : "Module sections completed"}
        </span>
      </div>
      <span className={`font-bold text-sm ${progressPercent === 100 ? "text-emerald-600" : "text-euk-primary"}`}>
        {progressPercent === 100
          ? (lang === "fr" ? "✓ Terminé" : "✓ Done")
          : `${progressPercent}%`}
      </span>
    </div>
    <div className="h-2 w-full rounded-full bg-slate-200">
      <div
        className={`h-2 rounded-full transition-all duration-500 ${progressPercent === 100 ? "bg-emerald-500" : "bg-euk-primary"}`}
        style={{ width: `${progressPercent}%` }}
      />
    </div>
  </div>

  {/* Ligne 2 — Mastery du skill */}
  {moduleData?.skill_mastery && (
    <div>
      <div className="flex items-center justify-between text-sm mb-1.5">
        <div>
          <span className="font-semibold text-euk-dark">
            🎯 {moduleData.skill_mastery.skill_name}
          </span>
          <span className="block text-xs text-slate-400 mt-0.5">
            {lang === "fr"
              ? "Compétence acquise sur vos données réelles"
              : "Skill acquired on your real data"}
          </span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="font-bold text-sm text-euk-primary">
            {Math.round((moduleData.skill_mastery.mastery_score || 0) * 100)}%
          </span>
          <span className="rounded-full border border-euk-primary/20 bg-white px-2 py-0.5 text-xs font-semibold text-euk-dark capitalize">
            {moduleData.skill_mastery.mastery_level || "novice"}
          </span>
        </div>
      </div>
      <div className="h-2 w-full rounded-full bg-slate-200">
        <div
          className="h-2 rounded-full bg-euk-primary transition-all duration-500"
          style={{ width: `${Math.round((moduleData.skill_mastery.mastery_score || 0) * 100)}%` }}
        />
      </div>
      {moduleData.skill_mastery.last_update_reason && (
        <div className="mt-1.5 flex items-center gap-1.5 text-xs text-slate-400">
          <span>↳</span>
          <span>{
            moduleData.skill_mastery.last_update_reason.includes("execution_task")
              ? t[lang].masteryUpdated
              : moduleData.skill_mastery.last_update_reason.includes("completed")
              ? t[lang].masteryCompleted
              : moduleData.skill_mastery.last_update_reason
          }</span>
        </div>
      )}
    </div>
  )}
</div>
        </section>

        {/* ══ 2. SCÉNARIO ══ */}
        {roleBasedExample && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].scenarioTitle} subtitle={t[lang].scenarioSubtitle} />
            <div className="flex items-start gap-4 rounded-2xl border border-sky-200 bg-sky-50 p-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-100 text-xl">👤</div>
              <p className="text-sm leading-7 text-slate-700">{roleBasedExample}</p>
            </div>
          </section>
        )}

        {/* ══ 3. USE CASE ══ */}
        {useCaseDetail && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].useCaseTitle} subtitle={t[lang].useCaseSubtitle} />
            {useCaseDetail.narrative && (
              <p className="text-sm leading-6 text-slate-700 mb-4">{useCaseDetail.narrative}</p>
            )}
            {useCaseDetail.pain_points?.length > 0 && (
              <div className="space-y-2">
                {useCaseDetail.pain_points.map((point, i) => (
                  <div key={i} className="flex items-start gap-3 rounded-xl border border-red-100 bg-red-50 px-4 py-2.5">
                    <span className="mt-0.5 text-red-400 shrink-0">✕</span>
                    <span className="text-sm text-red-900">{point}</span>
                  </div>
                ))}
              </div>
            )}
            {useCaseDetail.maghreb_specifics?.length > 0 && (
              <div className="mt-4 rounded-2xl border border-rose-200 bg-rose-50 p-4">
                <div className="text-xs font-bold uppercase tracking-wide text-rose-700 mb-2">🌍 {t[lang].maghrebSpecifics}</div>
                <ul className="space-y-1">
                  {useCaseDetail.maghreb_specifics.map((s, i) => (
                    <li key={i} className="text-sm text-rose-900 flex items-start gap-2"><span className="shrink-0">•</span>{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}

        {/* ══ 4. KPI BEFORE/AFTER ══ */}
        {kpiTargets && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].kpiTitle} subtitle={t[lang].kpiSubtitle} />
            <ComparisonTableCard table={kpiTargets} />
          </section>
        )}

        {/* ══ 5. AU PROGRAMME ══ */}
        {hasProgramContent && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].programTitle} subtitle={t[lang].programSubtitle} />
            <div className="space-y-4">
              {pick(moduleData.learning_objective_fr, moduleData.learning_objective_en) && (
                <ProgramItem icon="🎯" label={t[lang].learningObjective}
                  content={pick(moduleData.learning_objective_fr, moduleData.learning_objective_en)}
                  accent="border-emerald-200 bg-emerald-50" iconBg="bg-emerald-100" labelColor="text-emerald-700" />
              )}
              {pick(moduleData.expected_outcome_fr, moduleData.expected_outcome_en) && (
                <ProgramItem icon="✨" label={t[lang].expectedOutcome}
                  content={pick(moduleData.expected_outcome_fr, moduleData.expected_outcome_en)}
                  accent="border-sky-200 bg-sky-50" iconBg="bg-sky-100" labelColor="text-sky-700" />
              )}
              {pick(moduleData.why_this_module_fr, moduleData.why_this_module_en) && (
                <ProgramItem icon="💡" label={t[lang].whyThisModule}
                  content={pick(moduleData.why_this_module_fr, moduleData.why_this_module_en)}
                  accent="border-violet-200 bg-violet-50" iconBg="bg-violet-100" labelColor="text-violet-700" />
              )}
            </div>
          </section>
        )}

        {/* ══ 6. COMPÉTENCES CLÉS ══ */}
        {keyConceptsList.length > 0 && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].conceptsTitle} subtitle={t[lang].conceptsSubtitle} />
            <div className="flex flex-wrap gap-2">
              {keyConceptsList.map((concept, idx) => (
                <span key={idx} className="inline-flex items-center gap-1.5 rounded-full border border-euk-primary/20 bg-euk-primary/5 px-3 py-1.5 text-sm font-medium text-euk-dark">
                  <svg className="h-3.5 w-3.5 text-euk-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  {concept}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* ══ SÉPARATEUR EXECUTION CONTENT ══ */}
        {hasExecutionContent && (
          <div className="mt-8 mb-2 flex items-center gap-3">
            <div className="h-px flex-1 bg-slate-200" />
            <span className="rounded-full border border-slate-200 bg-slate-50 px-4 py-1 text-xs font-bold uppercase tracking-widest text-slate-500">
              {t[lang].executionContentLabel}
            </span>
            <div className="h-px flex-1 bg-slate-200" />
          </div>
        )}

        {/* ══ 7. PROMPTS ══ */}
        {promptExamples.length > 0 && (
          <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].promptsTitle} subtitle={t[lang].promptsSubtitle} />
            <div className="space-y-5">
              {promptExamples.map((prompt) => (
                <PromptCard key={prompt.id} prompt={prompt}
                  isCopied={copiedPromptId === prompt.id}
                  onCopy={() => copyPrompt(prompt.id, prompt.content)} />
              ))}
            </div>
          </section>
        )}

        {/* ══ 8. WORKFLOWS ══ */}
        {workflowsTable && (
          <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].workflowsTitle} subtitle={t[lang].workflowsSubtitle} />
            <ComparisonTableCard table={workflowsTable} />
          </section>
        )}

        {/* ══ 9. TOOLS ══ */}
        {toolsTable && (
          <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].toolsTitle} subtitle={t[lang].toolsSubtitle} />
            <ComparisonTableCard table={toolsTable} />
          </section>
        )}

        {/* ══ 10. TUTORIALS ══ */}
{tutorials.length > 0 && (
  <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
    <SectionHeader title={t[lang].tutorialsTitle} subtitle={t[lang].tutorialsSubtitle} />
    <div className="space-y-4">
      {tutorials.map((tuto, idx) => (
        <div key={idx} className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div className="flex items-start gap-4 border-b border-slate-100 bg-slate-50/50 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-euk-primary/10 text-lg">
              📋
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-euk-dark text-sm">{tuto.title}</div>
              <div className="mt-1 flex flex-wrap items-center gap-2">
                {tuto.duration_min && (
                  <span className="text-xs text-slate-500">⏱ {tuto.duration_min} min</span>
                )}
                {tuto.tool && (
                  <span className="rounded-full border border-sky-200 bg-sky-50 px-2 py-0.5 text-xs font-semibold text-sky-700">
                    {tuto.tool}
                  </span>
                )}
                {tuto.format && (
                  <span className="rounded-full border border-slate-200 bg-white px-2 py-0.5 text-xs font-medium text-slate-600">
                    {tuto.format}
                  </span>
                )}
              </div>
            </div>
          </div>
          {tuto.steps?.length > 0 && (
            <div className="p-4">
              <div className="text-xs font-bold uppercase tracking-wide text-slate-400 mb-3">
                {lang === "fr" ? "Étapes" : "Steps"}
              </div>
              <div className="space-y-2">
                {tuto.steps.map((step, sIdx) => (
                  <div key={sIdx} className="flex items-start gap-3">
                    <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-euk-primary/10 text-xs font-bold text-euk-primary">
                      {sIdx + 1}
                    </div>
                    <p className="text-sm text-slate-700 leading-6">{step}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          {(tuto.url || tuto.template_url) && (
            <div className="border-t border-slate-100 p-4 flex flex-wrap gap-2">
              {tuto.url && (
                <a href={tuto.url} target="_blank" rel="noreferrer"
                  className="rounded-xl bg-euk-primary px-3 py-1.5 text-xs font-bold text-white hover:bg-euk-deep transition">
                  ▶ {t[lang].tutorialWatch}
                </a>
              )}
              {tuto.template_url && (
                <a href={tuto.template_url} target="_blank" rel="noreferrer"
                  className="rounded-xl border border-euk-primary/30 bg-euk-primary/5 px-3 py-1.5 text-xs font-bold text-euk-primary hover:bg-euk-primary/10 transition">
                  📋 {t[lang].tutorialTemplate}
                </a>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  </section>
)}
        {/* ══ 10b. RESOURCES ══ */}
{resources.length > 0 && (
  <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
    <SectionHeader title={t[lang].resourcesTitle} subtitle={t[lang].resourcesSubtitle} />
    <div className="grid gap-3 md:grid-cols-2">
      {resources.map((resource, idx) => {
        const typeColors = {
          video:    "border-violet-200 bg-violet-50 text-violet-700",
          article:  "border-sky-200 bg-sky-50 text-sky-700",
          tool:     "border-emerald-200 bg-emerald-50 text-emerald-700",
          template: "border-amber-200 bg-amber-50 text-amber-700",
        };
        const typeIcons = {
          video: "▶", article: "📄", tool: "🔧", template: "📋",
        };
        const typeLabels = {
          video:    t[lang].resourceTypeVideo,
          article:  t[lang].resourceTypeArticle,
          tool:     t[lang].resourceTypeTool,
          template: t[lang].resourceTypeTemplate,
        };
        const colorClass = typeColors[resource.type] || "border-slate-200 bg-slate-50 text-slate-700";
        return (
          <a key={idx} href={resource.url} target="_blank" rel="noreferrer"
            className="group flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-4 transition hover:border-euk-primary/30 hover:shadow-sm">
            <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${colorClass}`}>
              {typeIcons[resource.type] || "🔗"}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="text-sm font-semibold text-euk-dark group-hover:text-euk-primary transition line-clamp-2">
                  {resource.title}
                </div>
                <span className="shrink-0 text-xs font-bold text-euk-primary opacity-0 group-hover:opacity-100 transition">
                  {t[lang].resourceOpen}
                </span>
              </div>
              {resource.description && (
                <p className="mt-1 text-xs leading-5 text-slate-500 line-clamp-2">{resource.description}</p>
              )}
              <div className="mt-2 flex flex-wrap items-center gap-1.5">
                <span className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${colorClass}`}>
                  {typeLabels[resource.type] || resource.type}
                </span>
                {resource.duration && (
                  <span className="text-xs text-slate-400">⏱ {resource.duration}</span>
                )}
                {resource.tags?.slice(0, 2).map((tag, i) => (
                  <span key={i} className="rounded-full border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs text-slate-500">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </a>
        );
      })}
    </div>
  </section>
)}
        {/* ══ SÉPARATEUR EXECUTION TASK ══ */}
        {practicalExercise && (
          <div className="mt-8 mb-2 flex items-center gap-3">
            <div className="h-px flex-1 bg-slate-200" />
            <span className="rounded-full border border-amber-200 bg-amber-50 px-4 py-1 text-xs font-bold uppercase tracking-widest text-amber-700">
              {t[lang].missionLabel}
            </span>
            <div className="h-px flex-1 bg-slate-200" />
          </div>
        )}

        {/* ══ 11. EXECUTION TASK ══ */}
        {practicalExercise && (
          <section className="mt-4 rounded-3xl border-2 border-amber-200 bg-gradient-to-br from-amber-50/50 to-white p-6 shadow-md md:p-8">
            <div className="mb-1 inline-flex items-center gap-2 rounded-full border border-amber-300 bg-amber-100 px-3 py-1 text-xs font-bold uppercase tracking-wide text-amber-800">
              ✅ {t[lang].missionTitle}
            </div>
            <h2 className="mt-3 text-xl font-bold text-euk-dark md:text-2xl">{practicalExercise.title}</h2>
            {practicalExercise.objective && (
              <div className="mt-4 rounded-2xl border border-amber-200 bg-white p-4">
                <div className="text-xs font-bold uppercase tracking-wide text-amber-700">{t[lang].missionObjective}</div>
                <p className="mt-1.5 text-sm leading-6 text-slate-700">{practicalExercise.objective}</p>
              </div>
            )}
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {practicalExercise.duration_minutes && (
                <div className="rounded-2xl border border-slate-200 bg-white p-4">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-500">{t[lang].missionDuration}</div>
                  <div className="mt-1 text-base font-bold text-euk-dark">{practicalExercise.duration_minutes} {t[lang].min}</div>
                </div>
              )}
              {practicalExercise.tools_required?.length > 0 && (
                <div className="rounded-2xl border border-slate-200 bg-white p-4">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-500">{t[lang].missionTools}</div>
                  <div className="mt-1.5 flex flex-wrap gap-1.5">
                    {practicalExercise.tools_required.map((tool, i) => (
                      <span key={i} className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs font-semibold text-slate-700">{tool}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Étapes cochables (visuel local) */}
            {practicalExercise.steps?.length > 0 && (
              <div className="mt-5">
                <div className="mb-3 flex items-center justify-between">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-500">{t[lang].missionStepsLabel}</div>
                  <div className="text-xs font-semibold text-amber-700">
                    {Object.values(missionSteps).filter(Boolean).length}/{practicalExercise.steps.length} {t[lang].stepsCompleted}
                  </div>
                </div>
                <div className="space-y-2">
                  {practicalExercise.steps.map((step, idx) => {
                    const isDone = !!missionSteps[idx];
                    return (
                      <div key={idx} onClick={() => setMissionSteps(p => ({ ...p, [idx]: !p[idx] }))}
                        className={`flex cursor-pointer gap-4 rounded-2xl border p-4 transition ${isDone ? "border-emerald-200 bg-emerald-50" : "border-slate-200 bg-white hover:border-amber-300 hover:bg-amber-50/30"}`}>
                        <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${isDone ? "bg-emerald-500 text-white" : "bg-amber-100 text-amber-700"}`}>
                          {isDone ? "✓" : step.n}
                        </div>
                        <div className="flex-1 min-w-0">
                          {step.title && <div className={`text-sm font-semibold ${isDone ? "text-emerald-800 line-through" : "text-euk-dark"}`}>{step.title}</div>}
                          {step.description && <div className={`mt-1 text-sm leading-6 ${isDone ? "text-emerald-700" : "text-slate-600"}`}>{step.description}</div>}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {practicalExercise.success_criteria?.length > 0 && (
              <div className="mt-5 rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                <div className="text-xs font-bold uppercase tracking-wide text-emerald-700">{t[lang].missionSuccess}</div>
                <ul className="mt-2 space-y-1.5">
                  {practicalExercise.success_criteria.map((c, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-emerald-900">
                      <svg className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                      {c}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {practicalExercise.maghreb_note && (
              <div className="mt-4 rounded-2xl border border-rose-200 bg-rose-50 p-4">
                <div className="text-xs font-bold uppercase tracking-wide text-rose-700">🌍 {t[lang].missionMaghreb}</div>
                <p className="mt-1.5 text-sm leading-6 text-rose-900">{practicalExercise.maghreb_note}</p>
              </div>
            )}

            {/* ── Formulaire soumission Execution Task ── */}
            <div className="mt-8 border-t border-slate-200 pt-6">
              <h3 className="text-base font-bold text-euk-dark mb-1">🚀 {t[lang].submitTitle}</h3>
              <p className="text-sm text-slate-500 mb-5">{t[lang].submitSubtitle}</p>

              {taskFeedback ? (
                <div className="space-y-4">
                  <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-sm font-bold text-emerald-700">✓ {t[lang].submitted}</span>
                      {taskFeedback.progression_signal && (
                        <span className="rounded-full border border-emerald-300 bg-white px-3 py-1 text-xs font-bold text-emerald-700 capitalize">
                          {taskFeedback.progression_signal}
                        </span>
                      )}
                    </div>
                    <div className="text-xs font-bold uppercase tracking-wide text-emerald-700 mb-1">{t[lang].feedbackTitle}</div>
                    <p className="text-sm leading-6 text-slate-700">{taskFeedback.feedback}</p>
                  </div>

                  {taskFeedback.suggestion && (
                    <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                      <p className="text-sm text-amber-900">💡 {taskFeedback.suggestion}</p>
                    </div>
                  )}

                  {taskFeedback.next_step && (
                    <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4">
                      <span className="text-xs font-bold text-sky-700 uppercase tracking-wide">{t[lang].nextStep}</span>
                      <p className="mt-1 text-sm text-slate-700">{taskFeedback.next_step}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Lien du livrable */}
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">{t[lang].taskUrl}</label>
                    <input
                      type="url"
                      value={taskForm.url}
                      onChange={e => setTaskForm(f => ({ ...f, url: e.target.value }))}
                      placeholder={t[lang].taskUrlPlaceholder}
                      className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-euk-primary focus:outline-none focus:ring-1 focus:ring-euk-primary"
                    />
                  </div>

                  {/* KPI après */}
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">{t[lang].taskKpiAfter}</label>
                    <input
                      type="text"
                      value={taskForm.kpi_after}
                      onChange={e => setTaskForm(f => ({ ...f, kpi_after: e.target.value }))}
                      placeholder={t[lang].taskKpiAfterPlaceholder}
                      className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-euk-primary focus:outline-none focus:ring-1 focus:ring-euk-primary"
                    />
                  </div>

                  {/* Difficulté */}
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-1.5">{t[lang].taskDifficulty}</label>
                    <div className="flex gap-2">
                      {[
                        { key: "facile", label: t[lang].diffEasy },
                        { key: "moyenne", label: t[lang].diffMedium },
                        { key: "élevée", label: t[lang].diffHard },
                      ].map(opt => (
                        <button
                          key={opt.key}
                          type="button"
                          onClick={() => setTaskForm(f => ({ ...f, difficulty: opt.key }))}
                          className={`flex-1 rounded-2xl border px-4 py-2.5 text-sm font-semibold transition ${
                            taskForm.difficulty === opt.key
                              ? "border-euk-primary bg-euk-primary/10 text-euk-primary"
                              : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
                          }`}
                        >
                          {opt.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {taskError && <p className="text-sm text-red-600 font-medium">{taskError}</p>}

                  <button
                    onClick={submitTask}
                    disabled={taskSubmitting || !taskForm.url || !taskForm.kpi_after}
                    className="w-full rounded-2xl bg-euk-primary px-6 py-3.5 text-sm font-bold text-white transition hover:bg-euk-deep disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {taskSubmitting ? t[lang].submitting : t[lang].submitBtn}
                  </button>
                </div>
              )}
            </div>
          </section>
        )}

        {/* ══ 12. KPI MEASUREMENT ══ */}
        {(kpiMeasurement || kpiPattern) && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm md:p-8">
            <SectionHeader title={t[lang].kpiMeasurementTitle} subtitle={t[lang].kpiMeasurementSubtitle} />
            {kpiPattern && kpiPattern.levels?.length > 0 && (
              <div className="mb-6">
                <div className="text-xs font-bold uppercase tracking-wide text-slate-500 mb-3">{t[lang].kpiPatternTitle}</div>
                <div className="grid gap-3 md:grid-cols-3">
                  {kpiPattern.levels.map((lvl, i) => {
                    const colors = [
                      "border-emerald-200 bg-emerald-50 text-emerald-700",
                      "border-sky-200 bg-sky-50 text-sky-700",
                      "border-violet-200 bg-violet-50 text-violet-700",
                    ];
                    return (
                      <div key={i} className={`rounded-2xl border p-4 ${colors[i % 3]}`}>
                        <div className="text-xs font-bold uppercase tracking-wide mb-1">{lvl.level}</div>
                        <div className="text-xs font-semibold mb-1">{lvl.horizon}</div>
                        <div className="text-xs opacity-80">{lvl.type}</div>
                        {lvl.examples && <div className="mt-2 text-xs italic opacity-70">{lvl.examples}</div>}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
            {kpiMeasurement && kpiMeasurement.milestones?.length > 0 && (
              <div>
                <div className="text-xs font-bold uppercase tracking-wide text-slate-500 mb-3">{t[lang].milestonesTitle}</div>
                <div className="space-y-2">
                  {kpiMeasurement.milestones.map((m, i) => (
                    <div key={i} className="flex items-start gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-3">
                      <div className="flex h-10 w-16 shrink-0 items-center justify-center rounded-xl bg-euk-primary text-xs font-bold text-white">
                        {m.when}
                      </div>
                      <p className="text-sm text-slate-700 leading-6">{m.what}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* ══ 13. PROGRESS UPDATE ══ */}
        <section className="mt-6 mb-6 rounded-3xl border border-euk-primary/20 bg-gradient-to-br from-euk-primary/5 to-white p-6 shadow-sm md:p-8">
          <SectionHeader title={t[lang].progressTitle} subtitle={t[lang].progressSubtitle} />
          <div className="grid gap-3 md:grid-cols-3">
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-center">
              <div className="text-2xl font-bold text-emerald-700">{progressPercent}%</div>
              <div className="mt-1 text-xs font-semibold text-emerald-600">{t[lang].progressModuleDone}</div>
            </div>
            <div className="rounded-2xl border border-sky-200 bg-sky-50 p-4 text-center">
              <div className="text-2xl">🏆</div>
              <div className="mt-1 text-xs font-semibold text-sky-700">{progressUpdate?.skill_label || (moduleData?.skill_mastery?.skill_name) || "Skill"}</div>
            </div>
            <div className="rounded-2xl border border-violet-200 bg-violet-50 p-4 text-center">
              <div className="text-2xl">→</div>
              <div className="mt-1 text-xs font-semibold text-violet-700">{progressUpdate?.next_step || t[lang].progressNextStep}</div>
            </div>
          </div>
          <div className="mt-5 flex flex-col items-center gap-3">
            <button
              onClick={handleMarkComplete}
              disabled={progressDone}
              className={`rounded-2xl px-6 py-3 text-sm font-bold transition ${progressDone ? "bg-emerald-500 text-white cursor-default" : "bg-euk-primary text-white hover:bg-euk-deep"}`}>
              {progressDone ? t[lang].progressDoneLabel : t[lang].progressMarkDone}
            </button>
            {loadingRec && (
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <div className="h-3 w-3 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
                {lang === "fr" ? "Analyse de votre parcours..." : "Analyzing your path..."}
              </div>
            )}

            {/* STAGNATION ALERT */}
            {nextRecommendation?.stagnation?.is_stagnating && (
              <div className="w-full rounded-2xl border border-amber-300 bg-amber-50 p-4 text-left">
                <div className="text-xs font-bold uppercase tracking-wide text-amber-700 mb-1">
                  ⚠️ {lang === "fr" ? "Signal de stagnation" : "Stagnation detected"}
                </div>
                <p className="text-xs text-amber-800 leading-5">
                  {nextRecommendation.stagnation.reset_message}
                </p>
                <div className="mt-2 flex flex-wrap gap-1">
                  {nextRecommendation.stagnation.signals.map((s, i) => (
                    <span key={i} className="rounded-full bg-amber-100 px-2 py-0.5 text-xs text-amber-700">
                      {s.message}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* SECTION A REVOIR */}
            {nextRecommendation?.section_review?.section && (
              <div className="w-full rounded-2xl border border-sky-200 bg-sky-50 p-4 text-left">
                <div className="text-xs font-bold uppercase tracking-wide text-sky-700 mb-1">
                  📌 {lang === "fr" ? "Section a revoir" : "Section to review"}
                </div>
                <div className="text-sm font-semibold text-sky-900">
                  {nextRecommendation.section_review.section_label}
                </div>
                <p className="mt-1 text-xs text-sky-800 leading-5">
                  {nextRecommendation.section_review.reason}
                </p>
                {nextRecommendation.section_review.expected_result && (
                  <p className="mt-1 text-xs text-sky-600 italic">
                    {lang === "fr" ? "Resultat attendu : " : "Expected: "}
                    {nextRecommendation.section_review.expected_result}
                  </p>
                )}
              </div>
            )}

            {/* MODULE SUIVANT */}
            {nextRecommendation?.next_module?.module_title && (
              <div className="w-full rounded-2xl border border-euk-primary/20 bg-euk-primary/5 p-4 text-left">
                <div className="text-xs font-bold uppercase tracking-wide text-euk-primary mb-1">
                  💡 {t[lang].recommendedModule}
                </div>
                <div className="text-sm font-semibold text-euk-dark">
                  {nextRecommendation.next_module.module_title}
                </div>
                {nextRecommendation.next_module.reason && (
                  <p className="mt-1 text-xs text-slate-600">{nextRecommendation.next_module.reason}</p>
                )}
                <div className="mt-2 flex items-center gap-2">
                  <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${nextRecommendation.next_module.source === "llm" ? "bg-violet-100 text-violet-700" : "bg-slate-100 text-slate-600"}`}>
                    {nextRecommendation.next_module.source === "llm" ? "🤖 IA" : "📋 Regle"}
                  </span>
                  {nextRecommendation.next_module.module_id && nextRecommendation.next_module.module_id !== parseInt(moduleId) && (
                    <button onClick={() => navigate(`/learning/module/${nextRecommendation.next_module.module_id}/units`)}
                      className="rounded-xl bg-euk-primary px-3 py-1 text-xs font-bold text-white hover:bg-euk-deep transition">
                      {t[lang].goToModule}
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* PLAN MICRO-SESSIONS */}
            {nextRecommendation?.session_plan && (
              <div className="w-full rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-left">
                <div className="text-xs font-bold uppercase tracking-wide text-emerald-700 mb-1">
                  🗓️ {lang === "fr" ? "Plan de la semaine" : "Weekly plan"}
                </div>
                <p className="text-xs text-emerald-800 leading-5">
                  {nextRecommendation.session_plan.plan_description}
                </p>
                {nextRecommendation.session_plan.cta === "update_profile" && (
                  <button onClick={() => navigate("/account")}
                    className="mt-2 rounded-xl bg-emerald-600 px-3 py-1 text-xs font-bold text-white hover:bg-emerald-700 transition">
                    {lang === "fr" ? "Renseigner mon profil" : "Update my profile"}
                  </button>
                )}
              </div>
            )}
          </div>
        </section>

      </div>

      <TutorChat
        moduleId={parseInt(moduleId, 10)}
        userId={USER_ID}
        kpiBaseline={kpiBaseline}
        lang={lang}
      />
    </div>
  );
}
