import { useMemo, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import ConfirmModal from "../components/ConfirmModal";
import { apiFetch } from "../utils/api";
import RetakeDiagnosticBtn from "../components/RetakeDiagnosticBtn";

export default function AIRoadmapPage() {
  const navigate = useNavigate();
  const lang = "fr";

  const { data: roadmapData, loading, refetch } = useApi("/api/v1/roadmap");
  const [showConfirm, setShowConfirm] = useState(false);
  const [diagStatus, setDiagStatus] = useState(null);

  useEffect(() => {
    const handleFocus = () => refetch();
    window.addEventListener("focus", handleFocus);
    return () => window.removeEventListener("focus", handleFocus);
  }, [refetch]);

  // Charger le status diagnostic pour savoir si on peut refaire
  useEffect(() => {
    (async () => {
      try {
        const res = await apiFetch("/api/v1/diagnostic/status");
        if (res?.ok) setDiagStatus(await res.json());
      } catch { /* non-blocking */ }
    })();
  }, []);

  const roadmapItems     = roadmapData?.items || [];
  const roadmapProgress  = roadmapData?.roadmap_progress || 0;
  const modulesCompleted = roadmapData?.modules_completed || 0;
  const modulesTotal     = roadmapData?.modules_total || 0;
  const totalDurationMin = roadmapData?.total_duration_min || 0;

  // Peut refaire le diagnostic si 90j écoulés OU tous modules terminés
  const canRetake = diagStatus?.recommended === true || roadmapProgress === 100;

  const t = {
    fr: {
      badge:            "Plan de développement personnalisé",
      title:            "Feuille de route IA",
      subtitle:         "Vos 3 use cases business à maîtriser avec l'IA — à votre rythme.",
      retakeDiagnostic: "Refaire le diagnostic",
      confirmTitle:     "Refaire le diagnostic ?",
      confirmMessage:   "Vos scores actuels seront remplacés par les nouveaux résultats. Cette action est irréversible.",
      confirmLabel:     "Oui, refaire",
      cancelLabel:      "Annuler",
      loading:          "Chargement de la feuille de route...",
      noRoadmap:        "Aucune feuille de route disponible",
      noRoadmapText:    "Complétez le diagnostic pour générer votre feuille de route personnalisée.",
      startDiagnostic:  "Commencer le diagnostic",
      allCompleted:     "Tous les use cases sont maîtrisés ! Vous pouvez refaire le diagnostic.",
      progression:      "Progression",
      modulesLabel:     "modules terminés",
      useCases:         "Use cases",
      of3:              "sur 3",
      duration:         "Durée totale",
      hours:            "heures",
      over90:           "sur 90 jours",
      skill:            "Compétence",
      score:            "Score",
      min:              "min",
      kpiBefore:        "Avant",
      kpiAfter:         "Après",
      completed:        "Terminé",
      inProgress:       "En cours",
      notStarted:       "Non commencé",
      high:             "Priorité haute",
      medium:           "Priorité moyenne",
      low:              "Optionnel",
      yourUseCases:     "Vos 3 use cases",
      yourUseCasesDesc: "Chaque module traite un problème business concret avec des prompts IA, des workflows et une mission sur vos vraies données.",
      days:             ["Jours 1-30", "Jours 31-60", "Jours 61-90"],
      daysTooltip:      "Séquence recommandée — commencez par la priorité la plus haute",
    },
  };
  const tx = t[lang];

  const statusLabel = s => {
    const v = String(s || "").toLowerCase();
    if (v.includes("complete")) return tx.completed;
    if (v.includes("progress")) return tx.inProgress;
    return tx.notStarted;
  };
  const statusColor = s => {
    const v = String(s || "").toLowerCase();
    if (v.includes("complete")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (v.includes("progress")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-slate-200 bg-slate-50 text-slate-600";
  };
  const statusDot = s => {
    const v = String(s || "").toLowerCase();
    if (v.includes("complete")) return "bg-emerald-500";
    if (v.includes("progress")) return "bg-sky-500 animate-pulse";
    return "bg-slate-300";
  };
  const priorityLabel = p => {
    const v = String(p).toUpperCase();
    if (v === "HIGH")   return tx.high;
    if (v === "MEDIUM") return tx.medium;
    return tx.low;
  };
  const priorityColor = p => {
    const v = String(p).toUpperCase();
    if (v === "HIGH")   return "border-red-200 bg-red-50 text-red-700";
    if (v === "MEDIUM") return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-slate-200 bg-slate-50 text-slate-500";
  };
  const moduleTitle = m => m.module_title_fr || m.module_title;

  const useCasesMastered = useMemo(
    () => roadmapItems.filter(m => String(m.status).toLowerCase().includes("complete")).length,
    [roadmapItems]
  );
  const totalHours = useMemo(
    () => Math.round((totalDurationMin / 60) * 10) / 10,
    [totalDurationMin]
  );

  // Trier HIGH → MEDIUM → LOW puis use_case_display_order
  const sortedItems = useMemo(() => {
    const rank = p => { const v = String(p).toUpperCase(); if (v === "HIGH") return 0; if (v === "MEDIUM") return 1; return 2; };
    return [...roadmapItems].sort((a, b) => {
      const pr = rank(a.priority) - rank(b.priority);
      if (pr !== 0) return pr;
      return (a.use_case_display_order || 0) - (b.use_case_display_order || 0);
    });
  }, [roadmapItems]);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-page">

        {/* ─── HERO ─── */}
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {tx.badge}
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{tx.title}</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">{tx.subtitle}</p>
            </div>
            <RetakeDiagnosticBtn
              canRetake={canRetake}
              nextAllowedAt={diagStatus?.next_allowed_at}
              onClick={() => setShowConfirm(true)}
              tx={tx}
              lang={lang}
            />
          </div>
        </section>

        {/* ─── LOADING ─── */}
        {loading && (
          <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
            <div className="flex items-center justify-center gap-3">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-euk-primary border-t-transparent" />
              <span className="text-sm text-slate-500">{tx.loading}</span>
            </div>
          </section>
        )}

        {/* ─── EMPTY STATE ─── */}
        {!loading && !roadmapItems.length && (
          <section className="mt-6 rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
            <div className="text-base font-semibold text-euk-dark">{tx.noRoadmap}</div>
            <div className="mt-2 text-sm text-slate-500">{tx.noRoadmapText}</div>
            <button
              onClick={() => navigate("/diagnostic")}
              className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep"
            >
              {tx.startDiagnostic}
            </button>
          </section>
        )}

        {!loading && !!roadmapItems.length && (
          <>
            {/* ─── Bandeau tous terminés ─── */}
            {roadmapProgress === 100 && (
              <section className="mt-6 rounded-3xl border border-emerald-200 bg-emerald-50 p-5 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <span className="text-sm font-semibold text-emerald-900">{tx.allCompleted}</span>
                  <button
                    onClick={() => setShowConfirm(true)}
                    className="rounded-2xl bg-emerald-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:opacity-90"
                  >
                    {tx.retakeDiagnostic}
                  </button>
                </div>
              </section>
            )}

            {/* ─── KPI CARDS ─── */}
            <section className="mt-6 grid gap-4 md:grid-cols-3">
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{tx.progression}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-primary">{roadmapProgress}%</div>
                <div className="mt-4 h-2.5 w-full rounded-full bg-slate-100">
                  <div className="h-2.5 rounded-full bg-euk-primary transition-all" style={{ width: `${roadmapProgress}%` }} />
                </div>
                <div className="mt-3 text-sm text-slate-500">{modulesCompleted} / {modulesTotal} {tx.modulesLabel}</div>
              </div>
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{tx.useCases}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">{useCasesMastered} / 3</div>
                <div className="mt-3 inline-flex rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                  {tx.of3} use cases
                </div>
              </div>
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="text-sm font-medium text-slate-500">{tx.duration}</div>
                <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">~{totalHours} {tx.hours}</div>
                <div className="mt-3 text-sm text-slate-500">{tx.over90}</div>
              </div>
            </section>

            {/* ─── USE CASES ─── */}
            <section className="mt-10 mb-10">
              <div className="mb-6">
                <h2 className="text-xl font-bold text-euk-dark md:text-2xl">{tx.yourUseCases}</h2>
                <p className="mt-1 text-sm text-slate-500 max-w-3xl">{tx.yourUseCasesDesc}</p>
              </div>
              <div className="grid gap-5 md:grid-cols-3">
                {sortedItems.map((m, idx) => (
                  <UseCaseCard
                    key={m.module_id}
                    item={m}
                    index={idx}
                    tx={tx}
                    lang={lang}
                    moduleTitle={moduleTitle}
                    statusLabel={statusLabel}
                    statusColor={statusColor}
                    statusDot={statusDot}
                    priorityLabel={priorityLabel}
                    priorityColor={priorityColor}
                  />
                ))}
              </div>
            </section>
          </>
        )}
      </div>

      {showConfirm && (
        <ConfirmModal
          title={tx.confirmTitle}
          message={tx.confirmMessage}
          confirmLabel={tx.confirmLabel}
          cancelLabel={tx.cancelLabel}
          confirmClass="bg-rose-500 hover:bg-rose-600"
          onConfirm={() => { setShowConfirm(false); navigate("/diagnostic"); }}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
}

function UseCaseCard({ item, index, tx, lang, moduleTitle, statusLabel, statusColor, statusDot, priorityLabel, priorityColor }) {
  const accents = [
    { border: "border-emerald-200", bg: "bg-emerald-50", text: "text-emerald-700", num: "bg-emerald-500", dayBorder: "border-emerald-200", dayBg: "bg-emerald-50", dayText: "text-emerald-700" },
    { border: "border-sky-200",     bg: "bg-sky-50",     text: "text-sky-700",     num: "bg-sky-500",     dayBorder: "border-sky-200",     dayBg: "bg-sky-50",     dayText: "text-sky-700"     },
    { border: "border-violet-200",  bg: "bg-violet-50",  text: "text-violet-700",  num: "bg-violet-500",  dayBorder: "border-violet-200",  dayBg: "bg-violet-50",  dayText: "text-violet-700"  },
  ];
  const accent = accents[index % 3];
  const stageParts = (item.journey_stage || "").split(" — ");
  const stageCycle = stageParts[0] || "";
  const stageFocus = stageParts[1] || "";
  const dayLabel   = tx.days[index] || "";

  return (
    <article className="flex flex-col rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">

      {/* Header : numéro + jours + journey_stage */}
      <div className="flex items-start gap-3 mb-4">
        <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold text-white ${accent.num}`}>
          {index + 1}
        </div>
        <div className="flex flex-col gap-1">
          {/* Badge jours */}
          {dayLabel && (
            <span className={`inline-flex rounded-full border px-2.5 py-0.5 text-xs font-semibold ${accent.dayBorder} ${accent.dayBg} ${accent.dayText}`}>
              {dayLabel}
            </span>
          )}
          {/* Cycle */}
          {stageCycle && (
            <span className="text-xs font-semibold text-slate-500">{stageCycle}</span>
          )}
          {/* Focus */}
          {stageFocus && (
            <span className="text-xs text-slate-400">{stageFocus}</span>
          )}
        </div>
      </div>

      {/* Titre module */}
      <h3 className="text-base font-bold leading-snug text-euk-dark mb-3">
        {moduleTitle(item)}
      </h3>

      {/* Status + Priority */}
      <div className="flex flex-wrap gap-2 mb-4">
        <span className={`flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold ${statusColor(item.status)}`}>
          <span className={`h-1.5 w-1.5 rounded-full ${statusDot(item.status)}`} />
          {statusLabel(item.status)}
        </span>
        <span className={`rounded-full border px-2.5 py-0.5 text-xs font-semibold ${priorityColor(item.priority)}`}>
          {priorityLabel(item.priority)}
        </span>
      </div>

      {/* Skill + Score */}
      <div className="mb-4">
        {item.skill_name && (
          <div className="text-xs text-slate-500 mb-2">
            {tx.skill} : <span className="font-medium text-slate-700">{item.skill_name}</span>
          </div>
        )}
        <div className="flex items-center gap-2">
          <div className="h-2 flex-1 rounded-full bg-slate-100">
            <div className="h-2 rounded-full bg-euk-primary transition-all" style={{ width: `${item.score || 0}%` }} />
          </div>
          <span className="text-xs font-semibold text-euk-primary">{item.score}%</span>
        </div>
      </div>

      {/* KPI before / after */}
      {(item.kpi_before || item.kpi_after) && (
        <div className="mt-auto rounded-2xl border border-slate-100 bg-slate-50 p-3 space-y-1.5">
          {item.kpi_before && (
            <div className="flex gap-2 text-xs">
              <span className="font-semibold text-slate-400 shrink-0">{tx.kpiBefore} :</span>
              <span className="text-slate-600">{item.kpi_before}</span>
            </div>
          )}
          {item.kpi_after && (
            <div className="flex gap-2 text-xs">
              <span className="font-semibold text-emerald-600 shrink-0">{tx.kpiAfter} :</span>
              <span className="text-emerald-700 font-medium">{item.kpi_after}</span>
            </div>
          )}
        </div>
      )}

      {/* Durée */}
      {item.estimated_duration_min && (
        <div className="mt-3 text-xs text-slate-400 text-right">
          {item.estimated_duration_min} {tx.min}
        </div>
      )}
    </article>
  );
}