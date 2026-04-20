import { useMemo, useEffect } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { useApi } from "../hooks/useApi";

export default function AIRoadmapPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext();
  const lang = language || "en";

  const { data: roadmapData, loading, refetch } = useApi("/api/v1/roadmap");
  useEffect(() => {
    const handleFocus = () => refetch();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [refetch]);

  const roadmapItems = roadmapData?.items || [];
  const roadmapProgress = roadmapData?.roadmap_progress || 0;
  const modulesCompleted = roadmapData?.modules_completed || 0;
  const modulesTotal = roadmapData?.modules_total || 0;

  const t = {
    en: {
      personalizedPlan: "Personalized development plan",
      title: "AI Roadmap",
      subtitle: "Your personalized 90-day AI capability development plan based on your current assessment priorities.",
      updateAssessment: "Update assessment",
      loading: "Loading roadmap...",
      noRoadmap: "No roadmap available",
      noRoadmapText: "Complete the assessment to generate your personalized roadmap.",
      startAssessment: "Start assessment",
      roadmapProgress: "Roadmap Progress",
      modulesCompleted: "core modules completed.",
      highPriorityAreas: "High Priority Areas",
      focusFirst: "Focus first",
      noCriticalGaps: "No critical gaps",
      allCompleted: "All modules completed!",
      duration: "Duration",
      durationValue: "90 days",
      durationText: "Recommended roadmap cycle before reassessment.",
      roadmap90: "90-Day Roadmap",
      roadmap90Text: "A structured progression path to help you build, apply and integrate AI capabilities.",
      focusAreas: "Focus areas",
      expectedOutcome: "Expected outcome",
      recommendedModules: "Recommended modules",
      skill: "Skill",
      startModule: "Start module",
      completed: "Completed",
      inProgress: "In progress",
      notStarted: "Not started",
      min: "min",
      phase1Title: "Phase 1 - Foundations",
      phase1Period: "Days 1-30",
      phase1Goal: "Build strong AI fundamentals and address your most urgent capability gaps first.",
      phase1Focus1: "Strengthen priority AI fundamentals",
      phase1Focus2: "Address your highest-priority skill gaps",
      phase1Focus3: "Build confidence with core AI use cases",
      phase1Outcome: "A stronger baseline and clear progress on the most critical areas identified in your assessment.",
      phase1Empty: "No High priority modules in this phase.",
      phase2Title: "Phase 2 - Applied Practice",
      phase2Period: "Days 31-60",
      phase2Goal: "Develop more practical and consistent AI usage through Medium-priority capability building.",
      phase2Focus1: "Apply AI more regularly in work tasks",
      phase2Focus2: "Improve quality and consistency",
      phase2Focus3: "Reinforce practical workflows",
      phase2Outcome: "Better day-to-day AI usage with stronger execution and more relevant outputs.",
      phase2Empty: "No Medium priority modules in this phase.",
      phase3Title: "Phase 3 - Advanced Modules",
      phase3Period: "Days 61-90",
      phase3Goal: "Access the Expert module and prepare for your official Euklydia certification.",
      phase3Focus1: "Access the Expert module and its certification",
      phase3Focus2: "Explore advanced AI strategies and leadership skills",
      phase3Focus3: "Prepare for the official Euklydia certification",
      phase3Outcome: "A clear vision of your full AI learning journey and access to the Expert certification path.",
      phase3Empty: "No advanced modules available.",
      startHere: "Start here",
      journeyStart: "Your journey starts here - complete your first module!",
      roadmapCompleted: "Roadmap completed! Take a new assessment.",
    },
    fr: {
      personalizedPlan: "Plan de developpement personnalise",
      title: "Feuille de route IA",
      subtitle: "Votre plan personnalise de developpement des capacites IA sur 90 jours, base sur les priorites de votre assessment actuel.",
      updateAssessment: "Refaire l'assessment",
      loading: "Chargement de la feuille de route...",
      noRoadmap: "Aucune feuille de route disponible",
      noRoadmapText: "Completez l'assessment pour generer votre feuille de route personnalisee.",
      startAssessment: "Commencer l'assessment",
      roadmapProgress: "Progression de la feuille de route",
      modulesCompleted: "modules principaux termines.",
      highPriorityAreas: "Zones a haute priorite",
      focusFirst: "A traiter en premier",
      noCriticalGaps: "Aucun ecart critique",
      allCompleted: "Tous les modules termines !",
      duration: "Duree",
      durationValue: "90 jours",
      durationText: "Cycle recommande de feuille de route avant une nouvelle evaluation.",
      roadmap90: "Feuille de route sur 90 jours",
      roadmap90Text: "Un parcours structure pour vous aider a developper, appliquer et integrer les capacites IA.",
      focusAreas: "Axes de focus",
      expectedOutcome: "Resultat attendu",
      recommendedModules: "Modules recommandes",
      skill: "Competence",
      startModule: "Commencer le module",
      completed: "Termine",
      inProgress: "En cours",
      notStarted: "Non commence",
      min: "min",
      phase1Title: "Phase 1 - Fondations",
      phase1Period: "Jours 1-30",
      phase1Goal: "Construire de solides bases en IA et traiter d'abord vos ecarts de competences les plus urgents.",
      phase1Focus1: "Renforcer les fondamentaux IA prioritaires",
      phase1Focus2: "Traiter vos ecarts de competences les plus prioritaires",
      phase1Focus3: "Developper la confiance avec les cas d'usage IA essentiels",
      phase1Outcome: "Une base plus solide et des progres clairs sur les domaines les plus critiques identifies dans votre assessment.",
      phase1Empty: "Aucun module de haute priorite dans cette phase.",
      phase2Title: "Phase 2 - Pratique appliquee",
      phase2Period: "Jours 31-60",
      phase2Goal: "Developper un usage plus pratique et plus regulier de l'IA grace au renforcement des capacites de priorite moyenne.",
      phase2Focus1: "Utiliser l'IA plus regulierement dans les taches de travail",
      phase2Focus2: "Ameliorer la qualite et la coherence",
      phase2Focus3: "Renforcer les workflows pratiques",
      phase2Outcome: "Un meilleur usage quotidien de l'IA, avec une execution plus solide et des resultats plus pertinents.",
      phase2Empty: "Aucun module de priorite moyenne dans cette phase.",
      phase3Title: "Phase 3 - Modules Avances",
      phase3Period: "Jours 61-90",
      phase3Goal: "Accedez au module Expert et preparez votre certification officielle Euklydia.",
      phase3Focus1: "Acceder au module Expert et a sa certification",
      phase3Focus2: "Explorer les strategies IA avancees et le leadership",
      phase3Focus3: "Se preparer a la certification officielle Euklydia",
      phase3Outcome: "Une vision claire de votre parcours IA complet et acces au chemin de certification Expert.",
      phase3Empty: "Aucun module avance disponible.",
      startHere: "Commencer ici",
      journeyStart: "Votre parcours commence ici - completez votre premier module !",
      roadmapCompleted: "Roadmap terminee ! Faites un nouvel assessment.",
    },
  };

  const highPriorityAreas = useMemo(() => {
    return roadmapItems.filter(
      (item) => String(item.priority).toUpperCase() === "HIGH"
    ).length;
  }, [roadmapItems]);

  const allHighCompleted = useMemo(() => {
    const highItems = roadmapItems.filter(
      (item) => String(item.priority).toUpperCase() === "HIGH"
    );
    return highItems.length > 0 && highItems.every(
      (item) => item.status === "completed"
    );
  }, [roadmapItems]);

  const phases = useMemo(() => {
    const highItems = roadmapItems.filter((item) => String(item.priority).toUpperCase() === "HIGH");
    const mediumItems = roadmapItems.filter((item) => String(item.priority).toUpperCase() === "MEDIUM");
    const lowItems = roadmapItems.filter((item) => String(item.priority).toUpperCase() === "LOW");

    return [
      {
        title: t[lang].phase1Title, period: t[lang].phase1Period, goal: t[lang].phase1Goal,
        focus: [t[lang].phase1Focus1, t[lang].phase1Focus2, t[lang].phase1Focus3],
        outcome: t[lang].phase1Outcome, items: highItems, emptyMessage: t[lang].phase1Empty,
        accentClass: "border-red-200 bg-red-50 text-red-700", id: "high",
      },
      {
        title: t[lang].phase2Title, period: t[lang].phase2Period, goal: t[lang].phase2Goal,
        focus: [t[lang].phase2Focus1, t[lang].phase2Focus2, t[lang].phase2Focus3],
        outcome: t[lang].phase2Outcome, items: mediumItems, emptyMessage: t[lang].phase2Empty,
        accentClass: "border-amber-200 bg-amber-50 text-amber-700", id: "medium",
      },
      {
        title: t[lang].phase3Title, period: t[lang].phase3Period, goal: t[lang].phase3Goal,
        focus: [t[lang].phase3Focus1, t[lang].phase3Focus2, t[lang].phase3Focus3],
        outcome: t[lang].phase3Outcome, items: lowItems, emptyMessage: t[lang].phase3Empty,
        accentClass: "border-emerald-200 bg-emerald-50 text-emerald-700", id: "low",
      },
    ];
  }, [roadmapItems, lang]);

  const statusBadgeClass = (status) => {
    const value = String(status).toLowerCase();
    if (value.includes("complete")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (value.includes("progress")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-slate-200 bg-slate-50 text-slate-700";
  };

  const statusLabel = (status) => {
    const value = String(status).toLowerCase();
    if (value.includes("complete")) return t[lang].completed;
    if (value.includes("progress")) return t[lang].inProgress;
    return t[lang].notStarted;
  };

  const levelBadgeClass = (level) => {
    const value = String(level || "").toLowerCase();
    if (value.includes("begin")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (value.includes("inter")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-violet-200 bg-violet-50 text-violet-700";
  };

  const goToModule = (moduleId) => {
    if (!moduleId) return;
    navigate(`/learning/module/${moduleId}/units`);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">

        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {t[lang].personalizedPlan}
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">
                {t[lang].title}
              </h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">
                {t[lang].subtitle}
              </p>
            </div>
            <button
              onClick={() => navigate("/assessment")}
              className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
            >
              {t[lang].updateAssessment}
            </button>
          </div>
        </section>

        {loading && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="text-sm text-slate-500">{t[lang].loading}</div>
          </section>
        )}

        {!loading && !roadmapItems.length && (
          <section className="mt-6 rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
            <div className="text-base font-semibold text-euk-dark">{t[lang].noRoadmap}</div>
            <div className="mt-2 text-sm text-slate-500">{t[lang].noRoadmapText}</div>
            <button
              onClick={() => navigate("/assessment")}
              className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep"
            >
              {t[lang].startAssessment}
            </button>
          </section>
        )}

        {!loading && !!roadmapItems.length && (
          <>
            {roadmapProgress === 100 && (
              <section className="mt-6 rounded-3xl border border-emerald-200 bg-emerald-50 p-5 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div className="text-sm font-semibold text-emerald-900">{t[lang].allCompleted}</div>
                  <button
                    onClick={() => navigate("/assessment")}
                    className="rounded-2xl bg-emerald-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:opacity-90"
                  >
                    {t[lang].updateAssessment}
                  </button>
                </div>
              </section>
            )}

            <section className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{t[lang].roadmapProgress}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-primary">{roadmapProgress}%</div>
                <div className="mt-4 h-2.5 w-full rounded-full bg-slate-100">
                  <div className="h-2.5 rounded-full bg-euk-primary transition-all" style={{ width: `${roadmapProgress}%` }} />
                </div>
                <div className="mt-3 text-sm text-slate-500">
                  {modulesCompleted} / {modulesTotal} {t[lang].modulesCompleted}
                </div>
                {roadmapProgress === 0 && (
                  <div className="mt-2 text-xs text-euk-primary font-medium">{t[lang].journeyStart}</div>
                )}
              </div>

              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{t[lang].highPriorityAreas}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">{highPriorityAreas}</div>
                <div className={["mt-3 inline-flex rounded-full border px-3 py-1 text-xs font-semibold",
                  allHighCompleted || highPriorityAreas === 0
                    ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                    : "border-red-200 bg-red-50 text-red-700"
                ].join(" ")}>
                  {allHighCompleted || highPriorityAreas === 0 ? t[lang].noCriticalGaps : t[lang].focusFirst}
                </div>
              </div>

              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{t[lang].duration}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">{t[lang].durationValue}</div>
                <div className="mt-3 text-sm text-slate-500">{t[lang].durationText}</div>
              </div>
            </section>

            <section className="mt-8">
              <div className="mb-4">
                <h2 className="text-lg font-bold text-euk-dark">{t[lang].roadmap90}</h2>
                <p className="mt-1 text-sm text-slate-500">{t[lang].roadmap90Text}</p>
              </div>

              <div className="mb-6 flex gap-3">
                {phases.map((phase) => (
                  <a key={phase.id} href={`#${phase.id}`}
                    className={["rounded-full border px-4 py-1.5 text-xs font-semibold transition hover:opacity-80", phase.accentClass].join(" ")}>
                    {phase.title}
                  </a>
                ))}
              </div>

              <div className="grid gap-6 lg:grid-cols-3">
                {phases.map((phase) => (
                  <div key={phase.title} id={phase.id} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div className={["mb-3 inline-flex rounded-full border px-3 py-1 text-xs font-semibold", phase.accentClass].join(" ")}>
                      {phase.period}
                    </div>
                    <h3 className="text-lg font-bold text-euk-dark">{phase.title}</h3>
                    <p className="mt-3 text-sm leading-6 text-slate-500">{phase.goal}</p>

                    <div className="mt-5">
                      <div className="text-sm font-semibold text-euk-dark">{t[lang].focusAreas}</div>
                      <ul className="mt-3 space-y-2 text-sm text-slate-500">
                        {phase.focus.map((item) => (
                          <li key={item} className="flex items-start gap-2">
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-euk-primary" />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{t[lang].expectedOutcome}</div>
                      <div className="mt-2 text-sm leading-6 text-slate-600">{phase.outcome}</div>
                    </div>

                    <div className="mt-5">
                      <div className="text-sm font-semibold text-euk-dark">{t[lang].recommendedModules}</div>
                      {phase.items.length > 0 ? (
                        <div className="mt-3 space-y-3">
                          {phase.items.map((item, index) => (
                            <div key={`${phase.id}-${item.module_id}-${index}`}
                              className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                              <div className="flex items-start justify-between gap-3">
                                <div>
                                  <div className="text-sm font-semibold text-euk-dark">
                                    {index + 1}. {lang === "fr" ? item.module_title_fr || item.module_title : item.module_title}
                                  </div>
                                  <div className="mt-1 flex flex-wrap gap-1">
                                    {(item.covered_skills?.length > 0
                                      ? item.covered_skills
                                      : [{ skill_name: item.skill_name }]
                                    ).map((s, si) => (
                                      <span key={si} className="rounded-full border border-slate-200 bg-white px-2 py-0.5 text-xs text-slate-500">
                                        {s.skill_name}
                                      </span>
                                    ))}
                                  </div>
                                </div>
                                {index === 0 && phase.id === "high" && !allHighCompleted && (
                                  <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">
                                    {t[lang].startHere}
                                  </span>
                                )}
                              </div>

                              <div className="mt-3 flex flex-wrap items-center gap-2">
                                <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(item.level)].join(" ")}>
                                  {item.level}
                                </span>
                                <span className={["rounded-full border px-3 py-1 text-xs font-semibold", statusBadgeClass(item.status)].join(" ")}>
                                  {statusLabel(item.status)}
                                </span>
                                {item.estimated_duration_min && (
                                  <span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-700">
                                    {item.estimated_duration_min} {t[lang].min}
                                  </span>
                                )}
                              </div>

                              <button
                                onClick={() => goToModule(item.module_id)}
                                className="mt-4 w-fit rounded-2xl bg-euk-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-euk-deep"
                              >
                                {t[lang].startModule}
                              </button>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="mt-3 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-500">
                          {phase.emptyMessage}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
}