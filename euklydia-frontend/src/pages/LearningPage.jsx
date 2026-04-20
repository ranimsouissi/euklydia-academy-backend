import { useEffect, useMemo, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";

export default function LearningPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext();

  const [roadmapItems, setRoadmapItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [allModules, setAllModules] = useState([]);
  const [roadmapProgress, setRoadmapProgress] = useState(0);
  const [modulesCompleted, setModulesCompleted] = useState(0);
  const [modulesTotal, setModulesTotal] = useState(0);

  const lang = language || "en";

  const t = {
    en: {
      untitledModule: "Untitled module",
      recommendedModuleFor: "Recommended module for",
      min: "min",
      completed: "Completed",
      inProgress: "In progress",
      notStarted: "Not started",
      continue: "Continue",
      review: "Review",
      start: "Start",
      personalizedLearningExperience: "Personalized learning experience",
      learning: "Learning",
      learningIntro: "Explore your recommended learning modules and follow a focused, personalized AI upskilling journey.",
      viewAIRoadmap: "View AI Roadmap",
      loadingLearningContent: "Loading learning content...",
      noLearningModulesAvailable: "No learning modules available",
      completeAssessment: "Complete the assessment to generate your recommended modules.",
      startAssessment: "Start assessment",
      suggestedModules: "Suggested Modules",
      coreRoadmapProgress: "Core Roadmap Progress",
      coreModulesCompleted: "core modules completed.",
      deepenStrongCapabilities: "Modules suggested to deepen already strong AI capabilities.",
      inProgressCard: "In Progress",
      startedModules: "Modules you have already started.",
      completedCard: "Completed",
      completedModules: "Modules you have already completed.",
      learningTime: "Learning Time",
      learningTimeDescription: "Estimated total active learning time in this learning cycle.",
      continueThisModule: "Continue this module",
      reviewThisModule: "Review this module",
      continueStrengthening: "Continue strengthening",
      nextRecommendedModule: "Next recommended module",
      progress: "Progress",
      highPriority: "priority",
      recommendedRoadmap: "Recommended Roadmap",
      roadmapDescription: "Modules selected to address your current High and Medium priority skill gaps.",
      startHere: "Start here",
      optionalModules: "Optional Modules",
      optionalModulesDescription: "Modules available to explore beyond your current recommended path.",
      exploreModule: "Explore Module",
      advancedLearningRecommendations: "Advanced Learning Recommendations",
      advancedLearningDescription: "Your assessment shows strong performance across all assessed AI skill areas.",
      introductory: "Introductory", core: "Core", applied: "Applied", advanced: "Advanced",
      beginner: "Beginner", intermediate: "Intermediate",
      high: "High", mediumPriority: "Medium", low: "Low",
      blended: "Blended", video: "Video", infographic: "Infographic",
    },
    fr: {
      untitledModule: "Module sans titre",
      recommendedModuleFor: "Module recommandé pour",
      min: "min",
      completed: "Terminé",
      inProgress: "En cours",
      notStarted: "Non commencé",
      continue: "Continuer",
      review: "Revoir",
      start: "Commencer",
      personalizedLearningExperience: "Expérience d'apprentissage personnalisée",
      learning: "Apprentissage",
      learningIntro: "Explorez vos modules recommandés et suivez un parcours personnalisé de montée en compétences en IA.",
      viewAIRoadmap: "Voir la feuille de route IA",
      loadingLearningContent: "Chargement du contenu d'apprentissage...",
      noLearningModulesAvailable: "Aucun module d'apprentissage disponible",
      completeAssessment: "Complétez l'assessment pour générer vos modules recommandés.",
      startAssessment: "Commencer l'assessment",
      suggestedModules: "Modules suggérés",
      coreRoadmapProgress: "Progression de la roadmap principale",
      coreModulesCompleted: "modules principaux terminés.",
      deepenStrongCapabilities: "Modules suggérés pour approfondir des capacités IA déjà solides.",
      inProgressCard: "En cours",
      startedModules: "Modules que vous avez déjà commencés.",
      completedCard: "Terminés",
      completedModules: "Modules que vous avez déjà terminés.",
      learningTime: "Temps d'apprentissage",
      learningTimeDescription: "Temps total estimé d'apprentissage actif pour ce cycle.",
      continueThisModule: "Continuer ce module",
      reviewThisModule: "Revoir ce module",
      continueStrengthening: "Continuer à renforcer",
      nextRecommendedModule: "Prochain module recommandé",
      progress: "Progression",
      highPriority: "priorité",
      recommendedRoadmap: "Roadmap recommandée",
      roadmapDescription: "Modules sélectionnés pour traiter vos écarts de compétences actuels.",
      startHere: "Commencer ici",
      optionalModules: "Modules optionnels",
      optionalModulesDescription: "Modules disponibles pour explorer au-delà de votre parcours recommandé actuel.",
      exploreModule: "Explorer le module",
      advancedLearningRecommendations: "Recommandations d'apprentissage avancé",
      advancedLearningDescription: "Votre assessment montre de bonnes performances sur l'ensemble des compétences IA évaluées.",
      introductory: "Introduction", core: "Fondamental", applied: "Appliqué", advanced: "Avancé",
      beginner: "Débutant", intermediate: "Intermédiaire",
      high: "Haute", mediumPriority: "Moyenne", low: "Faible",
      blended: "Mixte", video: "Vidéo", infographic: "Infographie",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        const [roadmapRes, modulesRes] = await Promise.all([
          apiFetch("/api/v1/roadmap"),
          apiFetch("/api/v1/modules"),
        ]);
        if (!roadmapRes || !modulesRes) return;
        const roadmapData = await roadmapRes.json().catch(() => ({}));
        const modulesData = await modulesRes.json().catch(() => ([]));
        if (roadmapRes.ok) {
          setRoadmapItems(Array.isArray(roadmapData?.items) ? roadmapData.items : []);
          setRoadmapProgress(Number(roadmapData?.roadmap_progress) || 0);
          setModulesCompleted(Number(roadmapData?.modules_completed) || 0);
          setModulesTotal(Number(roadmapData?.modules_total) || 0);
        }
        if (modulesRes.ok) setAllModules(Array.isArray(modulesData) ? modulesData : []);
      } catch (e) {
        setRoadmapItems([]);
        setAllModules([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const levelLabel = (level) => {
    const v = String(level || "").toLowerCase();
    if (v.includes("begin")) return t[lang].beginner;
    if (v.includes("inter")) return t[lang].intermediate;
    if (v.includes("adv")) return t[lang].advanced;
    return level || "—";
  };
  const priorityLabel = (priority) => {
    const v = String(priority || "").toLowerCase();
    if (v.includes("high")) return t[lang].high;
    if (v.includes("medium")) return t[lang].mediumPriority;
    if (v.includes("low")) return t[lang].low;
    return priority || "—";
  };
  const formatLabel = (format) => {
    const v = String(format || "").toLowerCase();
    if (v === "blended") return t[lang].blended;
    if (v === "video") return t[lang].video;
    if (v === "infographic") return t[lang].infographic;
    return format || "—";
  };
  const journeyStageLabel = (stage) => {
    const v = String(stage || "").toLowerCase();
    if (v === "introductory") return t[lang].introductory;
    if (v === "core") return t[lang].core;
    if (v === "applied") return t[lang].applied;
    if (v === "advanced") return t[lang].advanced;
    return stage || "—";
  };

  const renderSkillBadges = (module, badgeClass = "border-slate-200 bg-slate-50 text-slate-700") => {
    const skills = module.covered_skills?.length > 0
      ? module.covered_skills
      : [{ skill_name: module.skill }];
    return skills.map((s, si) => (
      <span key={si} className={`rounded-full border px-3 py-1 text-xs font-semibold ${badgeClass}`}>
        {s.skill_name}
      </span>
    ));
  };

  const modules = useMemo(() => {
    return roadmapItems.map((item, index) => {
      const fullModule = allModules.find((m) => m.id === item.module_id);
      const durationValue = fullModule?.estimated_duration_min || item.estimated_duration_min;
      return {
        id: item.module_id || fullModule?.id || index,
        moduleId: fullModule?.id || item.module_id || null,
        title: (lang === "fr" ? fullModule?.title_fr : fullModule?.title_en) || item.module_title || t[lang].untitledModule,
        skill: item.skill_name || "—",
        covered_skills: item.covered_skills || [],
        level: fullModule?.level || item.module_level || item.level || "—",
        duration: durationValue ? `${durationValue} ${t[lang].min}` : "—",
        format: fullModule?.format || item.format || "—",
        priority: item.priority || t[lang].mediumPriority,
        status: item.status || "not_started",
        description: (lang === "fr" ? fullModule?.description_fr : fullModule?.description_en) || item.module_description || `${t[lang].recommendedModuleFor} ${item.skill_name}.`,
        progress: item.progress_percent ?? (item.status === "completed" ? 100 : 0),
        journeyStage: fullModule?.journey_stage || "—",
        score: item.score ?? null,
      };
    });
  }, [roadmapItems, allModules, lang]);

  const mainModules = useMemo(() => modules.filter((m) => String(m.priority).toLowerCase() !== "low"), [modules]);
  const optionalModules = useMemo(() => modules.filter((m) => String(m.priority).toLowerCase() === "low"), [modules]);
  const isStrongProfile = modules.length > 0 && mainModules.length === 0;

  const overview = useMemo(() => {
    const src = isStrongProfile ? modules : mainModules;
    const totalMinutes = src.reduce((acc, m) => { const v = parseInt(m.duration, 10); return acc + (Number.isNaN(v) ? 0 : v); }, 0);
    return {
      recommended: src.length,
      inProgress: src.filter((m) => m.status === "in_progress").length,
      completed: src.filter((m) => m.status === "completed").length,
      learningTime: `${totalMinutes} ${t[lang].min}`,
    };
  }, [mainModules, modules, isStrongProfile, lang]);

  const featuredModule = useMemo(() => {
    if (isStrongProfile) return modules.find((m) => m.status !== "completed") || modules[0] || null;
    return mainModules.find((m) => m.status === "in_progress") || mainModules.find((m) => m.status === "not_started") || mainModules[0] || null;
  }, [mainModules, modules, isStrongProfile]);

  const hasAnyModules = modules.length > 0;
  const goToModule = (module) => { if (!module?.moduleId) return; navigate(`/learning/module/${module.moduleId}/units`); };

  const statusBadgeClass = (status) => {
    const v = String(status).toLowerCase();
    if (v.includes("complete")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (v.includes("progress")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-slate-200 bg-slate-50 text-slate-700";
  };
  const statusLabel = (status) => {
    const v = String(status).toLowerCase();
    if (v.includes("complete")) return t[lang].completed;
    if (v.includes("progress")) return t[lang].inProgress;
    return t[lang].notStarted;
  };
  const levelBadgeClass = (level) => {
    const v = String(level).toLowerCase();
    if (v.includes("begin")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (v.includes("inter")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-violet-200 bg-violet-50 text-violet-700";
  };
  const priorityBadgeClass = (priority) => {
    const v = String(priority).toLowerCase();
    if (v.includes("high")) return "border-red-200 bg-red-50 text-red-700";
    if (v.includes("medium")) return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-emerald-200 bg-emerald-50 text-emerald-700";
  };
  const actionLabel = (module) => {
    if (module.status === "completed") return t[lang].review;
    if (module.status === "in_progress") return t[lang].continue;
    return t[lang].start;
  };

  if (loading) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="text-sm text-slate-500">{t[lang].loadingLearningContent}</div>
        </section>
      </div>
    </div>
  );

  if (!hasAnyModules) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">
        <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
          <div className="text-base font-semibold text-euk-dark">{t[lang].noLearningModulesAvailable}</div>
          <div className="mt-2 text-sm text-slate-500">{t[lang].completeAssessment}</div>
          <button onClick={() => navigate("/assessment")}
            className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">
            {t[lang].startAssessment}
          </button>
        </section>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {t[lang].personalizedLearningExperience}
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{t[lang].learning}</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">{t[lang].learningIntro}</p>
            </div>
            <button onClick={() => navigate("/roadmap")}
              className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50">
              {t[lang].viewAIRoadmap}
            </button>
          </div>
        </section>

        <section className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {[
            { label: t[lang].suggestedModules, value: overview.recommended, desc: isStrongProfile ? t[lang].deepenStrongCapabilities : t[lang].roadmapDescription },
            { label: t[lang].inProgressCard, value: overview.inProgress, desc: t[lang].startedModules },
            { label: t[lang].completedCard, value: overview.completed, desc: t[lang].completedModules },
            { label: t[lang].learningTime, value: overview.learningTime, desc: t[lang].learningTimeDescription, primary: true },
          ].map(({ label, value, desc, primary }) => (
            <div key={label} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="text-sm font-medium text-slate-500">{label}</div>
              <div className={`mt-3 text-3xl font-bold tracking-tight ${primary ? "text-euk-primary" : "text-euk-dark"}`}>{value}</div>
              <div className="mt-3 text-sm text-slate-500">{desc}</div>
            </div>
          ))}
        </section>

        {featuredModule && (
          <section className="mt-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 inline-flex rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
              {isStrongProfile ? t[lang].continueStrengthening : featuredModule.status === "completed" ? t[lang].reviewThisModule : featuredModule.status === "in_progress" ? t[lang].continueThisModule : t[lang].nextRecommendedModule}
            </div>
            <h2 className="text-xl font-bold text-euk-dark md:text-2xl">{featuredModule.title}</h2>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              {renderSkillBadges(featuredModule)}
              <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(featuredModule.level)].join(" ")}>{levelLabel(featuredModule.level)}</span>
              <span className={["rounded-full border px-3 py-1 text-xs font-semibold", priorityBadgeClass(featuredModule.priority)].join(" ")}>{priorityLabel(featuredModule.priority)} {t[lang].highPriority}</span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{featuredModule.duration}</span>
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{formatLabel(featuredModule.format)}</span>
            </div>
            <p className="mt-4 text-sm leading-6 text-slate-600 md:text-base">{featuredModule.description}</p>
            <div className="mt-5">
              <div className="flex items-center justify-between text-sm font-medium text-slate-600">
                <span>{t[lang].progress}</span><span>{featuredModule.progress}%</span>
              </div>
              <div className="mt-2 h-2.5 w-full rounded-full bg-slate-100">
                <div className="h-2.5 rounded-full bg-euk-primary" style={{ width: `${featuredModule.progress}%` }} />
              </div>
            </div>
            <button onClick={() => goToModule(featuredModule)} className="mt-6 rounded-2xl bg-euk-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">
              {actionLabel(featuredModule)}
            </button>
          </section>
        )}

        {!isStrongProfile && (
          <>
            <section className="mt-8">
              <div className="mb-4">
                <h2 className="text-lg font-bold text-euk-dark">{t[lang].recommendedRoadmap}</h2>
                <p className="mt-1 text-sm text-slate-500">{t[lang].roadmapDescription}</p>
              </div>
              <div className="grid items-stretch gap-4 md:grid-cols-2 xl:grid-cols-3">
                {mainModules.map((module, index) => (
                  <div key={module.id} className="flex h-full flex-col rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="text-base font-bold leading-snug text-euk-dark">{module.title}</h3>
                      <span className={["rounded-full border px-3 py-1 text-xs font-semibold", statusBadgeClass(module.status)].join(" ")}>{statusLabel(module.status)}</span>
                    </div>
                    {index === 0 && <div className="mt-3 inline-flex w-fit rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">{t[lang].startHere}</div>}
                    <div className="mt-4 flex flex-wrap items-center gap-2">
                      {renderSkillBadges(module)}
                      <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(module.level)].join(" ")}>{levelLabel(module.level)}</span>
                      <span className={["rounded-full border px-3 py-1 text-xs font-semibold", priorityBadgeClass(module.priority)].join(" ")}>{priorityLabel(module.priority)}</span>
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{module.duration}</span>
                    </div>
                    <div className="mt-3 flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{journeyStageLabel(module.journeyStage)}</span>
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{formatLabel(module.format)}</span>
                    </div>
                    <p className="mt-4 text-sm leading-6 text-slate-500">{module.description}</p>
                    <button onClick={() => goToModule(module)} className="mt-auto w-full rounded-2xl bg-euk-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">
                      {actionLabel(module)}
                    </button>
                  </div>
                ))}
              </div>
            </section>

            {!!optionalModules.length && (
              <section className="mt-8">
                <div className="mb-4">
                  <h2 className="text-lg font-bold text-euk-dark">{t[lang].optionalModules}</h2>
                  <p className="mt-1 text-sm text-slate-500">{t[lang].optionalModulesDescription}</p>
                </div>
                <div className="grid items-stretch gap-4 md:grid-cols-2 xl:grid-cols-3">
                  {optionalModules.map((module) => (
                    <div key={module.id} className="flex h-full flex-col rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                      <div className="flex items-start justify-between gap-3">
                        <h3 className="text-base font-bold leading-snug text-euk-dark">{module.title}</h3>
                        <span className={["rounded-full border px-3 py-1 text-xs font-semibold", statusBadgeClass(module.status)].join(" ")}>{statusLabel(module.status)}</span>
                      </div>
                      <div className="mt-4 flex flex-wrap items-center gap-2">
                        {renderSkillBadges(module)}
                        <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(module.level)].join(" ")}>{levelLabel(module.level)}</span>
                        <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{module.duration}</span>
                      </div>
                      <p className="mt-4 text-sm leading-6 text-slate-500">{module.description}</p>
                      <button onClick={() => goToModule(module)} className="mt-auto w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50">
                        {t[lang].exploreModule}
                      </button>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}

        {isStrongProfile && (
          <section className="mt-8">
            <div className="mb-4">
              <h2 className="text-lg font-bold text-euk-dark">{t[lang].advancedLearningRecommendations}</h2>
              <p className="mt-1 text-sm text-slate-500">{t[lang].advancedLearningDescription}</p>
            </div>
            <div className="grid items-stretch gap-4 md:grid-cols-2 xl:grid-cols-3">
              {modules.map((module) => (
                <div key={module.id} className="flex h-full flex-col rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-base font-bold leading-snug text-euk-dark">{module.title}</h3>
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", statusBadgeClass(module.status)].join(" ")}>{statusLabel(module.status)}</span>
                  </div>
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    {renderSkillBadges(module)}
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(module.level)].join(" ")}>{levelLabel(module.level)}</span>
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">{module.duration}</span>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-slate-500">{module.description}</p>
                  <button onClick={() => goToModule(module)} className="mt-auto w-full rounded-2xl bg-euk-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">
                    {actionLabel(module)}
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}