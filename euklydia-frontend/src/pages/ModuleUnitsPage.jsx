import { useEffect, useState } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";

export default function ModuleUnitsPage() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const { language } = useOutletContext();

  const [moduleData, setModuleData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [openUnit, setOpenUnit] = useState(null);

  const lang = language || "fr";

  const t = {
    en: {
      loading: "Loading module...",
      back: "Back to Learning",
      notFound: "Module not found",
      notFoundDesc: "This module could not be loaded.",
      units: "Units",
      lessons: "lessons",
      min: "min",
      beginner: "Beginner",
      intermediate: "Intermediate",
      advanced: "Advanced",
      foundation: "Foundation",
      practice: "Practice",
      expert: "Expert",
      startLesson: "Start",
      continueLesson: "Continue",
      locked: "Locked",
      video: "Video",
      quiz: "Quiz",
      exercise: "Exercise",
      tutorial: "Tutorial",
      case_study: "Case Study",
      forum_discussion: "Forum",
      prompt_practice: "Prompt Practice",
      difficulty: "Level",
      duration: "Duration",
      moduleOverview: "Module Overview",
      yourProgress: "Your progress",
      totalLessons: "lessons",
      totalUnits: "units",
      completed: "Completed",
      inProgress: "In progress",
      notStarted: "Not started",
      lessonsCompleted: "lessons completed",
    },
    fr: {
      loading: "Chargement du module...",
      back: "Retour apprentissage",
      notFound: "Module introuvable",
      notFoundDesc: "Ce module n'a pas pu être chargé.",
      units: "Unités",
      lessons: "leçons",
      min: "min",
      beginner: "Débutant",
      intermediate: "Intermédiaire",
      advanced: "Avancé",
      foundation: "Fondations",
      practice: "Pratique",
      expert: "Expert",
      startLesson: "Démarrer",
      continueLesson: "Continuer",
      locked: "Verrouillé",
      video: "Vidéo",
      quiz: "Quiz",
      exercise: "Exercice",
      tutorial: "Tutoriel",
      case_study: "Cas pratique",
      forum_discussion: "Forum",
      prompt_practice: "Prompts",
      difficulty: "Niveau",
      duration: "Durée",
      moduleOverview: "Aperçu du module",
      yourProgress: "Votre progression",
      totalLessons: "leçons",
      totalUnits: "unités",
      completed: "Terminé",
      inProgress: "En cours",
      notStarted: "Non commencé",
      lessonsCompleted: "leçons complétées",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await apiFetch(`/api/v1/modules/${moduleId}/full`);
        if (!res) return;
        if (!res.ok) { setError(t[lang].notFoundDesc); return; }
        const data = await res.json();
        setModuleData(data);
        if (data.units?.length > 0) setOpenUnit(data.units[0].id);
      } catch {
        setError(t[lang].notFoundDesc);
      } finally {
        setLoading(false);
      }
    })();
  }, [moduleId, lang]);

  const levelLabel = (level) => {
    const v = String(level || "").toLowerCase();
    if (v.includes("begin")) return t[lang].beginner;
    if (v.includes("inter")) return t[lang].intermediate;
    if (v.includes("adv")) return t[lang].advanced;
    return level || "—";
  };

  const stageLabel = (stage) => {
    const v = String(stage || "").toLowerCase();
    if (v === "foundation") return t[lang].foundation;
    if (v === "practice") return t[lang].practice;
    if (v === "expert") return t[lang].expert;
    return stage || "—";
  };

  const stageBadge = (stage) => {
    const v = String(stage || "").toLowerCase();
    if (v === "foundation") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (v === "practice") return "border-sky-200 bg-sky-50 text-sky-700";
    if (v === "expert") return "border-violet-200 bg-violet-50 text-violet-700";
    return "border-slate-200 bg-slate-50 text-slate-700";
  };

  const statusBadge = (status) => {
    if (status === "completed") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (status === "in_progress") return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-slate-200 bg-slate-50 text-slate-600";
  };

  const statusLabel = (status) => {
    if (status === "completed") return t[lang].completed;
    if (status === "in_progress") return t[lang].inProgress;
    return t[lang].notStarted;
  };

  const formatIcon = (format) => {
    const icons = {
      video: "▶",
      quiz: "✦",
      exercise: "✎",
      tutorial: "◈",
      case_study: "◉",
      forum_discussion: "◎",
      prompt_practice: "◆",
    };
    return icons[format] || "•";
  };

  const formatLabel = (format) => t[lang][format] || format;

  const formatColor = (format) => {
    const colors = {
      video: "text-sky-600 bg-sky-50 border-sky-200",
      quiz: "text-violet-600 bg-violet-50 border-violet-200",
      exercise: "text-amber-600 bg-amber-50 border-amber-200",
      tutorial: "text-teal-600 bg-teal-50 border-teal-200",
      case_study: "text-rose-600 bg-rose-50 border-rose-200",
      forum_discussion: "text-indigo-600 bg-indigo-50 border-indigo-200",
      prompt_practice: "text-orange-600 bg-orange-50 border-orange-200",
    };
    return colors[format] || "text-slate-600 bg-slate-50 border-slate-200";
  };

  const difficultyDots = (level) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span
        key={i}
        className={`inline-block h-1.5 w-1.5 rounded-full ${
          i < level ? "bg-euk-primary" : "bg-slate-200"
        }`}
      />
    ));
  };

  const totalLessons = moduleData?.units?.reduce(
    (acc, u) => acc + (u.lessons?.length || 0), 0
  ) || 0;

  const completedLessons = moduleData?.units?.reduce(
    (acc, u) => acc + (u.lessons?.filter(l => l.is_completed)?.length || 0), 0
  ) || 0;

  const totalDuration = moduleData?.units?.reduce(
    (acc, u) => acc + (u.estimated_duration_min || 0), 0
  ) || 0;

  const progressPercent = moduleData?.progress_percent || 0;
  const moduleStatus = moduleData?.module_status || "not_started";

  if (loading) {
    return (
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
  }

  if (!moduleData || error) {
    return (
      <div className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-4xl p-6">
          <button
            onClick={() => navigate("/learning")}
            className="mb-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
          >
            ← {t[lang].back}
          </button>
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <h1 className="text-xl font-bold text-euk-dark">{t[lang].notFound}</h1>
            <p className="mt-2 text-sm text-slate-500">{error || t[lang].notFoundDesc}</p>
          </div>
        </div>
      </div>
    );
  }

  const title = lang === "fr"
    ? moduleData.title_fr || moduleData.title_en
    : moduleData.title_en || moduleData.title_fr;

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-4xl p-6">

        {/* Back */}
        <button
          onClick={() => navigate("/learning")}
          className="mb-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
        >
          ← {t[lang].back}
        </button>

        {/* Header */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${stageBadge(moduleData.journey_stage)}`}>
              {stageLabel(moduleData.journey_stage)}
            </span>
            <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">
              {levelLabel(moduleData.level)}
            </span>
            <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">
              {moduleData.role}
            </span>
            {/* ✅ Badge statut du module */}
            <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${statusBadge(moduleStatus)}`}>
              {statusLabel(moduleStatus)}
            </span>
          </div>

          <h1 className="mt-4 text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">
            {title}
          </h1>

          {/* Stats */}
          <div className="mt-5 grid grid-cols-3 gap-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">
                {moduleData.units?.length || 0}
              </div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].totalUnits}</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">{totalLessons}</div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].totalLessons}</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-center">
              <div className="text-xl font-bold text-euk-primary">{totalDuration}</div>
              <div className="mt-0.5 text-xs text-slate-500">{t[lang].min}</div>
            </div>
          </div>

          {/* ✅ Barre de progression */}
          <div className="mt-5">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-slate-500">{t[lang].yourProgress}</span>
              <span className="font-semibold text-euk-primary">
                {completedLessons}/{totalLessons} {t[lang].lessonsCompleted} — {progressPercent}%
              </span>
            </div>
            <div className="h-2.5 w-full rounded-full bg-slate-100">
              <div
                className="h-2.5 rounded-full bg-euk-primary transition-all duration-500"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </section>

        {/* Units */}
        <div className="mt-6 space-y-3">
          {moduleData.units?.map((unit, uIdx) => {
            const isOpen = openUnit === unit.id;
            const unitTitle = lang === "fr"
              ? unit.title_fr || unit.title_en
              : unit.title_en || unit.title_fr;

            const unitCompletedCount = unit.lessons?.filter(l => l.is_completed)?.length || 0;
            const unitTotal = unit.lessons?.length || 0;
            const unitDone = unitCompletedCount === unitTotal && unitTotal > 0;

            return (
              <section
                key={unit.id}
                className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
              >
                {/* Unit Header */}
                <button
                  onClick={() => setOpenUnit(isOpen ? null : unit.id)}
                  className="flex w-full items-center gap-4 p-5 text-left transition hover:bg-slate-50"
                >
                  {/* ✅ Numéro avec check si unité complète */}
                  <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl text-sm font-bold text-white ${
                    unitDone ? "bg-emerald-500" : "bg-euk-primary"
                  }`}>
                    {unitDone ? "✓" : uIdx + 1}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="text-base font-bold text-euk-dark">{unitTitle}</h2>
                    </div>
                    <div className="mt-1.5 flex flex-wrap items-center gap-3 text-xs text-slate-500">
                      <span>{unit.lessons?.length || 0} {t[lang].lessons}</span>
                      {unit.estimated_duration_min && (
                        <span>{unit.estimated_duration_min} {t[lang].min}</span>
                      )}
                      {/* ✅ Progression de l'unité */}
                      {unitCompletedCount > 0 && (
                        <span className="text-emerald-600 font-semibold">
                          {unitCompletedCount}/{unitTotal} complétées
                        </span>
                      )}
                    </div>
                  </div>

                  <div className={`shrink-0 text-slate-400 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}>
                    ▼
                  </div>
                </button>

                {/* Lessons */}
                {isOpen && (
                  <div className="border-t border-slate-100 px-5 pb-4">
                    <div className="mt-4 space-y-2">
                      {unit.lessons?.map((lesson, lIdx) => {
                        const lessonTitle = lang === "fr"
                          ? lesson.title_fr || lesson.title_en
                          : lesson.title_en || lesson.title_fr;

                        return (
                          <button
                            key={lesson.id}
                            onClick={() =>
                              navigate(
                                `/learning/module/${moduleId}/units/${unit.id}/lessons/${lesson.id}`
                              )
                            }
                            className={`group flex w-full items-center gap-4 rounded-2xl border p-4 text-left transition ${
                              lesson.is_completed
                                ? "border-emerald-100 bg-emerald-50/50 hover:border-emerald-200"
                                : "border-slate-100 bg-slate-50 hover:border-euk-primary/30 hover:bg-euk-primary/5"
                            }`}
                          >
                            {/* ✅ Numéro ou check */}
                            <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold transition ${
                              lesson.is_completed
                                ? "bg-emerald-500 text-white"
                                : "border border-slate-200 bg-white text-slate-500 group-hover:border-euk-primary/40 group-hover:text-euk-primary"
                            }`}>
                              {lesson.is_completed ? "✓" : lIdx + 1}
                            </div>

                            <div className="flex-1 min-w-0">
                              <div className="flex flex-wrap items-center gap-2">
                                <span className={`text-sm font-semibold leading-snug ${
                                  lesson.is_completed ? "text-emerald-800" : "text-euk-dark"
                                }`}>
                                  {lessonTitle}
                                </span>
                                {/* ✅ Badge complétée */}
                                {lesson.is_completed && (
                                  <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">
                                    ✓ {t[lang].completed}
                                  </span>
                                )}
                              </div>

                              {/* Activities tags */}
                              <div className="mt-2 flex flex-wrap items-center gap-1.5">
                                {lesson.activities?.map((act) => (
                                  <span
                                    key={act.id}
                                    className={`inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium ${formatColor(act.type)}`}
                                  >
                                    <span>{formatIcon(act.type)}</span>
                                    <span>{formatLabel(act.type)}</span>
                                    {act.is_assessed && (
                                      <span className="ml-0.5 text-xs opacity-60">★</span>
                                    )}
                                  </span>
                                ))}
                              </div>
                            </div>

                            {/* Right side */}
                            <div className="shrink-0 flex flex-col items-end gap-2">
                              {lesson.estimated_duration_min && (
                                <span className="text-xs text-slate-400">
                                  {lesson.estimated_duration_min} {t[lang].min}
                                </span>
                              )}
                              <div className="flex items-center gap-1">
                                {difficultyDots(lesson.difficulty_level || 1)}
                              </div>
                              {!lesson.is_completed && (
                                <span className="rounded-xl bg-euk-primary px-3 py-1 text-xs font-semibold text-white opacity-0 transition group-hover:opacity-100">
                                  {t[lang].startLesson} →
                                </span>
                              )}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )}
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}