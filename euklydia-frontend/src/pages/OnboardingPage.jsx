import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { setMyCareerPath } from "../services/auth";
import { getCareerPaths } from "../services/careerPaths";
import { apiFetch } from "../utils/api";

const ROLE_DETAILS = {
  "AI Sales Specialist": {
    forWho: "Sales managers, account executives, business developers",
    desc: "Leverage AI to close more deals, personalize outreach at scale, and automate your sales workflow — while keeping human relationships at the center.",
    tasks: [
      "Prospecter et qualifier des leads plus rapidement avec Apollo.io et LinkedIn Sales Navigator AI",
      "Personnaliser des emails et propositions à grande échelle avec HubSpot AI",
      "Automatiser les tâches répétitives du CRM et les séquences de relance",
      "Lire et exploiter les données ventes pour anticiper les résultats",
      "Utiliser l'AI de façon éthique et responsable dans les interactions clients",
    ],
    deliverables: [
      "AI Sales Playbook personnalisé",
      "Bibliothèque de prompts de prospection",
      "Séquences d'emails automatisées HubSpot",
      "Tableau de bord commercial AI",
    ],
    tag: "Sales",
    tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
  },
  "AI Marketing Strategist": {
    forWho: "Marketing managers, content managers, growth leads",
    desc: "Accelerate content production, sharpen campaign targeting, and turn marketing data into strategic insight — with AI as your growth engine.",
    tasks: [
      "Créer 30 posts, 5 emails et 3 visuels en 2 heures avec ChatGPT et Canva AI",
      "Planifier et automatiser 1 mois de contenu réseaux sociaux avec Buffer AI",
      "Lancer des campagnes publicitaires Facebook et Google Ads optimisées par AI",
      "Analyser les données marketing et adapter sa stratégie en temps réel",
      "Créer des campagnes email automatisées et personnalisées avec Brevo AI",
    ],
    deliverables: [
      "Calendrier de contenu AI — 1 mois complet",
      "Bibliothèque de prompts marketing",
      "Campagne publicitaire complète (Facebook + Google)",
      "Dashboard marketing AI avec KPIs",
    ],
    tag: "Go-to-Market",
    tagColor: { bg: "rgba(212,83,126,0.10)", color: "#993556" },
  },
  "AI Designer": {
    forWho: "Designers, architects, creative directors",
    desc: "Supercharge your creative process — from concept to delivery — using AI as an ideation partner, production accelerator, and creative co-pilot.",
    tasks: [
      "Générer des visuels et affiches professionnelles avec Midjourney et Adobe Firefly",
      "Créer des interfaces UI/UX bilingues arabe/français avec Figma AI et Uizard",
      "Produire des vidéos publicitaires avec voix off arabe via Runway ML et ElevenLabs",
      "Construire une identité visuelle complète avec calligraphie arabe et design moderne",
      "Maîtriser les droits commerciaux et la propriété intellectuelle des créations AI",
    ],
    deliverables: [
      "Identité visuelle complète (logo + palette + typographie)",
      "Maquettes UI/UX bilingues arabe/français",
      "Vidéo publicitaire AI avec voix off",
      "Bibliothèque de prompts visuels",
    ],
    tag: "Creativity",
    tagColor: { bg: "rgba(127,119,221,0.10)", color: "#534AB7" },
  },
  "AI Project Manager": {
    forWho: "Project managers, PMOs, coordinators",
    desc: "Deliver AI projects on time and on scope — by mastering planning, stakeholder alignment, risk management and team coordination in an AI-driven environment.",
    tasks: [
      "Générer des plannings complets automatiquement avec ClickUp AI et Notion AI",
      "Centraliser et coordonner plusieurs projets depuis un seul tableau de bord AI",
      "Prédire les risques et retards avant qu'ils surviennent avec l'AI",
      "Former son équipe à l'AI et gérer la résistance au changement",
      "Encadrer les décisions AI avec des règles éthiques et de gouvernance claires",
    ],
    deliverables: [
      "Planning projet complet généré par AI",
      "Tableau de bord risques et ressources",
      "AI Delivery Checklist",
      "Politique de gouvernance AI",
    ],
    tag: "Delivery",
    tagColor: { bg: "rgba(56,130,221,0.10)", color: "#1a5fa8" },
  },
};

