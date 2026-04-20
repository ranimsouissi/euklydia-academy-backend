import { useEffect, useMemo, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";
import ConfirmModal from "../components/ConfirmModal";

export default function CommandCenterPage() {
  const navigate = useNavigate();
  const { language } = useOutletContext();
  const lang = language || "en";

  const [skills, setSkills] = useState([]);
  const [summary, setSummary] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);

  const t = {
    en: {
      heroBadge: "AI capability dashboard",
      title: "Command Center",
      subtitle: "Visualize your current level, identify the most critical priorities, and move quickly toward your next strategic action.",
      viewRoadmap: "View AI Roadmap",
      redoAssessment: "Retake assessment",
      confirmTitle: "Retake assessment?",
      confirmMessage: "Your current scores will be replaced by the new results. This action cannot be undone.",
      confirmLabel: "Yes, retake",
      cancelLabel: "Cancel",
      globalScore: "Global AI Score",
      globalScoreText: "Estimated average score across all evaluated skills.",
      highPriorityGaps: "High Priority Gaps",
      highPrioritySkills: "High priority skills",
      highPriorityText: "Skills to strengthen first in order to accelerate your progress.",
      nextFocus: "Next Focus",
      completeAssessmentNextFocus: "Complete the assessment to define your next focus area.",
      priority: "Priority",
      nextStrategicMove: "Next Strategic Move",
      nextStrategicMoveEmpty: "Complete the assessment to generate your next action.",
      viewRoadmapShort: "View Roadmap",
      focusOn: 'Focus on "{skill}" (Priority: {priority}, Level: {level}, Score: {score}%).',
      executiveReport: "Executive Report",
      executiveReportText: "Generate and download your executive PDF report based on the current assessment results.",
      generateExecutivePdf: "Generate Executive PDF",
      skillBreakdown: "Skill Breakdown",
      skillBreakdownText: "Detailed view of the skills, levels, and priorities identified by the assessment.",
      scoreLabel: "Score",
      highPriorityDesc: "Address first with targeted training and guided practice.",
      mediumPriorityDesc: "Strengthen with focused exercises and concrete use cases.",
      lowPriorityDesc: "Good current level, with room for optimization and deeper development.",
      noResults: "No assessment results found",
      noResultsText: "Take the assessment to display your dashboard and generate your priorities.",
      startAssessment: "Start assessment",
      alertUserIdNotFound: "User ID not found. Login again.",
      alertTokenNotFound: "Token not found. Login again.",
      alertGenerateFailed: "Generate failed",
      alertDownloadFailed: "Download failed",
      alertUnexpectedError: "Unexpected error",
      aiProfile: "Your AI Profile",
      aiProfileGlobalScore: "Global Score",
      aiNovice: "AI Novice",
      aiPractitioner: "AI Practitioner",
      aiLeader: "AI Leader",
      aiNoviceDesc: "You are at the beginning of your AI journey. Focus on building foundational knowledge before integrating AI into your work.",
      aiPractitionerDesc: "You have a solid understanding of AI. Now focus on applying it consistently and responsibly in your daily work.",
      aiLeaderDesc: "You are ahead of most professionals in AI adoption. Focus on systematising AI in your workflows and leading your team.",
      aiNoviceFocus: "Recommended focus: Start with AI Literacy and Generative AI Basics.",
      aiPractitionerFocus: "Recommended focus: Focus on AI Prompting, Output Evaluation, and Responsible Use.",
      aiLeaderFocus: "Recommended focus: Focus on AI Workflow Integration and leading AI adoption in your organisation.",
    },
    fr: {
      heroBadge: "Tableau de bord des capacites IA",
      title: "Centre de commande",
      subtitle: "Visualisez votre niveau actuel, identifiez les priorites les plus critiques et passez rapidement a la prochaine action strategique.",
      viewRoadmap: "Voir la feuille de route IA",
      redoAssessment: "Refaire l'assessment",
      confirmTitle: "Refaire l'assessment?",
      confirmMessage: "Vos scores actuels seront remplaces par les nouveaux resultats. Cette action est irreversible.",
      confirmLabel: "Oui, refaire",
      cancelLabel: "Annuler",
      globalScore: "Score IA global",
      globalScoreText: "Score moyen estime sur l'ensemble des competences evaluees.",
      highPriorityGaps: "Ecarts a haute priorite",
      highPrioritySkills: "Compétences prioritaires",
      highPriorityText: "Competences a renforcer en priorite pour accelerer votre progression.",
      nextFocus: "Prochain focus",
      completeAssessmentNextFocus: "Completez l'assessment pour definir votre prochain axe de focus.",
      priority: "Priorite",
      nextStrategicMove: "Prochaine action strategique",
      nextStrategicMoveEmpty: "Completez l'assessment pour generer votre prochaine action.",
      viewRoadmapShort: "Voir la feuille de route",
      focusOn: 'Concentrez-vous sur "{skill}" (Priorite : {priority}, Niveau : {level}, Score : {score}%).',
      executiveReport: "Rapport executif",
      executiveReportText: "Generez et telechargez votre rapport PDF executif a partir des resultats actuels d'assessment.",
      generateExecutivePdf: "Generer le PDF executif",
      skillBreakdown: "Repartition des competences",
      skillBreakdownText: "Vue detaillee des competences, niveaux et priorites identifies par l'assessment.",
      scoreLabel: "Score",
      highPriorityDesc: "A traiter en priorite avec une formation ciblee et une pratique guidee.",
      mediumPriorityDesc: "A renforcer avec des exercices cibles et des cas d'usage concrets.",
      lowPriorityDesc: "Bon niveau actuel, avec un potentiel d'optimisation et d'approfondissement.",
      noResults: "Aucun resultat d'assessment trouve",
      noResultsText: "Faites l'assessment pour afficher votre dashboard et generer vos priorites.",
      startAssessment: "Commencer l'assessment",
      alertUserIdNotFound: "ID utilisateur introuvable. Reconnectez-vous.",
      alertTokenNotFound: "Token introuvable. Reconnectez-vous.",
      alertGenerateFailed: "Echec de generation",
      alertDownloadFailed: "Echec du telechargement",
      alertUnexpectedError: "Erreur inattendue",
      aiProfile: "Votre profil IA",
      aiProfileGlobalScore: "Score global",
      aiNovice: "Novice IA",
      aiPractitioner: "Praticien IA",
      aiLeader: "Leader IA",
      aiNoviceDesc: "Vous êtes au début de votre parcours IA. Concentrez-vous sur les bases avant d'intégrer l'IA dans votre travail.",
      aiPractitionerDesc: "Vous avez une bonne compréhension de l'IA. Concentrez-vous sur une application régulière et responsable dans votre travail.",
      aiLeaderDesc: "Vous êtes en avance sur la plupart des professionnels dans l'adoption de l'IA. Concentrez-vous sur la systématisation et le leadership.",
      aiNoviceFocus: "Focus recommandé : Commencez par AI Literacy et Generative AI Basics.",
      aiPractitionerFocus: "Focus recommandé : Concentrez-vous sur le Prompting, l'Évaluation des sorties et l'IA Responsable.",
      aiLeaderFocus: "Focus recommandé : Intégration IA dans vos workflows et leadership de l'adoption IA.",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        const sRes = await apiFetch("/api/v1/assessment/status");
        if (!sRes) return;
        const sData = await sRes.json().catch(() => ({}));

        if (sRes.ok && sData.required) {
          navigate("/assessment");
          return;
        }

        const res = await apiFetch("/api/v1/assessment/results");
        if (!res) return;
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          const msg = data?.detail || "";
          if (String(msg).toLowerCase().includes("career path")) {
            navigate("/onboarding");
            return;
          }
          setSkills([]);
          return;
        }

        setSkills(Array.isArray(data) ? data : []);
        const roadmapRes = await apiFetch("/api/v1/roadmap");
        if (roadmapRes?.ok) {
          const roadmapData = await roadmapRes.json().catch(() => ({}));
          if (roadmapData?.summary) setSummary(roadmapData.summary);
        }
      } catch (e) {
        setSkills([]);
      }
    })();
  }, [navigate]);

  const userId = useMemo(() => {
    try {
      const raw = localStorage.getItem("auth_user");
      if (!raw) return null;
      return JSON.parse(raw)?.id ?? null;
    } catch { return null; }
  }, []);

  const globalScore = useMemo(() => {
    if (!skills.length) return 0;
    const avg = skills.reduce((acc, s) => acc + (Number(s.score) || 0), 0) / skills.length;
    return Math.round(avg);
  }, [skills]);

  const highCount = useMemo(() => {
    return skills.filter((s) => String(s.priority).toUpperCase() === "HIGH").length;
  }, [skills]);

  const nextMove = useMemo(() => {
    if (!skills.length) return null;
    const rank = (p) => {
      const v = String(p).toUpperCase();
      if (v === "HIGH") return 0;
      if (v === "MEDIUM") return 1;
      return 2;
    };
    const sorted = [...skills].sort((a, b) => {
      const pr = rank(a.priority) - rank(b.priority);
      if (pr !== 0) return pr;
      return (Number(a.score) || 0) - (Number(b.score) || 0);
    });
    return sorted[0];
  }, [skills]);

  const aiProfile = useMemo(() => {
    if (summary) {
      const label = lang === "fr" ? summary.profile_fr : summary.profile;
      const description = lang === "fr" ? summary.description_fr : summary.description_en;
      const role = lang === "fr" ? summary.role_fr : summary.role_en;
      const cta = lang === "fr" ? summary.cta_fr : summary.cta_en;
      const badgeClass = globalScore < 40
        ? "border-amber-200 bg-amber-50 text-amber-700"
        : globalScore <= 70
        ? "border-sky-200 bg-sky-50 text-sky-700"
        : "border-emerald-200 bg-emerald-50 text-emerald-700";
      return { label, description, role, focus: cta, badgeClass };
    }
    if (globalScore < 40) return {
      label: t[lang].aiNovice, description: t[lang].aiNoviceDesc,
      focus: t[lang].aiNoviceFocus, badgeClass: "border-amber-200 bg-amber-50 text-amber-700",
    };
    if (globalScore <= 70) return {
      label: t[lang].aiPractitioner, description: t[lang].aiPractitionerDesc,
      focus: t[lang].aiPractitionerFocus, badgeClass: "border-sky-200 bg-sky-50 text-sky-700",
    };
    return {
      label: t[lang].aiLeader, description: t[lang].aiLeaderDesc,
      focus: t[lang].aiLeaderFocus, badgeClass: "border-emerald-200 bg-emerald-50 text-emerald-700",
    };
  }, [globalScore, lang, summary]);

  const priorityBadgeClass = (p) => {
    const v = String(p).toUpperCase();
    if (v === "HIGH") return "border-red-200 bg-red-50 text-red-700";
    if (v === "MEDIUM") return "border-amber-200 bg-amber-50 text-amber-700";
    return "border-emerald-200 bg-emerald-50 text-emerald-700";
  };

  const levelBadgeClass = (lvl) => {
    const v = String(lvl || "").toLowerCase();
    if (v.includes("begin")) return "border-emerald-200 bg-emerald-50 text-emerald-700";
    if (v.includes("inter")) return "border-sky-200 bg-sky-50 text-sky-700";
    return "border-violet-200 bg-violet-50 text-violet-700";
  };

  const formatNextMoveText = (item) => {
    if (!item) return t[lang].nextStrategicMoveEmpty;
    return t[lang].focusOn
      .replace("{skill}", item.skill_name)
      .replace("{priority}", String(item.priority).toUpperCase())
      .replace("{level}", item.level)
      .replace("{score}", item.score);
  };

  const nextFocusText = nextMove
    ? `${t[lang].priority} ${String(nextMove.priority).toUpperCase()} • ${nextMove.level}`
    : t[lang].completeAssessmentNextFocus;

  const getPriorityDescription = (priority) => {
    const value = String(priority).toUpperCase();
    if (value === "HIGH") return t[lang].highPriorityDesc;
    if (value === "MEDIUM") return t[lang].mediumPriorityDesc;
    return t[lang].lowPriorityDesc;
  };

  const downloadExecutivePdf = async () => {
    try {
      if (!userId) { alert(t[lang].alertUserIdNotFound); return; }
      const token = localStorage.getItem("token");
      if (!token) { alert(t[lang].alertTokenNotFound); return; }

      const res = await fetch(
        `${process.env.REACT_APP_API_URL}/api/v1/brochure/executive-report/${userId}/generate-and-store?lang=${lang}`,
        { method: "POST", headers: { Authorization: `Bearer ${token}` } }
      );
      const data = await res.json().catch(() => ({}));
      if (!res.ok) { alert(data?.detail || t[lang].alertGenerateFailed); return; }

      const reportId = data.report_id;
      const pdfRes = await fetch(
        `${process.env.REACT_APP_API_URL}/api/v1/brochure/reports/download/${reportId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!pdfRes.ok) {
        const err = await pdfRes.json().catch(() => ({}));
        alert(err?.detail || t[lang].alertDownloadFailed);
        return;
      }

      const blob = await pdfRes.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `euklydia_report_${reportId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert(e?.message || t[lang].alertUnexpectedError);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">

        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                {t[lang].heroBadge}
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">{t[lang].title}</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">{t[lang].subtitle}</p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setShowConfirm(true)}
                className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
              >
                {t[lang].redoAssessment}
              </button>
            </div>
          </div>
        </section>

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
            <div className="mt-3 text-3xl font-bold tracking-tight text-euk-dark">{highCount}</div>
            <div className="mt-3 inline-flex rounded-full border border-red-200 bg-red-50 px-3 py-1 text-xs font-semibold text-red-700">
              {t[lang].highPrioritySkills}
            </div>
            <div className="mt-4 text-sm text-slate-500">{t[lang].highPriorityText}</div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-medium text-slate-500">{t[lang].nextFocus}</div>
            <div className="mt-3 text-xl font-bold leading-tight text-euk-dark">{nextMove?.skill_name || "—"}</div>
            <div className="mt-3 text-sm text-slate-500">{nextFocusText}</div>
          </div>
        </section>

        {!!skills.length && (
          <section className="mt-6 rounded-3xl border border-euk-primary/20 bg-euk-primary/5 p-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-euk-primary">{t[lang].aiProfile}</div>
                <div className="text-2xl font-bold text-euk-dark">{aiProfile.label}</div>
                {aiProfile.role && <div className="mt-1 text-sm font-medium text-euk-primary">{aiProfile.role}</div>}
              </div>
              <div className={["rounded-full border px-4 py-2 text-sm font-semibold", aiProfile.badgeClass].join(" ")}>
                {globalScore}% {t[lang].aiProfileGlobalScore}
              </div>
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-600">{aiProfile.description}</p>
            <button onClick={() => navigate("/roadmap")} className="mt-3 text-sm font-semibold text-euk-primary underline">
              {t[lang].viewRoadmap}
            </button>
          </section>
        )}

        <section className="mt-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="text-sm font-semibold text-euk-dark">{t[lang].executiveReport}</div>
            <div className="mt-2 text-sm leading-6 text-slate-500">{t[lang].executiveReportText}</div>
            <button
              onClick={downloadExecutivePdf}
              className="mt-5 w-full rounded-2xl bg-euk-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep"
            >
              {t[lang].generateExecutivePdf}
            </button>
          </div>
        </section>

        <section className="mt-8">
          <div className="mb-4">
            <h2 className="text-lg font-bold text-euk-dark">{t[lang].skillBreakdown}</h2>
            <p className="mt-1 text-sm text-slate-500">{t[lang].skillBreakdownText}</p>
          </div>

          {!!skills.length && (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {skills.map((s) => (
                <div key={s.skill_id} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-base font-bold leading-snug text-euk-dark">{s.skill_name}</h3>
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", priorityBadgeClass(s.priority)].join(" ")}>
                      {String(s.priority).toUpperCase()}
                    </span>
                  </div>
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    <span className={["rounded-full border px-3 py-1 text-xs font-semibold", levelBadgeClass(s.level)].join(" ")}>{s.level}</span>
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-euk-dark">
                      {t[lang].scoreLabel}: {s.score}%
                    </span>
                  </div>
                  <div className="mt-4 h-2.5 w-full rounded-full bg-slate-100">
                    <div className="h-2.5 rounded-full bg-euk-primary" style={{ width: `${Number(s.score) || 0}%` }} />
                  </div>
                  <div className="mt-4 text-sm leading-6 text-slate-500">{getPriorityDescription(s.priority)}</div>
                </div>
              ))}
            </div>
          )}

          {!skills.length && (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm">
              <div className="text-base font-semibold text-euk-dark">{t[lang].noResults}</div>
              <div className="mt-2 text-sm text-slate-500">{t[lang].noResultsText}</div>
              <button
                onClick={() => navigate("/assessment")}
                className="mt-5 rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep"
              >
                {t[lang].startAssessment}
              </button>
            </div>
          )}
        </section>
      </div>

      {showConfirm && (
        <ConfirmModal
          title={t[lang].confirmTitle}
          message={t[lang].confirmMessage}
          confirmLabel={t[lang].confirmLabel}
          cancelLabel={t[lang].cancelLabel}
          confirmClass="bg-rose-500 hover:bg-rose-600"
          onConfirm={() => { setShowConfirm(false); navigate("/assessment"); }}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
}