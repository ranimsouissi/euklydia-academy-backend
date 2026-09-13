import { useState } from "react";
import { apiFetch } from "../utils/api";

export default function LearnerProgressDashboard({ lang }) {
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

    {/* ══ SCORE GLOBAL DE MAÎTRISE ══ */}
    {(() => {
      const withMastery = modulesWithProgress.filter(m => m.mastery_score != null);
      const avgMastery = withMastery.length > 0
        ? Math.round(withMastery.reduce((sum, m) => sum + (m.mastery_score * 100), 0) / withMastery.length)
        : 0;
      const level = avgMastery >= 75 ? "Avancé" : avgMastery >= 50 ? "Intermédiaire" : "Novice";
      const levelColor = avgMastery >= 75 ? "text-emerald-700" : avgMastery >= 50 ? "text-amber-700" : "text-slate-600";
      const barColor = avgMastery >= 75 ? "bg-emerald-500" : avgMastery >= 50 ? "bg-amber-400" : "bg-euk-primary";
      const completedCount = modulesWithProgress.filter(m => m.status === "completed").length;

      return (
        <div className="rounded-3xl border border-euk-primary/20 bg-gradient-to-br from-euk-primary/5 to-white p-6 shadow-sm">
          <h3 className="text-base font-bold text-euk-dark mb-1">🏆 Score global de maîtrise</h3>
          <p className="text-xs text-slate-500 mb-5">
            Synthèse de votre progression sur l'ensemble des modules commencés.
          </p>
          <div className="grid grid-cols-3 gap-3 mb-5">
            <div className="rounded-2xl border border-slate-100 bg-white p-4 text-center shadow-sm">
              <div className={`text-3xl font-bold ${levelColor}`}>{avgMastery}%</div>
              <div className="mt-1 text-xs text-slate-500">Maîtrise moyenne</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-white p-4 text-center shadow-sm">
              <div className={`text-lg font-bold ${levelColor}`}>{level}</div>
              <div className="mt-1 text-xs text-slate-500">Niveau global</div>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-white p-4 text-center shadow-sm">
              <div className="text-3xl font-bold text-euk-primary">{completedCount}</div>
              <div className="mt-1 text-xs text-slate-500">
                Module{completedCount > 1 ? "s" : ""} complété{completedCount > 1 ? "s" : ""}
              </div>
            </div>
          </div>
          <div>
            <div className="flex justify-between text-xs text-slate-500 mb-1.5">
              <span>Novice</span>
              <span>Intermédiaire</span>
              <span>Avancé</span>
            </div>
            <div className="h-3 w-full rounded-full bg-slate-100">
              <div
                className={`h-3 rounded-full transition-all duration-700 ${barColor}`}
                style={{ width: `${avgMastery}%` }}
              />
            </div>
            {withMastery.length === 0 && (
              <p className="mt-2 text-xs text-slate-400 text-center">
                Soumettez votre première Execution Task pour calculer votre score.
              </p>
            )}
          </div>
        </div>
      );
    })()}

    {/* Mastery Heatmap */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-base font-bold text-euk-dark mb-1">Mastery Heatmap</h3>
            <p className="text-xs text-slate-500 mb-4">
              {lang === "fr" ? "Progression par section pour chaque module commencé." : "Progress by section for each started module."}
            </p>
            <div className="space-y-4">
              {modulesWithProgress.map((m, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-euk-dark truncate max-w-xs">
                      {m.module_title_fr || m.module_title || m.title_fr}
                    </span>
                    <span className={`rounded-full border px-2 py-0.5 text-xs font-semibold
                      ${m.status === "completed" ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : m.status === "in_progress" ? "border-sky-200 bg-sky-50 text-sky-700"
                        : "border-slate-200 bg-slate-50 text-slate-500"}`}>
                      {m.status === "completed" ? "✓ Terminé" : m.status === "in_progress" ? "En cours" : "Non commencé"}
                    </span>
                  </div>
                  <div className="flex gap-1">
                    {SECTIONS.map((s) => {
                      const status = Array.isArray(m.section_progress)
                        ? (m.section_progress.find(sp => sp.section_type === s)?.status || "not_started")
                        : (m.section_progress?.[s] || "not_started");
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
                  <div className="mt-2 flex items-center gap-2">
                    <div className="h-1.5 flex-1 rounded-full bg-slate-100">
                      <div className="h-1.5 rounded-full bg-euk-primary transition-all" style={{ width: `${m.progress_percent || 0}%` }} />
                    </div>
                    <span className="text-xs font-semibold text-euk-primary">{m.progress_percent || 0}%</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 flex items-center gap-4 text-xs text-slate-500">
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-emerald-500" />{lang === "fr" ? "Complété" : "Completed"}</div>
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-amber-400" />{lang === "fr" ? "En cours" : "In progress"}</div>
              <div className="flex items-center gap-1"><div className="h-3 w-3 rounded bg-slate-200" />{lang === "fr" ? "Non commencé" : "Not started"}</div>
            </div>
          </div>

          {/* KPI Avant / Après */}
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
                    <div className="text-sm font-semibold text-euk-dark mb-3">
                      {m.module_title_fr || m.module_title || m.title_fr}
                    </div>
                    {kpis.length > 0 ? (
                      <div className="space-y-2">
                        {kpis.map((kpi, kIdx) => (
                          <div key={kIdx} className="grid grid-cols-2 gap-2 text-xs">
                            <div className="col-span-2 text-xs font-semibold text-slate-500 mb-0.5">{kpi.indicator}</div>
                            <div className="rounded-xl border border-red-100 bg-red-50 p-2.5">
                              <div className="font-bold text-red-700 mb-0.5">{lang === "fr" ? "KPI Avant" : "KPI Before"}</div>
                              <div className="text-slate-700 font-semibold">
                                {kpi.baseline_value !== null ? `${kpi.baseline_value} ${kpi.unit || ""}` : "—"}
                              </div>
                            </div>
                            <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-2.5">
                              <div className="font-bold text-emerald-700 mb-0.5">{lang === "fr" ? "KPI Après" : "KPI After"}</div>
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