const OPTION_KEYS = ["A", "B", "C", "D"];
const OPTION_LABELS = { A: "option_a", B: "option_b", C: "option_c", D: "option_d" };

export default function OnboardingPage() {
  const navigate = useNavigate();
  const [careerPaths, setCareerPaths] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [loadingCP, setLoadingCP] = useState(true);
  const [savingCP, setSavingCP] = useState(false);
  const [questionnaire, setQuestionnaire] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loadingQ, setLoadingQ] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        setError("");
        setLoadingCP(true);
        const data = await getCareerPaths();
        const activeRoles = Object.keys(ROLE_DETAILS);
        setCareerPaths(data.filter((cp) => activeRoles.includes(cp.name)));
      } catch (e) {
        setError(e?.response?.data?.detail || e.message);
      } finally {
        setLoadingCP(false);
      }
    }
    load();
  }, []);

  const loadQuestionnaire = async () => {
    try {
      setError("");
      setLoadingQ(true);
      const res = await apiFetch("/api/v1/assessment/questionnaire");
      if (!res) return;
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.detail || "Failed to load questionnaire");
        return;
      }
      const data = await res.json();
      setQuestionnaire(data);
      setAnswers({});
    } catch (e) {
      setError(e.message || "Error loading questionnaire");
    } finally {
      setLoadingQ(false);
    }
  };

  const handleSelectCareerPath = async (cpId) => {
    try {
      setError("");
      setSelectedId(cpId);
      setSavingCP(true);
      await setMyCareerPath(cpId);
      await loadQuestionnaire();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setSavingCP(false);
    }
  };

  const setAnswer = (questionId, option) =>
    setAnswers((prev) => ({ ...prev, [questionId]: option }));

  const totalQuestions = useMemo(
    () => questionnaire?.skills?.reduce((acc, skill) => acc + (skill?.questions?.length || 0), 0) || 0,
    [questionnaire]
  );
  const answeredCount = useMemo(() => Object.keys(answers).length, [answers]);
  const isComplete = totalQuestions > 0 && answeredCount === totalQuestions;

  const handleSubmit = async () => {
    try {
      setError("");
      if (!questionnaire) { setError("No questionnaire loaded."); return; }
      if (!isComplete) { setError(`Please answer all questions (${answeredCount}/${totalQuestions}).`); return; }
      setSubmitting(true);

      const payload = {
        answers: Object.entries(answers).map(([qid, selected_option]) => ({
          question_id: Number(qid),
          selected_option,
        })),
      };

      const res = await apiFetch("/api/v1/assessment/submit", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (!res) return;
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data?.detail?.message || data?.detail || "Submit failed");
        return;
      }
      const data = await res.json();
      localStorage.setItem("assessment_results", JSON.stringify(data));
      navigate("/dashboard");
    } catch (e) {
      setError(e.message || "Error");
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingCP) {
    return (
      <div className="min-h-screen bg-slate-50 px-6 py-12">
        <div className="max-w-5xl mx-auto">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-slate-200 rounded-xl w-1/3" />
            <div className="h-4 bg-slate-200 rounded-xl w-1/2" />
            <div className="grid md:grid-cols-2 gap-4">
              {[1,2,3,4].map(i => <div key={i} className="h-48 bg-slate-200 rounded-2xl" />)}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-6">
      <div className="max-w-5xl mx-auto">

        <div className="mb-10">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-teal-700 bg-teal-50 px-3 py-1.5 rounded-full mb-4 border border-teal-100">
            <span className="w-1.5 h-1.5 rounded-full bg-teal-500 inline-block" />
            Welcome to Euklydia Academy
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-2">What is your role?</h1>
          <p className="text-slate-500 text-sm leading-relaxed max-w-xl">
            Choose the path that matches your position. Your training will be fully adapted to your responsibilities and goals.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 text-sm">{error}</div>
        )}

        {/* STEP 1 — Choix du rôle */}
        <section className="mb-12">
          <div className="mb-5">
            <h2 className="text-base font-semibold text-slate-900">
              <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-teal-600 text-white text-xs font-bold mr-2">1</span>
              Choose your role
            </h2>
            <p className="text-sm text-slate-400 mt-1 ml-8">Click "See details" to understand what you'll learn and produce.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {careerPaths.map((cp) => {
              const selected = selectedId === cp.id;
              const expanded = expandedId === cp.id;
              const details = ROLE_DETAILS[cp.name];

              return (
                <div key={cp.id} className={[
                  "bg-white rounded-2xl border transition-all duration-200",
                  selected ? "border-teal-500 ring-2 ring-teal-100 shadow-md" : "border-slate-200 hover:shadow-md hover:-translate-y-0.5",
                ].join(" ")}>
                  <div className="p-5">
                    <div className="flex justify-between items-start gap-3 mb-3">
                      <div className="flex-1">
                        {details && (
                          <span style={{
                            display: "inline-flex", padding: "3px 10px", borderRadius: 999,
                            background: details.tagColor.bg, color: details.tagColor.color,
                            fontWeight: 700, fontSize: 11, marginBottom: 6,
                          }}>
                            {details.tag}
                          </span>
                        )}
                        <div className="font-bold text-slate-900 text-base">{cp.name}</div>
                        {details && <div className="text-xs text-slate-400 font-medium mt-0.5">{details.forWho}</div>}
                      </div>
                      {selected && (
                        <span className="shrink-0 text-xs bg-teal-50 text-teal-700 px-2.5 py-1 rounded-full font-bold border border-teal-100">✓ Selected</span>
                      )}
                    </div>

                    <p className="text-sm text-slate-500 leading-relaxed mb-3">
                      {details ? details.desc : cp.description}
                    </p>

                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => handleSelectCareerPath(cp.id)}
                        disabled={savingCP}
                        className={[
                          "flex-1 py-2.5 rounded-xl text-sm font-bold transition-all duration-200",
                          selected ? "bg-teal-600 text-white" : "bg-slate-50 text-slate-700 border border-slate-200 hover:bg-teal-50 hover:text-teal-700 hover:border-teal-200",
                          savingCP ? "opacity-60 cursor-not-allowed" : "",
                        ].join(" ")}
                      >
                        {selected ? "Path selected ✓" : "Choose this path"}
                      </button>
                      {details && (
                        <button
                          onClick={() => setExpandedId(expanded ? null : cp.id)}
                          className="px-3 py-2.5 rounded-xl text-sm font-semibold text-slate-500 border border-slate-200 hover:bg-slate-50 transition whitespace-nowrap"
                        >
                          {expanded ? "Hide ↑" : "See details ↓"}
                        </button>
                      )}
                    </div>
                  </div>

                  {expanded && details && (
                    <div className="border-t border-slate-100 px-5 pb-5 pt-4 bg-slate-50 rounded-b-2xl">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">Ce que vous apprendrez à faire</div>
                          <ul className="space-y-1.5">
                            {details.tasks.map((t) => (
                              <li key={t} className="flex items-start gap-2 text-sm text-slate-600">
                                <span className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5 shrink-0" />{t}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <div className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">Ce que vous produirez</div>
                          <ul className="space-y-1.5">
                            {details.deliverables.map((d) => (
                              <li key={d} className="flex items-center gap-2 text-sm text-slate-600 bg-white border border-slate-200 rounded-lg px-2.5 py-1.5">
                                <span className="text-xs">📄</span>
                                <span className="font-medium">{d}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* STEP 2 — Assessment */}
        <section>
          <div className="mb-5">
            <h2 className="text-base font-semibold text-slate-900">
              <span className={[
                "inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold mr-2",
                selectedId ? "bg-teal-600 text-white" : "bg-slate-200 text-slate-400",
              ].join(" ")}>2</span>
              Assess your current AI skills
            </h2>
            <p className="text-sm text-slate-400 mt-1 ml-8">A 10-question assessment to personalize your path. Takes about 5 minutes.</p>
          </div>

          {!selectedId ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 text-center">
              <div className="text-slate-300 text-3xl mb-3">🔒</div>
              <div className="text-slate-500 text-sm">Select your role first to access the assessment.</div>
            </div>
          ) : loadingQ ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200">
              <div className="animate-pulse space-y-3">
                <div className="h-4 bg-slate-200 rounded w-1/2" />
                <div className="h-16 bg-slate-200 rounded-xl" />
                <div className="h-16 bg-slate-200 rounded-xl" />
              </div>
            </div>
          ) : !questionnaire ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 text-slate-500 text-sm">No questionnaire loaded.</div>
          ) : (
            <div className="space-y-6">
              <div className="bg-white p-4 rounded-2xl border border-slate-200">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-500">Progress</span>
                  <span className="font-bold text-slate-900">{answeredCount} / {totalQuestions}</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-2 rounded-full bg-teal-500 transition-all duration-500"
                    style={{ width: `${totalQuestions > 0 ? (answeredCount / totalQuestions) * 100 : 0}%` }} />
                </div>
              </div>

              {questionnaire.skills.map((skill) => {
                const answeredInSkill = skill.questions.filter((q) => answers[q.id] !== undefined).length;
                const skillComplete = answeredInSkill === skill.questions.length;
                return (
                  <div key={skill.id} className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="px-6 pt-6 pb-4 flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-base font-bold text-slate-900">{skill.name}</h3>
                        {skill.description && <p className="text-sm text-slate-400 mt-0.5">{skill.description}</p>}
                      </div>
                      <span className={["text-xs font-bold px-2.5 py-1 rounded-full shrink-0",
                        skillComplete ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-400"].join(" ")}>
                        {answeredInSkill}/{skill.questions.length}
                      </span>
                    </div>
                    <div className="px-6 mb-4">
                      <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                        <div className={`h-1 rounded-full transition-all duration-400 ${skillComplete ? "bg-teal-400" : "bg-teal-300"}`}
                          style={{ width: `${skill.questions.length > 0 ? (answeredInSkill / skill.questions.length) * 100 : 0}%` }} />
                      </div>
                    </div>
                    <div className="divide-y divide-slate-100">
                      {skill.questions.map((q, idx) => {
                        const selected = answers[q.id];
                        return (
                          <div key={q.id} className="px-6 py-5">
                            <p className="text-sm font-medium text-slate-800 leading-relaxed mb-4">
                              <span className="text-slate-400 font-medium mr-2">{idx + 1}.</span>{q.text}
                            </p>
                            <div className="space-y-2">
                              {OPTION_KEYS.map((key) => {
                                const active = selected === key;
                                const optionText = q[OPTION_LABELS[key]];
                                if (!optionText) return null;
                                return (
                                  <button key={key} type="button" onClick={() => setAnswer(q.id, key)}
                                    className={["w-full text-left px-4 py-3 rounded-xl border transition-all duration-150 flex items-start gap-3",
                                      active ? "bg-teal-600 border-teal-600 text-white shadow-sm" : "bg-white border-slate-200 text-slate-600 hover:border-teal-300 hover:bg-teal-50"].join(" ")}>
                                    <span className={["shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border",
                                      active ? "bg-white text-teal-600 border-white" : "bg-slate-100 text-slate-500 border-slate-200"].join(" ")}>
                                      {key}
                                    </span>
                                    <span className="text-sm leading-relaxed">{optionText}</span>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}

              <div className="sticky bottom-4 bg-white border border-slate-200 px-6 py-4 rounded-2xl shadow-lg flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <div className="text-sm text-slate-600">
                    <span className="font-bold text-slate-900">{answeredCount}</span>
                    <span className="text-slate-400"> / {totalQuestions} questions answered</span>
                  </div>
                  {isComplete
                    ? <div className="text-xs text-teal-600 font-semibold mt-0.5">✓ Assessment complete — ready to submit</div>
                    : <div className="text-xs text-slate-400 mt-0.5">Answer all questions to generate your path.</div>
                  }
                </div>
                <button onClick={handleSubmit} disabled={!isComplete || submitting}
                  className={["px-6 py-3 rounded-xl font-bold text-sm text-white transition-all duration-200 whitespace-nowrap",
                    isComplete && !submitting ? "bg-teal-600 hover:bg-teal-700 shadow-sm hover:-translate-y-0.5" : "bg-slate-300 cursor-not-allowed"].join(" ")}>
                  {submitting ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                      </svg>
                      Generating...
                    </span>
                  ) : "Generate my personalized path →"}
                </button>
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}