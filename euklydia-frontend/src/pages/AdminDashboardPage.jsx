import { useState } from "react";
import { apiFetch } from "../utils/api";

export default function AdminDashboardPage() {
  const lang = "fr";

  // ── Overview state ──
  const [overviewData, setOverviewData] = useState(null);
  const [overviewLoading, setOverviewLoading] = useState(false);

  // ── Module analysis state ──
  const [moduleId, setModuleId] = useState(403);
  const [moduleData, setModuleData] = useState(null);
  const [moduleLoading, setModuleLoading] = useState(false);

  // ── Role state ──
  const [selectedRole, setSelectedRole] = useState("AI Sales Specialist");
  const [roleData, setRoleData] = useState(null);
  const [roleLoading, setRoleLoading] = useState(false);
  // ── Content Effectiveness state ──
const [effectivenessModuleId, setEffectivenessModuleId] = useState(403);
const [effectivenessData, setEffectivenessData] = useState(null);
const [effectivenessLoading, setEffectivenessLoading] = useState(false);

  const ROLES = [
    "AI Sales Specialist",
    "AI Marketing Strategist",
    "AI Designer",
    "AI Project Manager",
  ];

  const t = {
    fr: {
      badge: "Tableau de bord administrateur",
      title: "Admin — Analyse cohorte",
      subtitle: "Visualisez l'engagement, les drop-offs et les insights IA sur l'ensemble de vos apprenants.",
      // Overview
      overviewTitle: "Vue globale",
      overviewBtn: "Charger la vue globale",
      overviewLoading: "Chargement...",
      totalLearners: "Apprenants total",
      avgMastery: "Mastery moyenne",
      completions: "Complétions",
      painPoints: "Pain points détectés",
      byRole: "Par rôle",
      topModules: "Top modules",
      learners: "apprenants",
      progress: "progression",
      // Module
      moduleTitle: "Analyse d'un module",
      moduleBtn: "Analyser le module",
      moduleLoading: "Analyse en cours...",
      moduleIdLabel: "Module ID",
      engagement: "Engagement par section",
      dropoffs: "Drop-off points",
      insights: "Insights IA",
      completion: "Complétion",
      abandonment: "Abandon",
      avgScore: "Score moy.",
      dropRate: "Taux abandon",
      blockers: "Top 3 blockers",
      interventions: "Interventions contenu",
      evidence: "Evidence",
      // Role
      roleTitle: "Analyse par rôle",
      roleBtn: "Analyser ce rôle",
      roleLoading: "Chargement...",
      completionRate: "Taux de complétion",
      // Trend
      trendImproving: "📈 En progression",
      trendStable: "➡️ Stable",
      trendDeclining: "📉 En déclin",
      priorityHigh: "Haute",
      priorityMedium: "Moyenne",
      priorityLow: "Basse",
    },
  };
  const tx = t[lang];

  const loadOverview = async () => {
    setOverviewLoading(true);
    try {
      const res = await apiFetch("/api/v1/admin/cohort/overview");
      if (res?.ok) setOverviewData(await res.json());
    } catch { /* non-blocking */ }
    finally { setOverviewLoading(false); }
  };

  const analyzeModule = async () => {
    setModuleLoading(true);
    try {
      const res = await apiFetch(`/api/v1/admin/cohort/module/${moduleId}`);
      if (res?.ok) setModuleData(await res.json());
    } catch { /* non-blocking */ }
    finally { setModuleLoading(false); }
  };

  const analyzeRole = async () => {
    setRoleLoading(true);
    try {
      const res = await apiFetch(`/api/v1/admin/cohort/role/${encodeURIComponent(selectedRole)}`);
      if (res?.ok) setRoleData(await res.json());
    } catch { /* non-blocking */ }
    finally { setRoleLoading(false); }
  };
  const analyzeEffectiveness = async () => {
  setEffectivenessLoading(true);
  try {
    const res = await apiFetch(`/api/v1/analytics/module/${effectivenessModuleId}`);
    if (res?.ok) setEffectivenessData(await res.json());
  } catch { /* non-blocking */ }
  finally { setEffectivenessLoading(false); }
};

  const trendColor = trend => {
    if (trend === "improving") return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (trend === "declining") return "border-red-200 bg-red-50 text-red-700";
    return "border-slate-200 bg-slate-50 text-slate-600";
  };

  const trendLabel = trend => {
    if (trend === "improving") return tx.trendImproving;
    if (trend === "declining") return tx.trendDeclining;
    return tx.trendStable;
  };

  const priorityColor = p => {
    if (p === "high") return "border-red-200 bg-red-50 text-red-700";
    if (p === "medium") return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-emerald-200 bg-emerald-50 text-emerald-700";
  };

  const priorityLabel = p => {
    if (p === "high") return tx.priorityHigh;
    if (p === "medium") return tx.priorityMedium;
    return tx.priorityLow;
  };
  const exportCSV = () => {
  if (!overviewData && !roleData && !effectivenessData) {
    alert("Chargez au moins une section (Vue globale, Rôle, Module ou Effectiveness) avant d'exporter.");
    return;
  }
  const rows = [];
  rows.push(["Type", "Métrique", "Valeur"]);
  if (overviewData?.global) {
    rows.push(["Vue globale", "Apprenants total", overviewData.global.total_learners]);
    rows.push(["Vue globale", "Mastery moyenne", `${overviewData.global.global_avg_mastery}%`]);
    rows.push(["Vue globale", "Complétions", overviewData.global.learners_with_completion]);
  }
  if (roleData?.modules) {
    roleData.modules.forEach(m => {
      rows.push(["Module", m.title, `${m.completion_rate}% complétion`]);
      rows.push(["Module", m.title, `${m.avg_mastery}% mastery`]);
    });
  }
  if (effectivenessData?.analysis) {
    const a = effectivenessData.analysis;
    rows.push(["Effectiveness", `Module ${a.module_id}`, `Score: ${a.effectiveness_score}`]);
    rows.push(["Effectiveness", "Flag", a.performance_flag]);
    rows.push(["Effectiveness", "Drop-off section", a.drop_off_analysis?.main_drop_off_section || "—"]);
  }
  const csv = rows.map(r => r.map(c => `"${c}"`).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `euklydia_analytics_${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
  URL.revokeObjectURL(url);
};

const exportPDF = () => window.print();

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-page">

        {/* ─── HERO ─── */}
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="mb-3 inline-flex items-center rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700">
            {tx.badge}
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{tx.title}</h1>
          <p className="mt-2 text-sm leading-6 text-slate-600">{tx.subtitle}</p>

<div className="mt-4 flex gap-3">
  <button
    onClick={exportCSV}
    className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50">
    ⬇ Export CSV
  </button>
  <button
    onClick={exportPDF}
    className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50">
    🖨 Export PDF
  </button>
</div>
</section>

        {/* ─── 1. VUE GLOBALE ─── */}
        <section className="mt-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-euk-dark">{tx.overviewTitle}</h2>
            <button
              onClick={loadOverview}
              disabled={overviewLoading}
              className="rounded-2xl bg-euk-primary px-5 py-2.5 text-sm font-bold text-white transition hover:bg-euk-deep disabled:opacity-50">
              {overviewLoading ? tx.overviewLoading : tx.overviewBtn}
            </button>
          </div>

          {overviewLoading && <Spinner />}

          {overviewData && !overviewLoading && (
            <div className="space-y-4">
              {/* KPI globaux */}
              <div className="grid gap-4 md:grid-cols-4">
                <KpiCard label={tx.totalLearners} value={overviewData.global?.total_learners ?? 0} />
                <KpiCard label={tx.avgMastery} value={`${overviewData.global?.global_avg_mastery ?? 0}%`} />
                <KpiCard label={tx.completions} value={overviewData.global?.learners_with_completion ?? 0} />
                <KpiCard label={tx.painPoints} value={overviewData.global?.total_pain_points ?? 0} color="text-amber-600" />
              </div>

              {/* Par rôle */}
              {overviewData.by_role?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">{tx.byRole}</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    {overviewData.by_role.map((r, i) => (
                      <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-semibold text-euk-dark">{r.role}</span>
                          <span className="text-xs text-slate-500">{r.learners_count} {tx.learners}</span>
                        </div>
                        <div className="flex items-center gap-2 mb-1">
                          <div className="h-2 flex-1 rounded-full bg-slate-200">
                            <div className="h-2 rounded-full bg-euk-primary" style={{ width: `${r.avg_mastery}%` }} />
                          </div>
                          <span className="text-xs font-semibold text-euk-primary">{r.avg_mastery}%</span>
                        </div>
                        <div className="text-xs text-slate-500">{tx.progress} moy. : {r.avg_progress}% • {r.completions} complétions</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top modules */}
              {overviewData.top_modules?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">{tx.topModules}</h3>
                  <div className="space-y-2">
                    {overviewData.top_modules.map((m, i) => (
                      <div key={i} className="flex items-center gap-4 rounded-2xl border border-slate-100 bg-slate-50 p-3">
                        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-euk-primary/10 text-xs font-bold text-euk-primary">
                          {i + 1}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-semibold text-euk-dark truncate">{m.title}</div>
                          <div className="text-xs text-slate-500">{m.role} • {m.level}</div>
                        </div>
                        <div className="text-right shrink-0">
                          <div className="text-sm font-bold text-euk-primary">{m.completions}</div>
                          <div className="text-xs text-slate-500">{tx.completion}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
        </section>

        {/* ─── 2. ANALYSE PAR RÔLE ─── */}
        <section className="mt-8">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-lg font-bold text-euk-dark">{tx.roleTitle}</h2>
            <div className="flex items-center gap-3">
              <select
                value={selectedRole}
                onChange={e => setSelectedRole(e.target.value)}
                className="rounded-xl border border-slate-200 px-3 py-2 text-sm text-euk-dark outline-none focus:border-euk-primary bg-white">
                {ROLES.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
              <button
                onClick={analyzeRole}
                disabled={roleLoading}
                className="rounded-2xl bg-euk-deep px-5 py-2.5 text-sm font-bold text-white transition hover:bg-euk-primary disabled:opacity-50">
                {roleLoading ? tx.roleLoading : tx.roleBtn}
              </button>
            </div>
          </div>

          {roleLoading && <Spinner color="border-euk-deep" />}

          {roleData && !roleLoading && (
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-3">
                {roleData.modules?.map((m, i) => (
                  <div key={i} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <h3 className="text-sm font-bold text-euk-dark leading-snug">{m.title}</h3>
                      <span className="rounded-full border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs font-semibold text-slate-600 shrink-0">{m.level}</span>
                    </div>
                    <div className="space-y-2 text-xs text-slate-500">
                      <div className="flex justify-between"><span>{tx.learners}</span><span className="font-semibold text-euk-dark">{m.learners}</span></div>
                      <div className="flex justify-between"><span>{tx.completionRate}</span><span className="font-semibold text-emerald-600">{m.completion_rate}%</span></div>
                      <div className="flex justify-between"><span>{tx.avgMastery}</span><span className="font-semibold text-euk-primary">{m.avg_mastery}%</span></div>
                    </div>
                    <div className="mt-3 h-1.5 w-full rounded-full bg-slate-100">
                      <div className="h-1.5 rounded-full bg-euk-primary" style={{ width: `${m.avg_progress}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {/* Insights LLM rôle */}
          {roleData && roleData.insights && !roleData.insights.error && (
            <div className="space-y-4 mt-4">

              {/* Summary + trend */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <p className="flex-1 text-sm leading-6 text-slate-700">
                    {roleData.insights.summary}
                  </p>
                  <span className={`rounded-full border px-3 py-1 text-xs font-semibold shrink-0 ${trendColor(roleData.insights.trend)}`}>
                    {trendLabel(roleData.insights.trend)}
                  </span>
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {roleData.insights.strongest_module && (
                    <span className="rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                      ✅ Meilleur : {roleData.insights.strongest_module}
                    </span>
                  )}
                  {roleData.insights.weakest_module && (
                    <span className="rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
                      ⚠️ À renforcer : {roleData.insights.weakest_module}
                    </span>
                  )}
                </div>
              </div>

              {/* Blockers */}
              {roleData.insights.top_blockers?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">Top blockers</h3>
                  <div className="space-y-3">
                    {roleData.insights.top_blockers.map((b, i) => (
                      <div key={i} className="flex items-start gap-4 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-red-100 text-sm font-bold text-red-700">
                          {b.rank}
                        </div>
                        <div className="flex-1">
                          <div className="text-sm font-semibold text-euk-dark">{b.module}</div>
                          <div className="mt-1 text-xs text-slate-500">
                            <span className="font-medium">Evidence : </span>{b.evidence}
                          </div>
                          <div className="mt-1 text-xs text-slate-500">
                            <span className="font-medium">Impact : </span>{b.impact}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Interventions */}
              {roleData.insights.interventions?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">Interventions recommandées</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    {roleData.insights.interventions.map((item, i) => (
                      <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xl">💡</span>
                          <span className="text-xs font-bold text-euk-dark">{item.type}</span>
                          <span className={`ml-auto rounded-full border px-2 py-0.5 text-xs font-semibold ${priorityColor(item.priority)}`}>
                            {priorityLabel(item.priority)}
                          </span>
                        </div>
                        <div className="text-xs font-semibold text-slate-600 mb-1">{item.module}</div>
                        <div className="text-xs text-slate-500 leading-5">{item.reason}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}
        </section>

        {/* ─── 3. ANALYSE MODULE ─── */}
        <section className="mt-8 mb-8">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-lg font-bold text-euk-dark">{tx.moduleTitle}</h2>
            <div className="flex items-center gap-3">
              <input
                type="number"
                value={moduleId}
                onChange={e => setModuleId(parseInt(e.target.value))}
                className="w-28 rounded-xl border border-slate-200 px-3 py-2 text-sm text-euk-dark outline-none focus:border-euk-primary"
                placeholder={tx.moduleIdLabel}
              />
              <button
                onClick={analyzeModule}
                disabled={moduleLoading}
                className="rounded-2xl bg-violet-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-violet-700 disabled:opacity-50">
                {moduleLoading ? tx.moduleLoading : tx.moduleBtn}
              </button>
            </div>
          </div>

          {moduleLoading && <Spinner color="border-violet-600" />}

          {moduleData && !moduleLoading && (
            <div className="space-y-4">

              {/* Info module */}
              <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-100 text-sm font-bold text-violet-700">
                    #{moduleData.module?.id}
                  </div>
                  <div>
                    <div className="text-base font-bold text-euk-dark">{moduleData.module?.title}</div>
                    <div className="text-xs text-slate-500">{moduleData.module?.role} • {moduleData.module?.level}</div>
                  </div>
                </div>
              </div>

              {/* Engagement par section */}
              {moduleData.engagement?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">{tx.engagement}</h3>
                  <div className="space-y-3">
                    {moduleData.engagement.map((e, i) => (
  <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
    <div className="flex items-center justify-between mb-2">
      <span className="text-sm font-semibold text-euk-dark">{e.module_title}</span>
      <span className="text-xs text-slate-500">{e.learners_count} {tx.learners}</span>
    </div>
    <div className="grid grid-cols-3 gap-2 text-xs text-slate-500">
      <div><span className="font-medium">{tx.progress} :</span> {Math.round(e.avg_progress || 0)}%</div>
      <div><span className="font-medium text-emerald-600">{tx.completion} :</span> {e.completed_count}</div>
      <div><span className="font-medium text-sky-600">En cours :</span> {e.in_progress_count}</div>
    </div>
  </div>
))}
                  </div>
                </div>
              )}
              {/* KPI Cohorte */}
{moduleData.kpi_summary?.length > 0 && (
  <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
    <h3 className="text-base font-bold text-euk-dark mb-4">
      KPI Cohorte — Impact business
    </h3>
    <div className="space-y-3">
      {moduleData.kpi_summary.map((kpi, i) => (
        <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-euk-dark">
              {kpi.indicator}
            </span>
            <span className="text-xs text-slate-500">
              {kpi.learners_measured}/{kpi.learners_total} apprenants mesurés
            </span>
          </div>
          <div className="grid grid-cols-3 gap-3 text-xs">
            <div className="rounded-xl bg-white border border-slate-200 p-2 text-center">
              <div className="text-slate-500 mb-1">Baseline moy.</div>
              <div className="font-bold text-euk-dark">
                {kpi.baseline_avg ?? "—"} {kpi.unit}
              </div>
            </div>
            <div className="rounded-xl bg-white border border-slate-200 p-2 text-center">
              <div className="text-slate-500 mb-1">Actuel moy.</div>
              <div className="font-bold text-euk-dark">
                {kpi.current_avg != null ? `${kpi.current_avg} ${kpi.unit}` : "—"}
              </div>
            </div>
            <div className="rounded-xl bg-white border border-slate-200 p-2 text-center">
              <div className="text-slate-500 mb-1">Delta moy.</div>
              <div className={`font-bold ${
                kpi.delta_avg_pct == null
                  ? "text-slate-400"
                  : kpi.delta_avg_pct < 0
                  ? "text-emerald-600"
                  : "text-blue-600"
              }`}>
                {kpi.delta_avg_pct != null ? `${kpi.delta_avg_pct}%` : "—"}
              </div>
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            🎯 Cible : {kpi.target_label}
          </div>
          {/* Barre de progression mesure */}
          <div className="mt-2 flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-slate-200">
              <div
                className="h-1.5 rounded-full bg-euk-primary"
                style={{ width: `${Math.round(kpi.measurement_rate * 100)}%` }}
              />
            </div>
            <span className="text-xs text-slate-500 shrink-0">
              {Math.round(kpi.measurement_rate * 100)}% saisi
            </span>
          </div>
        </div>
      ))}
    </div>

    {/* kpi_insights LLM */}
    {moduleData.insights?.kpi_insights && (
      <div className="mt-4 rounded-2xl border border-violet-100 bg-violet-50 p-4">
        <div className="text-xs font-bold uppercase tracking-wide text-violet-700 mb-2">
          Analyse IA
        </div>
        <p className="text-xs text-slate-700 leading-5">
          {moduleData.insights.kpi_insights.comment}
        </p>
        <div className="mt-2 flex flex-wrap gap-2">
          {moduleData.insights.kpi_insights.best_indicator && (
            <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">
              ✅ Meilleur : {moduleData.insights.kpi_insights.best_indicator}
            </span>
          )}
          {moduleData.insights.kpi_insights.worst_indicator && (
            <span className="rounded-full border border-amber-200 bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700">
              ⚠️ À améliorer : {moduleData.insights.kpi_insights.worst_indicator}
            </span>
          )}
        </div>
      </div>
    )}
  </div>
)}
              {/* Insights IA */}
              {moduleData.insights && !moduleData.insights.error && (
                <div className="space-y-4">
                  {/* Summary + trend */}
                  <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                    <div className="flex flex-wrap items-start justify-between gap-3">
                      <p className="flex-1 text-sm leading-6 text-slate-700">{moduleData.insights.summary}</p>
                      <div className="flex gap-2 shrink-0">
                        <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${trendColor(moduleData.insights.trend)}`}>
                          {trendLabel(moduleData.insights.trend)}
                        </span>
                        <span className="rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-xs font-semibold text-violet-700">
                          {tx.completionRate} : {Math.round((moduleData.insights.completion_rate || 0) * 100)}%
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Blockers */}
                  {moduleData.insights.top_blockers?.length > 0 && (
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                      <h3 className="text-base font-bold text-euk-dark mb-4">{tx.blockers}</h3>
                      <div className="space-y-3">
                        {moduleData.insights.top_blockers.map((b, i) => (
                          <div key={i} className="flex items-start gap-4 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-red-100 text-sm font-bold text-red-700">{b.rank}</div>
                            <div className="flex-1">
                              <div className="text-sm font-semibold text-euk-dark">{b.section}</div>
                              <div className="mt-1 flex items-center gap-2">
                                <div className="h-1.5 w-24 rounded-full bg-slate-200">
                                  <div className="h-1.5 rounded-full bg-red-400" style={{ width: `${Math.round((b.drop_off_rate || 0) * 100)}%` }} />
                                </div>
                                <span className="text-xs text-slate-500">{Math.round((b.drop_off_rate || 0) * 100)}% {tx.dropRate}</span>
                              </div>
                              <div className="mt-1 text-xs text-slate-500"><span className="font-medium">{tx.evidence} :</span> {b.evidence}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Interventions contenu */}
                  {moduleData.insights.interventions?.length > 0 && (
                    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                      <h3 className="text-base font-bold text-euk-dark mb-4">{tx.interventions}</h3>
                      <div className="grid gap-3 md:grid-cols-3">
                        {moduleData.insights.interventions.map((item, i) => (
                          <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-xl">📝</span>
                              <span className="text-xs font-bold text-euk-dark">{item.type}</span>
                              <span className={`ml-auto rounded-full border px-2 py-0.5 text-xs font-semibold ${priorityColor(item.priority)}`}>
                                {priorityLabel(item.priority)}
                              </span>
                              
                            </div>
                            <div className="text-xs font-semibold text-slate-600 mb-1">{item.section}</div>
                            <div className="text-xs text-slate-500 leading-5">{item.reason}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>

      {/* ─── 4. CONTENT EFFECTIVENESS SCORING ─── */}
        <section className="mt-8 mb-8">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <h2 className="text-lg font-bold text-euk-dark">
              Content Effectiveness Scoring
            </h2>
            <div className="flex items-center gap-3">
              <input
                type="number"
                value={effectivenessModuleId}
                onChange={e => setEffectivenessModuleId(parseInt(e.target.value))}
                className="w-28 rounded-xl border border-slate-200 px-3 py-2 text-sm text-euk-dark outline-none focus:border-euk-primary"
                placeholder="Module ID"
              />
              <button
                onClick={analyzeEffectiveness}
                disabled={effectivenessLoading}
                className="rounded-2xl bg-emerald-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-emerald-700 disabled:opacity-50">
                {effectivenessLoading ? "Analyse..." : "Analyser l'efficacité"}
              </button>
            </div>
          </div>

          {effectivenessLoading && <Spinner color="border-emerald-600" />}

          {effectivenessData && !effectivenessLoading && (
            <div className="space-y-4">

              {/* Score global */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <div className="text-base font-bold text-euk-dark mb-1">
                      {effectivenessData.analysis?.module_id && `Module ${effectivenessData.analysis.module_id}`}
                    </div>
                    <p className="text-sm leading-6 text-slate-600">{effectivenessData.analysis?.summary}</p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    {/* Score cercle */}
                    <div className="flex flex-col items-center">
                      <div className={`flex h-16 w-16 items-center justify-center rounded-full border-4 text-xl font-bold
                        ${effectivenessData.analysis?.effectiveness_score >= 70
                          ? "border-emerald-400 text-emerald-600"
                          : effectivenessData.analysis?.effectiveness_score >= 40
                          ? "border-amber-400 text-amber-600"
                          : "border-red-400 text-red-600"}`}>
                        {effectivenessData.analysis?.effectiveness_score ?? "—"}
                      </div>
                      <span className="mt-1 text-xs text-slate-500">Score</span>
                    </div>
                    {/* Flag */}
                    <span className={`rounded-full border px-3 py-1 text-xs font-bold
                      ${effectivenessData.analysis?.performance_flag === "good"
                        ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : effectivenessData.analysis?.performance_flag === "needs_improvement"
                        ? "border-amber-200 bg-amber-50 text-amber-700"
                        : "border-red-200 bg-red-50 text-red-700"}`}>
                      {effectivenessData.analysis?.performance_flag === "good" ? "🟢 Good"
                        : effectivenessData.analysis?.performance_flag === "needs_improvement" ? "🟡 Needs improvement"
                        : "🔴 Critical"}
                    </span>
                  </div>
                </div>
              </div>

              {/* 3 métriques */}
              <div className="grid gap-4 md:grid-cols-3">
                {/* KPI */}
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-400 mb-3">KPI Analysis</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-500">{lang === "fr" ? "Complétion tâche" : "Task completion"}</span>
                      <span className="font-bold text-euk-primary">
                        {Math.round((effectivenessData.analysis?.kpi_analysis?.completion_rate || 0) * 100)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{lang === "fr" ? "Mesure KPI" : "KPI measurement"}</span>
                      <span className="font-bold text-euk-primary">
                        {Math.round((effectivenessData.analysis?.kpi_analysis?.kpi_measurement_rate || 0) * 100)}%
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-slate-500 leading-5">
                      {effectivenessData.analysis?.kpi_analysis?.evidence}
                    </div>
                  </div>
                </div>

                {/* Time to mastery */}
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-400 mb-3">Time to Mastery</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-500">{lang === "fr" ? "Temps moyen" : "Avg time"}</span>
                      <span className="font-bold text-euk-primary">
                        {effectivenessData.analysis?.time_to_mastery_analysis?.avg_minutes
                          ? `${effectivenessData.analysis.time_to_mastery_analysis.avg_minutes} min`
                          : "—"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Assessment</span>
                      <span className="font-semibold text-slate-700">
                        {effectivenessData.analysis?.time_to_mastery_analysis?.assessment ?? "—"}
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-slate-500 leading-5">
                      {effectivenessData.analysis?.time_to_mastery_analysis?.evidence}
                    </div>
                  </div>
                </div>

                {/* Drop-off */}
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="text-xs font-bold uppercase tracking-wide text-slate-400 mb-3">Drop-off Analysis</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-500">{lang === "fr" ? "Section critique" : "Critical section"}</span>
                      <span className="font-bold text-red-600">
                        {effectivenessData.analysis?.drop_off_analysis?.main_drop_off_section ?? "—"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">{lang === "fr" ? "Taux abandon" : "Drop rate"}</span>
                      <span className="font-bold text-red-600">
                        {Math.round((effectivenessData.analysis?.drop_off_analysis?.drop_off_rate || 0) * 100)}%
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-slate-500 leading-5">
                      {effectivenessData.analysis?.drop_off_analysis?.evidence}
                    </div>
                  </div>
                </div>
              </div>

              {/* Recommandations */}
              {effectivenessData.analysis?.recommendations?.length > 0 && (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="text-base font-bold text-euk-dark mb-4">
                    {lang === "fr" ? "Recommandations d'amélioration" : "Improvement recommendations"}
                  </h3>
                  <div className="grid gap-3 md:grid-cols-3">
                    {effectivenessData.analysis.recommendations.map((r, i) => (
                      <div key={i} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-xl">💡</span>
                          <span className="text-xs font-bold text-euk-dark">{r.type}</span>
                          <span className={`ml-auto rounded-full border px-2 py-0.5 text-xs font-semibold ${priorityColor(r.priority)}`}>
                            {priorityLabel(r.priority)}
                          </span>
                        </div>
                        <div className="text-xs font-semibold text-slate-600 mb-1">{r.section}</div>
                        <div className="text-xs text-slate-500 leading-5">{r.action}</div>
                        <div className="mt-2 text-xs text-slate-400 italic">{r.evidence}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Flags */}
              {effectivenessData.analysis?.flags?.length > 0 && (
                <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                  <div className="text-xs font-bold uppercase tracking-wide text-amber-700 mb-2">
                    ⚠️ {lang === "fr" ? "Alertes" : "Flags"}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {effectivenessData.analysis.flags.map((f, i) => (
                      <span key={i} className="rounded-full border border-amber-300 bg-white px-3 py-1 text-xs font-semibold text-amber-700">
                        {f}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}

// ── Composants utilitaires internes ──

function KpiCard({ label, value, color = "text-euk-primary" }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="text-sm font-medium text-slate-500">{label}</div>
      <div className={`mt-2 text-3xl font-bold tracking-tight ${color}`}>{value}</div>
    </div>
  );
}

function Spinner({ color = "border-euk-primary" }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-sm">
      <div className="flex items-center justify-center gap-3">
        <div className={`h-5 w-5 animate-spin rounded-full border-2 ${color} border-t-transparent`} />
      </div>
    </div>
  );
}