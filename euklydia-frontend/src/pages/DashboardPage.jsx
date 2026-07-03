import { useEffect, useMemo, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";
import ConfirmModal from "../components/ConfirmModal";
import { ROLE_DETAILS } from "../data/roles";
import RetakeDiagnosticBtn from "../components/RetakeDiagnosticBtn";

export default function DashboardPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext();
  const lang = language || "en";

  const [skills, setSkills] = useState([]);
  const [summary, setSummary] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);

  // ── Performance Agent state ──
  const [perfData, setPerfData] = useState(null);
  const [perfLoading, setPerfLoading] = useState(false);
  const [diagStatus, setDiagStatus] = useState(null);

  const t = {
    en: {
      heroBadge: "AI capability dashboard",
      title: "Dashboard",
      subtitle: "Track your progress on your 3 business use cases and activate the AI Blueprints that will take you to the next level.",
      viewRoadmap: "View my AI Roadmap",
      redodiagnostic: "Retake diagnostic",
      confirmTitle: "Retake diagnostic?",
      confirmMessage: "Your current scores will be replaced by the new results. This action cannot be undone.",
      confirmLabel: "Yes, retake",
      cancelLabel: "Cancel",
      globalScore: "Global AI Score",
      globalScoreText: "Estimated average score across all evaluated skills.",
      highPriorityGaps: "High Priority Gaps",
      highPrioritySkills: "High priority skills",
      highPriorityText: "Skills to strengthen first in order to accelerate your progress.",
      noGapsTitle: "No priority gaps",
      noGapsText: "Great work! Keep advancing your skills with the recommended modules.",
      nextFocus: "Next Focus",
      completediagnosticNextFocus: "Complete the diagnostic to define your next focus area.",
      priority: "Priority",
      skillBreakdown: "Skill Breakdown",
      skillBreakdownText: "Detailed view of the skills, levels, and priorities identified by the diagnostic.",
      scoreLabel: "Score",
      highPriorityDesc: "Address first with targeted training and guided practice.",
      mediumPriorityDesc: "Strengthen with focused exercises and concrete use cases.",
      lowPriorityDesc: "Good current level, with room for optimization and deeper development.",
      noResults: "No diagnostic results found",
      noResultsText: "Take the diagnostic to display your dashboard and generate your priorities.",
      startdiagnostic: "Start diagnostic",
      aiProfile: "Your AI Profile",
      aiProfileGlobalScore: "Global Score",
      aiNovice: "AI Novice",
      aiPractitioner: "AI Practitioner",
      aiLeader: "AI Leader",
      yourUseCases: "Your 3 business use cases:",
      perfTitle: "Performance Analysis",
      perfSubtitle: "AI-generated insights on your learning blockers and recommended interventions.",
      perfAnalyze: "Analyze my performance",
      perfAnalyzing: "Analyzing...",
      perfEngagement: "Engagement rate",
      perfTrend: "Trend",
      perfBlockers: "Top 3 blockers",
      perfInterventions: "Recommended interventions",
      perfEvidence: "Evidence",
      perfImpact: "Business impact",
      trendImproving: "📈 Improving",
      trendStable: "➡️ Stable",
      trendDeclining: "📉 Declining",
      interventionReview: "Review section",
      interventionTutorial: "Watch tutorial",
      interventionCoach: "Coach session",
      priorityHigh: "High",
      priorityMedium: "Medium",
      priorityLow: "Low",
    },
    fr: {
      heroBadge: "Tableau de bord des capacités IA",
      title: "Tableau de bord",
      subtitle: "Suivez votre progression sur vos 3 use cases business et activez les AI Blueprints qui vous feront passer au niveau supérieur.",
      viewRoadmap: "Voir ma Feuille de route IA",
      redodiagnostic: "Refaire le diagnostic",
      confirmTitle: "Refaire le diagnostic ?",
      confirmMessage: "Vos scores actuels seront remplacés par les nouveaux résultats. Cette action est irréversible.",
      confirmLabel: "Oui, refaire",
      cancelLabel: "Annuler",
      globalScore: "Score IA global",
      globalScoreText: "Score moyen estimé sur l'ensemble des compétences évaluées.",
      highPriorityGaps: "Écarts à haute priorité",
      highPrioritySkills: "Compétences prioritaires",
      highPriorityText: "Compétences à renforcer en priorité pour accélérer votre progression.",
      noGapsTitle: "Aucun écart prioritaire",
      noGapsText: "Excellent ! Continuez à progresser avec les modules recommandés.",
      nextFocus: "Prochain focus",
      completediagnosticNextFocus: "Complétez le diagnostic pour définir votre prochain axe de focus.",
      priority: "Priorité",
      skillBreakdown: "Répartition des compétences",
      skillBreakdownText: "Vue détaillée des compétences, niveaux et priorités identifiés par le diagnostic.",
      scoreLabel: "Score",
      highPriorityDesc: "À traiter en priorité avec une formation ciblée et une pratique guidée.",
      mediumPriorityDesc: "À renforcer avec des exercices ciblés et des cas d'usage concrets.",
      lowPriorityDesc: "Bon niveau actuel, avec un potentiel d'optimisation et d'approfondissement.",
      noResults: "Aucun résultat de diagnostic trouvé",
      noResultsText: "Faites le diagnostic pour afficher votre dashboard et générer vos priorités.",
      startdiagnostic: "Commencer le diagnostic",
      aiProfile: "Votre profil IA",
      aiProfileGlobalScore: "Score global",
      aiNovice: "Novice IA",
      aiPractitioner: "Praticien IA",
      aiLeader: "Leader IA",
      yourUseCases: "Vos 3 use cases business :",
      perfTitle: "Analyse de performance",
      perfSubtitle: "Insights générés par l'IA sur vos blockers d'apprentissage et interventions recommandées.",
      perfAnalyze: "Analyser ma performance",
      perfAnalyzing: "Analyse en cours...",
      perfEngagement: "Taux d'engagement",
      perfTrend: "Tendance",
      perfBlockers: "Top 3 blockers",
      perfInterventions: "Interventions recommandées",
      perfEvidence: "Evidence",
      perfImpact: "Impact business",
      trendImproving: "📈 En progression",
      trendStable: "➡️ Stable",
      trendDeclining: "📉 En déclin",
      interventionReview: "Revoir la section",
      interventionTutorial: "Voir le tutoriel",
      interventionCoach: "Session coach",
      priorityHigh: "Haute",
      priorityMedium: "Moyenne",
      priorityLow: "Basse",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        // ── 1 seul appel diagnostic/status (fusionné) ──
        const sRes = await apiFetch("/api/v1/diagnostic/status");
        if (!sRes) return;
        const sData = await sRes.json().catch(() => ({}));
        if (sRes.ok) setDiagStatus(sData);
        if (sRes.ok && sData.required) { navigate("/diagnostic"); return; }
        const res = await apiFetch("/api/v1/diagnostic/results");
        if (!res) return;
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          const msg = data?.detail || "";
          if (String(msg).toLowerCase().includes("career path")) { navigate("/onboarding"); return; }
          setSkills([]); return;
        }
        setSkills(Array.isArray(data) ? data : []);
        const roadmapRes = await apiFetch("/api/v1/roadmap");
        if (roadmapRes?.ok) {
          const roadmapData = await roadmapRes.json().catch(() => ({}));
          if (roadmapData?.summary) setSummary(roadmapData.summary);
        }
      } catch { setSkills([]); }
    })();
  }, [navigate]);

  const analyzePerformance = async () => {
    setPerfLoading(true);
    try {
      const res = await apiFetch("/api/v1/performance/analyze", {
        method: "POST",
        body: JSON.stringify({ scope: "learner" }),
      });
      if (res?.ok) {
        const data = await res.json();
        setPerfData(data);
      }
    } catch { /* non-blocking */ }
    finally { setPerfLoading(false); }
  };

  const userRole = useMemo(() => {
    if (summary?.role_en) return summary.role_en;
    try {
      const raw = localStorage.getItem("auth_user");
      if (!raw) return null;
      return JSON.parse(raw)?.career_path_name || null;
    } catch { return null; }
  }, [summary]);

  const userRoleDetails = useMemo(() => {
    if (!userRole) return null;
    return ROLE_DETAILS[userRole] || null;
  }, [userRole]);

  const globalScore = useMemo(() => {
    if (!skills.length) return 0;
    const avg = skills.reduce((acc, s) => acc + (Number(s.score) || 0), 0) / skills.length;
    return Math.round(avg);
  }, [skills]);

  const highCount = useMemo(() => skills.filter(s => String(s.priority).toUpperCase() === "HIGH").length, [skills]);

  const nextMove = useMemo(() => {
    if (!skills.length) return null;
    const rank = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return 0; if (v === "MEDIUM") return 1; return 2; };
    return [...skills].sort((a, b) => { const pr = rank(a.priority) - rank(b.priority); if (pr !== 0) return pr; return (Number(a.score) || 0) - (Number(b.score) || 0); })[0];
  }, [skills]);

  const sortedSkills = useMemo(() => {
    if (!skills.length) return [];
    const rank = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return 0; if (v === "MEDIUM") return 1; return 2; };
    return [...skills].sort((a, b) => { const pr = rank(a.priority) - rank(b.priority); if (pr !== 0) return pr; return (Number(b.score) || 0) - (Number(a.score) || 0); });
  }, [skills]);

  const aiProfile = useMemo(() => {
    const getBadgeClass = score => {
      if (score < 40) return "border-amber-200 bg-amber-50 text-amber-700";
      if (score <= 70) return "border-sky-200 bg-sky-50 text-sky-700";
      return "border-emerald-200 bg-emerald-50 text-emerald-700";
    };
    if (summary) {
      return { label: lang === "fr" ? summary.profile_fr : summary.profile, description: lang === "fr" ? summary.description_fr : summary.description_en, role: lang === "fr" ? summary.role_fr : summary.role_en, cta: lang === "fr" ? summary.cta_fr : summary.cta_en, badgeClass: getBadgeClass(globalScore) };
    }
    let fallbackLabel = globalScore < 40 ? t[lang].aiNovice : globalScore <= 70 ? t[lang].aiPractitioner : t[lang].aiLeader;
    return { label: fallbackLabel, description: null, role: userRole, cta: t[lang].viewRoadmap, badgeClass: getBadgeClass(globalScore) };
  }, [globalScore, lang, summary, userRole]);

  // Peut refaire le diagnostic si 90j écoulés OU si pas de scores
  const canRetake = diagStatus?.recommended === true || !skills.length;

  const priorityBadgeClass = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return "border-red-200 bg-red-50 text-red-700"; if (v === "MEDIUM") return "border-amber-200 bg-amber-50 text-amber-700"; return "border-emerald-200 bg-emerald-50 text-emerald-700"; };
  const levelBadgeClass = lvl => { const v = String(lvl || "").toLowerCase(); if (v.includes("begin")) return "border-emerald-200 bg-emerald-50 text-emerald-700"; if (v.includes("inter")) return "border-sky-200 bg-sky-50 text-sky-700"; return "border-violet-200 bg-violet-50 text-violet-700"; };
  const nextFocusText = nextMove ? `${t[lang].priority} ${String(nextMove.priority).toUpperCase()} • ${nextMove.level}` : t[lang].completediagnosticNextFocus;
  const getPriorityDescription = priority => { const value = String(priority).toUpperCase(); if (value === "HIGH") return t[lang].highPriorityDesc; if (value === "MEDIUM") return t[lang].mediumPriorityDesc; return t[lang].lowPriorityDesc; };

  const trendLabel = trend => {
    if (trend === "improving") return t[lang].trendImproving;
    if (trend === "declining") return t[lang].trendDeclining;
    return t[lang].trendStable;
  };

  const trendColor = trend => {
    if (trend === "improving") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (trend === "declining") return "border-red-200 bg-red-50 text-red-700";
    return "border-slate-200 bg-slate-50 text-slate-600";
  };

  const interventionLabel = type => {
  if (type === "review_section") return t[lang].interventionReview;
  if (type === "watch_tutorial") return t[lang].interventionTutorial;
  if (type === "coach_session") return t[lang].interventionCoach;
  return type;
};

  const interventionIcon = type => {
  if (type === "review_section") return "📖";
  if (type === "watch_tutorial") return "🎬";
  if (type === "coach_session") return "🤝";
  return "💡";
};

  const priorityLabel = p => {
    if (p === "high") return t[lang].priorityHigh;
    if (p === "medium") return t[lang].priorityMedium;
    return t[lang].priorityLow;
  };

  const priorityColor = p => {
    if (p === "high") return "border-red-200 bg-red-50 text-red-700";
    if (p === "medium") return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-emerald-200 bg-emerald-50 text-emerald-700";
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* ── Conteneur principal — tout est à l'intérieur ── */}
      <div className="mx-auto max-w-page">

        {/* ─── 1. HERO ─── */}
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">{t[lang].heroBadge}</div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{t[lang].title}</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">{t[lang].subtitle}</p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <RetakeDiagnosticBtn
                canRetake={canRetake}
                nextAllowedAt={diagStatus?.next_allowed_at}
                onClick={() => setShowConfirm(true)}
                tx={t[lang]}
                lang={lang}
              />
            </div>
          </div>
        </section>

        {/* ─── 2. PROFIL IA ─── */}
        {!!skills.length && (
          <section className="mt-6 rounded-3xl border-2 border-euk-primary/30 bg-gradient-to-br from-euk-primary/10 to-euk-primary/5 p-6 shadow-md md:p-8">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <div className="mb-1 text-xs font-bold uppercase tracking-wide text-euk-primary">{t[lang].aiProfile}</div>
                <div className="text-3xl font-bold text-euk-dark md:text-4xl">{aiProfile.label}</div>
                {aiProfile.role && <div className="mt-2 text-sm font-semibold text-euk-primary md:text-base">{aiProfile.role}</div>}
              </div>
              <div className={["rounded-full border px-5 py-2.5 text-base font-bold", aiProfile.badgeClass].join(" ")}>{globalScore}% {t[lang].aiProfileGlobalScore}</div>
            </div>
            {aiProfile.description && <p className="mt-5 text-sm leading-7 text-slate-700 md:text-base">{aiProfile.description}</p>}
            {userRoleDetails && (
              <div className="mt-6">
                <div className="text-xs font-bold uppercase tracking-wide text-slate-500 mb-3">{t[lang].yourUseCases}</div>
                <div className="flex flex-col gap-2.5">
                  {userRoleDetails.useCases.map(uc => (
                    <div key={uc.name} className="flex items-center gap-3 text-sm text-slate-700 md:text-base">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="shrink-0">
                        <circle cx="12" cy="12" r="11" fill="rgba(0,179,160,0.20)" />
                        <path d="M7 12.5L10.5 16L17 9" stroke="#006355" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      <span className="font-semibold">{uc.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <button onClick={() => navigate("/roadmap")} className="mt-7 w-full rounded-2xl bg-euk-primary px-6 py-4 text-base font-bold text-white shadow-lg shadow-euk-primary/20 transition hover:-translate-y-0.5 hover:bg-euk-deep hover:shadow-xl md:w-auto md:min-w-[280px]">
              {aiProfile.cta || `${t[lang].viewRoadmap} →`}
            </button>
          </section>
        )}

        {/* ─── 3. KPI CARDS ─── */}
        {!!skills.length && (
          <section className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="text-sm font-medium text-slate-500">{t[lang].globalScore}</div>
              <div className="mt-3 text-3xl font-bold tracking-tight text-euk-primary">{globalScore}%</div>
              <div className="mt-4 h-2.5 w-full rounded-full bg-slate-100">
                <div className="h-2.5 rounded-full bg-euk-primary" style={{ width: `${globalScore}%` }} />
              </div>
              <div className="mt-3 text-sm text-slate-500">{t[lang].globalScoreText}</div>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="text-sm font-medium text-slate-500">{t[lang].highPriorityGaps}</div>
              {highCount > 0 ? (
                <>
                  <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">{highCount}</div>
                  <div className="mt-3 inline-flex rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">{t[lang].highPrioritySkills}</div>
                  <div className="mt-4 text-sm text-slate-500">{t[lang].highPriorityText}</div>
                </>
              ) : (
                <>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    </div>
                    <span className="text-base font-bold text-emerald-700">{t[lang].noGapsTitle}</span>
                  </div>
                  <div className="mt-4 text-sm text-slate-500">{t[lang].noGapsText}</div>
                </>
              )}
            </div>
            <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="text-sm font-medium text-slate-500">{t[lang].nextFocus}</div>
              <div className="mt-3 text-xl font-bold leading-tight text-euk-dark">{nextMove?.skill_name || "—"}</div>
              <div className="mt-3 text-sm text-slate-500">{nextFocusText}</div>
            </div>
          </section>
        )}

        {/* ─── 4. SKILL BREAKDOWN ─── */}
        <section className="mt-8">
          <div className="mb-4">
            <h2 className="text-lg font-bold text-euk-dark">{t[lang].skillBreakdown}</h2>
            <p className="mt-1 text-sm text-slate-500">{t[lang].skillBreakdownText}</p>
          </div>
          {!!sortedSkills.length && (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {sortedSkills.map(s => (
                <div key={s.skill_id} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-base font-bold leading-snug text-euk-dark">{s.skill_name}</h3>
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", priorityBadgeClass(s.priority)].join(" ")}>{String(s.priority).toUpperCase()}</span>
                  </div>
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(s.level)].join(" ")}>{s.level}</span>
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-euk-dark">{t[lang].scoreLabel}: {s.score}%</span>
                  </div>
                  <div className="mt-4 h-2.5 w-full rounded-full bg-slate-100">
                    <div className="h-2.5 rounded-full bg-euk-primary" style={{ width: `${Number(s.score) || 0}%` }} />
                  </div>
                  <div className="mt-4 text-sm leading-6 text-slate-500">{getPriorityDescription(s.priority)}</div>
                </div>
              ))}
            </div>
          )}
          {!sortedSkills.length && (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
              <div className="text-base font-semibold text-euk-dark">{t[lang].noResults}</div>
              <div className="mt-2 text-sm text-slate-500">{t[lang].noResultsText}</div>
              <button onClick={() => navigate("/diagnostic")} className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">{t[lang].startdiagnostic}</button>
            </div>
          )}
        </section>

        {/* ─── 5. PERFORMANCE ANALYSIS AGENT ─── */}
        <section className="mt-8 mb-8">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-euk-dark">{t[lang].perfTitle}</h2>
              <p className="mt-1 text-sm text-slate-500">{t[lang].perfSubtitle}</p>
            </div>
            <button
              onClick={analyzePerformance}
              disabled={perfLoading}
              className="rounded-2xl bg-euk-primary px-5 py-2.5 text-sm font-bold text-white transition hover:bg-euk-deep disabled:opacity-50 disabled:cursor-not-allowed">
              {perfLoading ? t[lang].perfAnalyzing : t[lang].perfAnalyze}
            </button>
          </div>

          {perfLoading && (
            <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
              <div className="flex items-center justify-center gap-3">
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
                <span className="text-sm text-slate-500">{t[lang].perfAnalyzing}</span>
              </div>
            </div>
          )}

          {perfData && !perfLoading && (
            <div className="space-y-4">
              {/* Summary + Trend + Engagement */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <p className="flex-1 text-sm leading-6 text-slate-700">{perfData.summary}</p>
                  <div className="flex flex-wrap gap-2 shrink-0">
                    <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${trendColor(perfData.trend)}`}>
                      {trendLabel(perfData.trend)}
                    </span>
                    <span className="rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-semibold text-sky-700">
                      {t[lang].perfEngagement} : {Math.round((perfData.engagement_rate || 0) * 100)}%
                    </span>
                  </div>
                </div>
              </div>
              {/* KPI + Execution Task metrics */}
{(perfData.kpi_before_avg !== undefined || perfData.execution_task_completion_rate !== undefined) && (
  <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
    <h3 className="text-base font-bold text-euk-dark mb-4">
      {lang === "fr" ? "Métriques clés" : "Key metrics"}
    </h3>
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

      {/* KPI avant */}
      <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4 text-center">
        <div className="text-xs font-bold uppercase tracking-wide text-slate-500 mb-2">
          {lang === "fr" ? "KPI moyen avant" : "Avg KPI before"}
        </div>
        <div className="text-2xl font-bold text-slate-700">
          {Math.round((perfData.kpi_before_avg || 0) * 100)}%
        </div>
      </div>

      {/* KPI après */}
      <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4 text-center">
        <div className="text-xs font-bold uppercase tracking-wide text-emerald-600 mb-2">
          {lang === "fr" ? "KPI moyen après" : "Avg KPI after"}
        </div>
        <div className="text-2xl font-bold text-emerald-700">
          {Math.round((perfData.kpi_after_avg || 0) * 100)}%
        </div>
      </div>

      {/* Taux soumission Execution Task */}
      <div className="rounded-2xl border border-sky-100 bg-sky-50 p-4 text-center">
        <div className="text-xs font-bold uppercase tracking-wide text-sky-600 mb-2">
          {lang === "fr" ? "Missions soumises" : "Tasks submitted"}
        </div>
        <div className="text-2xl font-bold text-sky-700">
          {Math.round((perfData.execution_task_completion_rate || 0) * 100)}%
        </div>
      </div>

      {/* Section de drop-off principal */}
      <div className="rounded-2xl border border-amber-100 bg-amber-50 p-4 text-center">
        <div className="text-xs font-bold uppercase tracking-wide text-amber-600 mb-2">
          {lang === "fr" ? "Section drop-off" : "Drop-off section"}
        </div>
        <div className="text-sm font-bold text-amber-700 capitalize">
          {perfData.main_drop_off_section
            ? perfData.main_drop_off_section.replace(/_/g, " ")
            : "—"}
        </div>
      </div>

    </div>
  </div>
)}
              {/* Top 3 Blockers */}
              {perfData.top_blockers?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">{t[lang].perfBlockers}</h3>
                  <div className="space-y-3">
                    {perfData.top_blockers.map((blocker, idx) => (
                      <div key={idx} className="flex items-start gap-4 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-red-100 text-sm font-bold text-red-700">
                          {blocker.rank}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold text-euk-dark">{blocker.skill}</div>
                          <div className="mt-1 flex items-center gap-2">
                            <div className="h-1.5 flex-1 max-w-[120px] rounded-full bg-slate-200">
                              <div className="h-1.5 rounded-full bg-euk-primary" style={{ width: `${Math.round((blocker.mastery_score || 0) * 100)}%` }} />
                            </div>
                            <span className="text-xs text-slate-500">{Math.round((blocker.mastery_score || 0) * 100)}%</span>
                          </div>
                          <div className="mt-1.5 text-xs text-slate-500">
                            <span className="font-medium">{t[lang].perfEvidence} :</span> {blocker.evidence}
                          </div>
                          <div className="mt-1 text-xs text-slate-500">
                            <span className="font-medium">{t[lang].perfImpact} :</span> {blocker.impact}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Interventions */}
              {perfData.interventions?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">{t[lang].perfInterventions}</h3>
                  <div className="grid gap-3 md:grid-cols-3">
                    {perfData.interventions.map((item, idx) => (
                      <div key={idx} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xl">{interventionIcon(item.type)}</span>
                          <span className="text-xs font-bold text-euk-dark">{interventionLabel(item.type)}</span>
                          <span className={`ml-auto rounded-full border px-2 py-0.5 text-xs font-semibold ${priorityColor(item.priority)}`}>
                            {priorityLabel(item.priority)}
                          </span>
                        </div>
                        <div className="text-xs font-semibold text-slate-600 mb-1">{item.skill}</div>
                        <div className="text-xs text-slate-500 leading-5">{item.reason}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

      {/* ─── LEARNER PROGRESS DASHBOARD ─── */}
        <LearnerProgressDashboard lang={lang} />

      </div>{/* ── fin max-w-page ── */}

      {showConfirm && (
        <ConfirmModal
          title={t[lang].confirmTitle}
          message={t[lang].confirmMessage}
          confirmLabel={t[lang].confirmLabel}
          cancelLabel={t[lang].cancelLabel}
          confirmClass="bg-rose-500 hover:bg-rose-600"
          onConfirm={() => { setShowConfirm(false); navigate("/diagnostic"); }}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
  function LearnerProgressDashboard({ lang }) {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [kpiByModule, setKpiByModule] = useState({});

  const load = async () => {
    setLoading(true);
    try {
      const res = await apiFetch("/api/v1/roadmap");
      if (res?.ok) {
        const data = await res.json();
        const items = data.items || [];
        setModules(items);
        setLoaded(true);

        // Charger les KPI pour chaque module en cours ou complété
        const kpiMap = {};
        await Promise.all(
          items
            .filter(m => m.status !== "not_started")
            .map(async (m) => {
              try {
                const r = await apiFetch(`/api/v1/kpi/${m.module_id}`);
                if (r?.ok) {
                  const kpis = await r.json();
                  if (kpis.length > 0) kpiMap[m.module_id] = kpis;
                }
              } catch { /* non-blocking */ }
            })
        );
        setKpiByModule(kpiMap);
      }
    } catch { /* non-blocking */ }
    finally { setLoading(false); }
  };

  const SECTIONS = ["use_case", "kpi", "execution_content", "execution_task", "kpi_measurement", "progress_update"];

  const sectionLabel = (s) => ({
    use_case: "Use Case", kpi: "KPI", execution_content: "Contenu",
    execution_task: "Mission", kpi_measurement: "Mesure KPI", progress_update: "Bilan"
  }[s] || s);

  const statusColor = (status) => {
    if (status === "completed") return "bg-emerald-500";
    if (status === "in_progress") return "bg-amber-400";
    return "bg-slate-200";
  };

  const flagColor = (flag) => {
    if (flag === "good") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (flag === "needs_improvement") return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-red-200 bg-red-50 text-red-700";
  };

  const modulesWithProgress = modules.filter(m => m.status !== "not_started");

  return (
    <section className="mt-8 mb-8">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-bold text-euk-dark">
          {lang === "fr" ? "Ma progression détaillée" : "My detailed progress"}
        </h2>
        <button
          onClick={load}
          disabled={loading}
          className="rounded-2xl bg-euk-primary px-5 py-2.5 text-sm font-bold text-white transition hover:bg-euk-deep disabled:opacity-50">
          {loading
            ? (lang === "fr" ? "Chargement..." : "Loading...")
            : (lang === "fr" ? "Voir ma progression" : "View my progress")}
        </button>
      </div>

      {loading && (
        <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <div className="flex items-center justify-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
          </div>
        </div>
      )}

      {loaded && !loading && modulesWithProgress.length === 0 && (
        <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <p className="text-sm text-slate-500">
            {lang === "fr" ? "Aucun module commencé." : "No module started yet."}
          </p>
        </div>
      )}

      {loaded && !loading && modulesWithProgress.length > 0 && (
        <div className="space-y-4">
          {/* Mastery Heatmap */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-base font-bold text-euk-dark mb-1">
              {lang === "fr" ? "Mastery Heatmap" : "Mastery Heatmap"}
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              {lang === "fr" ? "Progression par section pour chaque module commencé." : "Progress by section for each started module."}
            </p>
            <div className="space-y-4">
              {modulesWithProgress.map((m, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-euk-dark truncate max-w-xs">{m.module_title_fr || m.module_title_en}</span>
                    <span className={`rounded-full border px-2 py-0.5 text-xs font-semibold
                      ${m.status === "completed" ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : m.status === "in_progress" ? "border-sky-200 bg-sky-50 text-sky-700"
                        : "border-slate-200 bg-slate-50 text-slate-500"}`}>
                      {m.status === "completed" ? "✓ Terminé" : m.status === "in_progress" ? "En cours" : "Non commencé"}
                    </span>
                  </div>
                  {/* Heatmap sections */}
                  <div className="flex gap-1">
                    {SECTIONS.map((s) => {
                      const sectionItem = Array.isArray(m.section_progress)
  ? m.section_progress.find(sp => sp.section_type === s)
  : null;
const status = sectionItem?.status || "not_started";
                      return (
                        <div key={s} className="flex-1 group relative">
                          <div className={`h-6 rounded ${statusColor(status)}`} />
                          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 hidden group-hover:block z-10">
                            <div className="rounded-lg bg-slate-800 px-2 py-1 text-xs text-white whitespace-nowrap">
                              {sectionLabel(s)}: {status}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                  <div className="flex gap-1 mt-1">
                    {SECTIONS.map((s) => (
                      <div key={s} className="flex-1 text-center text-xs text-slate-400 truncate">{sectionLabel(s)}</div>
                    ))}
                  </div>
                  {/* Progress bar */}
                  <div className="mt-2 flex items-center gap-2">
                    <div className="h-1.5 flex-1 rounded-full bg-slate-100">
                      <div className="h-1.5 rounded-full bg-euk-primary transition-all" style={{ width: `${m.progress_percent || 0}%` }} />
                    </div>
                    <span className="text-xs font-semibold text-euk-primary">{m.progress_percent || 0}%</span>
                  </div>
                </div>
              ))}
            </div>
            {/* Légende */}
            <div className="mt-4 flex items-center gap-4 text-xs text-slate-500">
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-emerald-500" />{lang === "fr" ? "Complété" : "Completed"}</div>
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-amber-400" />{lang === "fr" ? "En cours" : "In progress"}</div>
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-slate-200" />{lang === "fr" ? "Non commencé" : "Not started"}</div>
            </div>
          </div>

          {/* KPI Improvement */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-base font-bold text-euk-dark mb-1">
              {lang === "fr" ? "Mes KPIs — Avant / Après" : "My KPIs — Before / After"}
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              {lang === "fr" ? "Impact mesuré après complétion de chaque module." : "Measured impact after completing each module."}
            </p>
            <div className="space-y-3">
              {modulesWithProgress.map((m, i) => {
                const kpis = kpiByModule[m.module_id] || [];
                return (
                  <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                    <div className="text-sm font-semibold text-euk-dark mb-3">{m.title_fr || m.title_en}</div>
                    {kpis.length > 0 ? (
                      <div className="space-y-2">
                        {kpis.map((kpi, kIdx) => (
                          <div key={kIdx} className="grid grid-cols-2 gap-2 text-xs">
                            <div className="col-span-2 text-xs font-semibold text-slate-500 mb-0.5">{kpi.indicator}</div>
                            <div className="rounded-xl border border-red-100 bg-red-50 p-2.5">
                              <div className="font-bold text-red-700 mb-0.5">
                                {lang === "fr" ? "KPI Avant" : "KPI Before"}
                              </div>
                              <div className="text-slate-700 font-semibold">
                                {kpi.baseline_value !== null ? `${kpi.baseline_value} ${kpi.unit || ""}` : "—"}
                              </div>
                            </div>
                            <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-2.5">
                              <div className="font-bold text-emerald-700 mb-0.5">
                                {lang === "fr" ? "KPI Après" : "KPI After"}
                              </div>
                              <div className="text-slate-700 font-semibold">
                                {kpi.current_value !== null
                                  ? `${kpi.current_value} ${kpi.unit || ""}`
                                  : (lang === "fr" ? "Non mesuré encore" : "Not measured yet")}
                              </div>
                            </div>
                            {kpi.current_value !== null && kpi.baseline_value !== null && (
                              <div className="col-span-2 rounded-xl border border-sky-100 bg-sky-50 p-2.5">
                                <span className="text-xs font-bold text-sky-700">
                                  {lang === "fr" ? "Cible : " : "Target: "}{kpi.target_label}
                                </span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div className="rounded-xl border border-red-100 bg-red-50 p-3">
                          <div className="font-bold text-red-700 mb-1">{lang === "fr" ? "KPI Avant" : "KPI Before"}</div>
                          <div className="text-slate-500">—</div>
                        </div>
                        <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-3">
                          <div className="font-bold text-emerald-700 mb-1">{lang === "fr" ? "KPI Après" : "KPI After"}</div>
                          <div className="text-slate-500">{lang === "fr" ? "Non mesuré encore" : "Not measured yet"}</div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
}