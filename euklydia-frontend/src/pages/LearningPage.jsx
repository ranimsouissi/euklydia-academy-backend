import { useEffect, useMemo, useState } from "react";
import { useNavigate, useOutletContext, useLocation } from "react-router-dom";
import { apiFetch } from "../utils/api";

export default function LearningPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext();
  const lang = language || "en";

  const [roadmapItems, setRoadmapItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  const t = {
    en: {
      heroBadge: "Learning focus", title: "Learning",
      subtitle: "Make progress on your current module at your own pace.",
      viewRoadmap: "View AI Roadmap", loading: "Loading...",
      noModules: "No modules available",
      noModulesText: "Complete the diagnostic to generate your learning modules.",
      startDiagnostic: "Start diagnostic",
      heroCurrentFocus: "Your current focus",
      heroResume: "Continue this module", heroReview: "Review this module", heroStart: "Start this module",
      currentScore: "Current score", kpiBefore: "Today", kpiAfter: "After mastering", progress: "Progress",
      ctaStart: "Start the module →", ctaContinue: "Continue the module →", ctaReview: "Review the module →",
      otherModulesTitle: "Your other modules",
      otherModulesSubtitle: "Switch between modules as you progress.",
      openModule: "Open →",
      priorityHigh: "High priority", priorityMedium: "Medium priority", priorityLow: "Optional",
      statusCompleted: "Completed", statusInProgress: "In progress", statusNotStarted: "Not started",
      min: "min", skillLabel: "Skill", score: "Score",
    },
    fr: {
      heroBadge: "Focus apprentissage", title: "Apprentissage",
      subtitle: "Avancez sur votre module en cours à votre rythme.",
      viewRoadmap: "Voir la feuille de route IA", loading: "Chargement...",
      noModules: "Aucun module disponible",
      noModulesText: "Complétez le diagnostic pour générer vos modules d'apprentissage.",
      startDiagnostic: "Commencer le diagnostic",
      heroCurrentFocus: "VOTRE FOCUS ACTUEL",
      heroResume: "CONTINUER CE MODULE", heroReview: "REVOIR CE MODULE", heroStart: "VOTRE FOCUS ACTUEL",
      currentScore: "Score actuel", kpiBefore: "Aujourd'hui", kpiAfter: "Après maîtrise", progress: "Progression",
      ctaStart: "Démarrer le module →", ctaContinue: "Continuer le module →", ctaReview: "Revoir le module →",
      otherModulesTitle: "Vos autres modules",
      otherModulesSubtitle: "Passez d'un module à l'autre selon votre progression.",
      openModule: "Ouvrir →",
      priorityHigh: "Priorité haute", priorityMedium: "Priorité moyenne", priorityLow: "Optionnel",
      statusCompleted: "Terminé", statusInProgress: "En cours", statusNotStarted: "Non commencé",
      min: "min", skillLabel: "Compétence", score: "Score",
    },
  };

  const fetchRoadmap = async () => {
    try {
      const res = await apiFetch("/api/v1/roadmap");
      if (!res) return;
      const data = await res.json().catch(() => ({}));
      if (res.ok) setRoadmapItems(Array.isArray(data?.items) ? data.items : []);
    } catch { setRoadmapItems([]); }
    finally { setLoading(false); }
  };

  // Recharge à chaque fois que le learner revient sur /learning
  // (navigation SPA + retour onglet)
  useEffect(() => {
    setLoading(true);
    fetchRoadmap();
  }, [location.pathname]); // eslint-disable-line react-hooks/exhaustive-deps

  // Recharge aussi quand le learner revient d'un autre onglet
  useEffect(() => {
    const handleFocus = () => fetchRoadmap();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const priorityRank = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return 0; if (v === "MEDIUM") return 1; return 2; };
  const priorityLabel = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return t[lang].priorityHigh; if (v === "MEDIUM") return t[lang].priorityMedium; return t[lang].priorityLow; };
  const priorityClass = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return "border-red-200 bg-red-50 text-red-700"; if (v === "MEDIUM") return "border-amber-200 bg-amber-50 text-amber-700"; return "border-slate-200 bg-slate-50 text-slate-600"; };
  const statusLabel = s => { const v = String(s || "").toLowerCase(); if (v.includes("complete")) return t[lang].statusCompleted; if (v.includes("progress")) return t[lang].statusInProgress; return t[lang].statusNotStarted; };
  const statusClass = s => { const v = String(s || "").toLowerCase(); if (v.includes("complete")) return "border-emerald-200 bg-emerald-50 text-emerald-700"; if (v.includes("progress")) return "border-sky-200 bg-sky-50 text-sky-700"; return "border-slate-200 bg-slate-50 text-slate-600"; };
  const statusDot = s => { const v = String(s || "").toLowerCase(); if (v.includes("complete")) return "bg-emerald-500"; if (v.includes("progress")) return "bg-sky-500 animate-pulse"; return "bg-slate-300"; };
  const moduleTitle = m => lang === "fr" ? m.module_title_fr || m.module_title : m.module_title;
  const moduleDescription = m => lang === "fr" ? m.module_description_fr || m.module_description : m.module_description;
  const goToModule = id => { if (id) navigate(`/learning/module/${id}/units`); };

  // journey_stage helper — ex: "Cycle de vente — Qualification" → {cycle, focus}
  const parseStage = stage => {
    const parts = (stage || "").split(" — ");
    return { cycle: parts[0] || "", focus: parts[1] || "" };
  };

  // ── Hero module — FIX : trier les in_progress par priorité aussi ──
  const heroModule = useMemo(() => {
    if (!roadmapItems.length) return null;

    // 1. Module "in_progress" — le plus prioritaire
    const inProgress = [...roadmapItems]
      .filter(m => String(m.status).toLowerCase().includes("progress"))
      .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority));
    if (inProgress.length > 0) return inProgress[0];

    // 2. Non commencé — le plus prioritaire (HIGH → MEDIUM → LOW)
    const notStarted = [...roadmapItems]
      .filter(m => !String(m.status).toLowerCase().includes("complete"))
      .sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority));
    if (notStarted.length > 0) return notStarted[0];

    // 3. Fallback — premier module (tous terminés)
    return roadmapItems[0];
  }, [roadmapItems]); // eslint-disable-line react-hooks/exhaustive-deps

  const otherModules = useMemo(() => {
    if (!roadmapItems.length || !heroModule) return [];
    return [...roadmapItems]
      .filter(m => m.module_id !== heroModule.module_id)
      .sort((a, b) => {
        const pr = priorityRank(a.priority) - priorityRank(b.priority);
        if (pr !== 0) return pr;
        return (a.use_case_display_order || 0) - (b.use_case_display_order || 0);
      });
  }, [roadmapItems, heroModule]); // eslint-disable-line react-hooks/exhaustive-deps

  const heroCtaLabel = useMemo(() => {
    if (!heroModule) return "";
    const s = String(heroModule.status || "").toLowerCase();
    if (s.includes("complete")) return t[lang].ctaReview;
    if (s.includes("progress")) return t[lang].ctaContinue;
    return t[lang].ctaStart;
  }, [heroModule, lang]); // eslint-disable-line react-hooks/exhaustive-deps

  const heroBadgeLabel = useMemo(() => {
    if (!heroModule) return "";
    const s = String(heroModule.status || "").toLowerCase();
    if (s.includes("complete")) return t[lang].heroReview;
    if (s.includes("progress")) return t[lang].heroResume;
    return t[lang].heroCurrentFocus;
  }, [heroModule, lang]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-page">
        <section className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <div className="flex items-center justify-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
            <span className="text-sm text-slate-500">{t[lang].loading}</span>
          </div>
        </section>
      </div>
    </div>
  );

  if (!roadmapItems.length) return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-page">
        <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
          <div className="text-base font-semibold text-euk-dark">{t[lang].noModules}</div>
          <div className="mt-2 text-sm text-slate-500">{t[lang].noModulesText}</div>
          <button onClick={() => navigate("/diagnostic")} className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep">
            {t[lang].startDiagnostic}
          </button>
        </section>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-page">

        {/* ─── HERO PAGE ─── */}
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {t[lang].heroBadge}
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{t[lang].title}</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">{t[lang].subtitle}</p>
            </div>
            <button onClick={() => navigate("/roadmap")} className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50 shrink-0">
              {t[lang].viewRoadmap}
            </button>
          </div>
        </section>

        {/* ─── MODULE HERO ─── */}
        {heroModule && (() => {
          const { cycle, focus } = parseStage(heroModule.journey_stage);
          return (
            <section className="mt-6 overflow-hidden rounded-3xl border-2 border-euk-primary/30 bg-gradient-to-br from-euk-primary/5 to-white shadow-md">
              <div className="p-6 md:p-8">

                {/* Badge contextuel */}
                <div className="mb-3 inline-flex items-center rounded-full border border-euk-primary/30 bg-white px-3 py-1 text-xs font-bold uppercase tracking-wide text-euk-primary">
                  {heroBadgeLabel}
                </div>

                {/* Journey stage */}
                {cycle && (
                  <div className="mb-2 flex items-center gap-2">
                    <span className="inline-flex rounded-full border border-euk-primary/20 bg-euk-primary/5 px-2.5 py-0.5 text-xs font-semibold text-euk-primary">
                      {cycle}
                    </span>
                    {focus && <span className="text-xs text-slate-400">{focus}</span>}
                  </div>
                )}

                {/* Priorité + score */}
                <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
                  <span className={["rounded-full border px-2.5 py-0.5", priorityClass(heroModule.priority)].join(" ")}>
                    {priorityLabel(heroModule.priority)}
                  </span>
                  <span className="text-slate-400">·</span>
                  <span className="text-slate-500">{t[lang].score} : <span className="text-euk-primary">{heroModule.score}%</span></span>
                </div>

                {/* Titre */}
                <h2 className="mt-3 text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">
                  {moduleTitle(heroModule)}
                </h2>

                {/* Compétence */}
                {heroModule.skill_name && (
                  <div className="mt-1.5 text-sm text-slate-500">
                    {t[lang].skillLabel} : <span className="font-medium text-slate-700">{heroModule.skill_name}</span>
                  </div>
                )}

                {/* Métadonnées */}
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  {heroModule.estimated_duration_min && (
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-600">
                      {heroModule.estimated_duration_min} {t[lang].min}
                    </span>
                  )}
                  <span className={["rounded-full border px-3 py-1 text-xs font-semibold", statusClass(heroModule.status)].join(" ")}>
                    {statusLabel(heroModule.status)}
                  </span>
                </div>

                {/* Description */}
                {moduleDescription(heroModule) && (
                  <p className="mt-5 text-sm leading-6 text-slate-700 md:text-base md:leading-7">
                    {moduleDescription(heroModule)}
                  </p>
                )}

                {/* KPI Before / After */}
                {(heroModule.kpi_before || heroModule.kpi_after) && (
                  <div className="mt-6 grid gap-3 md:grid-cols-2">
                    <div className="rounded-2xl border border-slate-200 bg-white p-4">
                      <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{t[lang].kpiBefore}</div>
                      <div className="mt-2 text-sm font-medium leading-6 text-slate-700">{heroModule.kpi_before || "—"}</div>
                    </div>
                    <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                      <div className="text-xs font-semibold uppercase tracking-wide text-emerald-700">{t[lang].kpiAfter}</div>
                      <div className="mt-2 text-sm font-bold leading-6 text-emerald-900">{heroModule.kpi_after || "—"}</div>
                    </div>
                  </div>
                )}

                {/* Progression */}
                <div className="mt-6">
                  <div className="flex items-center justify-between text-sm font-medium text-slate-600">
                    <span>{t[lang].progress}</span>
                    <span className={heroModule.progress_percent === 100 ? "text-emerald-600 font-bold" : "text-euk-primary"}>
                      {heroModule.progress_percent === 100
                        ? (lang === "fr" ? "✓ Terminé" : "✓ Completed")
                        : `${heroModule.progress_percent || 0}%`}
                    </span>
                  </div>
                  <div className="mt-2 h-2.5 w-full rounded-full bg-slate-100">
                    <div className={`h-2.5 rounded-full transition-all ${heroModule.progress_percent === 100 ? "bg-emerald-500" : "bg-euk-primary"}`}
                      style={{ width: `${heroModule.progress_percent || 0}%` }} />
                  </div>
                </div>

                {/* CTA */}
                <button
                  onClick={() => goToModule(heroModule.module_id)}
                  className="mt-7 w-full rounded-2xl bg-euk-primary px-6 py-4 text-base font-bold text-white shadow-lg shadow-euk-primary/20 transition hover:-translate-y-0.5 hover:bg-euk-deep hover:shadow-xl md:w-auto md:min-w-[280px]"
                >
                  {heroCtaLabel}
                </button>
              </div>
            </section>
          );
        })()}

        {/* ─── AUTRES MODULES ─── */}
        {otherModules.length > 0 && (
          <section className="mt-10 mb-10">
            <div className="mb-5">
              <h2 className="text-lg font-bold text-euk-dark">{t[lang].otherModulesTitle}</h2>
              <p className="mt-1 text-sm text-slate-500">{t[lang].otherModulesSubtitle}</p>
            </div>
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {otherModules.map(m => {
                const { cycle, focus } = parseStage(m.journey_stage);
                return (
                  <article key={m.module_id} className="flex h-full flex-col rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                    {/* Header */}
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <span className={["h-2.5 w-2.5 shrink-0 rounded-full", statusDot(m.status)].join(" ")} />
                        <span className={["rounded-full border px-2.5 py-0.5 text-xs font-semibold", priorityClass(m.priority)].join(" ")}>
                          {priorityLabel(m.priority)}
                        </span>
                      </div>
                      <span className={`text-xs font-semibold ${
                        String(m.status).toLowerCase().includes("complete")
                          ? "text-emerald-600"
                          : "text-euk-primary"
                      }`}>
                        {String(m.status).toLowerCase().includes("complete")
                          ? "✓"
                          : `${m.score}%`}
                      </span>
                    </div>

                    {/* Journey stage — remplace Fondation/Pratique/Expert */}
                    {cycle && (
                      <div className="mt-2 flex items-center gap-1.5">
                        <span className="text-xs font-semibold text-slate-500">{cycle}</span>
                        {focus && <span className="text-xs text-slate-400">— {focus}</span>}
                      </div>
                    )}

                    {/* Titre */}
                    <h3 className="mt-2 text-base font-bold leading-snug text-euk-dark">{moduleTitle(m)}</h3>

                    {/* Compétence */}
                    {m.skill_name && <div className="mt-1 text-xs text-slate-500">{m.skill_name}</div>}

                    {/* Durée */}
                    {m.estimated_duration_min && (
                      <div className="mt-3">
                        <span className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs font-semibold text-slate-600">
                          {m.estimated_duration_min} {t[lang].min}
                        </span>
                      </div>
                    )}
                    {/* Barre de progression mini */}
                    {(m.progress_percent || 0) > 0 && (
                      <div className="mt-3">
                        <div className="h-1.5 w-full rounded-full bg-slate-100">
                          <div
                            className={`h-1.5 rounded-full transition-all ${m.progress_percent === 100 ? "bg-emerald-500" : "bg-euk-primary"}`}
                            style={{ width: `${m.progress_percent}%` }}
                          />
                        </div>
                      </div>
                    )}

                    <div className="flex-1" />

                    <button
                      onClick={() => goToModule(m.module_id)}
                      className="mt-4 w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
                    >
                      {t[lang].openModule}
                    </button>
                  </article>
                );
              })}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}