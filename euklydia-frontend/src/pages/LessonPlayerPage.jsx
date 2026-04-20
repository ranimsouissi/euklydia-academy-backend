import { useEffect, useState } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";
import { apiFetch } from "../utils/api";

export default function LessonPlayerPage() {
  const { moduleId, unitId, lessonId } = useParams();
  const navigate = useNavigate();
  const { language } = useOutletContext();

  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Quiz state
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(null);

  // Exercise state
  const [exerciseResponse, setExerciseResponse] = useState("");
  const [exerciseSubmitted, setExerciseSubmitted] = useState(false);
  const [exerciseFeedback, setExerciseFeedback] = useState(null);
  const [exerciseLoading, setExerciseLoading] = useState(false);

  // Steps state
  const [completedSteps, setCompletedSteps] = useState({});

  // Activity navigation
  const [activeActivityIdx, setActiveActivityIdx] = useState(0);

  // Hint state
  const [hintLevel, setHintLevel] = useState(0);
  const [hintsUsed, setHintsUsed] = useState(0);

  // Video watched state
  const [videoWatched, setVideoWatched] = useState(false);

  // Forum state
  const [forumResponse, setForumResponse] = useState("");
  const [forumSubmitted, setForumSubmitted] = useState(false);

  const lang = language || "fr";

  const t = {
    en: {
      loading: "Loading lesson...",
      back: "Back to module",
      notFound: "Lesson not found",
      notFoundDesc: "This lesson could not be loaded.",
      video: "Video",
      quiz: "Quiz",
      exercise: "Exercise",
      tutorial: "Tutorial",
      case_study: "Case Study",
      forum_discussion: "Forum",
      prompt_practice: "Prompt Practice",
      quizIntro: "Answer all questions to validate your understanding.",
      quizSubmit: "Submit",
      quizRetry: "Retry",
      quizScore: "Your score",
      quizCorrect: "correct",
      quizPassed: "Well done! Quiz passed.",
      quizFailed: "Review the lesson and try again.",
      quizAnswerAll: "Please answer all questions before submitting.",
      exercisePlaceholder: "Write your answer here...",
      exerciseSubmit: "Submit answer",
      exerciseSubmitting: "Submitting...",
      exerciseSubmitted: "Answer submitted",
      forumPlaceholder: "Share your thoughts (minimum 5 lines)...",
      forumSubmit: "Post contribution",
      forumSubmitted: "Contribution posted ✓",
      nextActivity: "Next",
      prevActivity: "Previous",
      nextLesson: "Next lesson",
      backToModule: "Back to module",
      completed: "Completed",
      assessed: "Assessed",
      required: "Required",
      passingScore: "Passing score",
      showHint: "Show hint",
      nextHint: "Next hint",
      hint: "Hint",
      min: "min",
      difficulty: "Level",
      step: "Step",
      stepsCompleted: "steps completed",
      activityOf: "of",
      videoInstruction: "Watch this video carefully before moving to the next activity.",
      tutorialInstruction: "Follow each step of this tutorial carefully.",
      markWatched: "Mark as watched",
      watched: "Watched ✓",
      duration: "Duration",
    },
    fr: {
      loading: "Chargement de la leçon...",
      back: "Retour au module",
      notFound: "Leçon introuvable",
      notFoundDesc: "Cette leçon n'a pas pu être chargée.",
      video: "Vidéo",
      quiz: "Quiz",
      exercise: "Exercice",
      tutorial: "Tutoriel",
      case_study: "Cas pratique",
      forum_discussion: "Forum",
      prompt_practice: "Prompts",
      quizIntro: "Répondez à toutes les questions pour valider votre compréhension.",
      quizSubmit: "Soumettre",
      quizRetry: "Réessayer",
      quizScore: "Votre score",
      quizCorrect: "correctes",
      quizPassed: "Bravo ! Quiz réussi.",
      quizFailed: "Relisez la leçon et réessayez.",
      quizAnswerAll: "Veuillez répondre à toutes les questions avant de soumettre.",
      exercisePlaceholder: "Rédigez votre réponse ici...",
      exerciseSubmit: "Soumettre ma réponse",
      exerciseSubmitting: "Envoi en cours...",
      exerciseSubmitted: "Réponse soumise ✓",
      forumPlaceholder: "Partagez votre contribution (minimum 5 lignes)...",
      forumSubmit: "Poster ma contribution",
      forumSubmitted: "Contribution postée ✓",
      nextActivity: "Suivant",
      prevActivity: "Précédent",
      nextLesson: "Leçon suivante",
      backToModule: "Retour au module",
      completed: "Complété",
      assessed: "Évalué",
      required: "Requis",
      passingScore: "Score minimum",
      showHint: "Afficher un indice",
      nextHint: "Indice suivant",
      hint: "Indice",
      min: "min",
      difficulty: "Niveau",
      step: "Étape",
      stepsCompleted: "étapes complétées",
      activityOf: "sur",
      videoInstruction: "Regardez attentivement cette vidéo avant de passer à l'activité suivante.",
      tutorialInstruction: "Suivez chaque étape de ce tutoriel attentivement.",
      markWatched: "Marquer comme vu",
      watched: "Vu ✓",
      duration: "Durée",
    },
  };

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await apiFetch(`/api/v1/lessons/${lessonId}`);
        if (!res) return;
        if (!res.ok) { setError(t[lang].notFoundDesc); return; }
        const data = await res.json();
        setLesson(data);
      } catch {
        setError(t[lang].notFoundDesc);
      } finally {
        setLoading(false);
      }
    })();
  }, [lessonId, lang]);

  // ── Helpers ───────────────────────────────────────────────────────────────

  const activities = lesson?.activities || [];
  const currentActivity = activities[activeActivityIdx];

  const lessonTitle = lang === "fr"
    ? lesson?.title_fr || lesson?.title_en
    : lesson?.title_en || lesson?.title_fr;

  const formatLabel = (type) => t[lang][type] || type;

  const formatColor = (type) => {
    const colors = {
      video: "border-sky-200 bg-sky-50 text-sky-700",
      quiz: "border-violet-200 bg-violet-50 text-violet-700",
      exercise: "border-amber-200 bg-amber-50 text-amber-700",
      tutorial: "border-teal-200 bg-teal-50 text-teal-700",
      case_study: "border-rose-200 bg-rose-50 text-rose-700",
      forum_discussion: "border-indigo-200 bg-indigo-50 text-indigo-700",
      prompt_practice: "border-orange-200 bg-orange-50 text-orange-700",
    };
    return colors[type] || "border-slate-200 bg-slate-50 text-slate-700";
  };

  const difficultyDots = (level) =>
    Array.from({ length: 5 }, (_, i) => (
      <span
        key={i}
        className={`inline-block h-2 w-2 rounded-full ${
          i < level ? "bg-euk-primary" : "bg-slate-200"
        }`}
      />
    ));

  // ── Submit quiz ───────────────────────────────────────────────────────────

  const submitQuiz = async () => {
    if (!currentActivity?.content_fr?.questions) return;
    const questions = lang === "fr"
      ? currentActivity.content_fr?.questions
      : currentActivity.content_en?.questions || currentActivity.content_fr?.questions;

    if (Object.keys(quizAnswers).length < questions.length) return;

    let correct = 0;
    questions.forEach((q, idx) => {
      const userAnswer = quizAnswers[idx];
      const correctAnswer = q.correct;
      const optionLetters = ["A", "B", "C", "D"];
      const correctLetter = typeof correctAnswer === "number"
        ? optionLetters[correctAnswer]
        : correctAnswer;
      const userLetter = typeof userAnswer === "number"
        ? optionLetters[userAnswer]
        : userAnswer;
      if (userLetter === correctLetter) correct++;
    });

    setQuizScore(correct);
    setQuizSubmitted(true);

    try {
      await apiFetch(`/api/v1/activities/${currentActivity.id}/submit`, {
        method: "POST",
        body: JSON.stringify({
          score: Math.round((correct / questions.length) * 100),
          answers: quizAnswers,
          status: correct >= Math.ceil(questions.length * 0.7) ? "passed" : "failed",
        }),
      });
    } catch { /* non-blocking */ }
  };

  // ── Submit exercise ───────────────────────────────────────────────────────

  const submitExercise = async () => {
    if (!exerciseResponse.trim()) return;
    try {
      setExerciseLoading(true);
      const res = await apiFetch(`/api/v1/activities/${currentActivity.id}/submit`, {
        method: "POST",
        body: JSON.stringify({
          learner_response: exerciseResponse,
          status: "submitted",
        }),
      });
      if (res?.ok) {
        const data = await res.json().catch(() => ({}));
        setExerciseFeedback(
          lang === "fr"
            ? data.llm_feedback_fr || data.feedback || null
            : data.llm_feedback_en || data.feedback || null
        );
        setExerciseSubmitted(true);
      }
    } catch { /* non-blocking */ }
    finally { setExerciseLoading(false); }
  };

  // ── Submit forum ──────────────────────────────────────────────────────────

  const submitForum = async () => {
    if (!forumResponse.trim()) return;
    try {
      await apiFetch(`/api/v1/activities/${currentActivity.id}/submit`, {
        method: "POST",
        body: JSON.stringify({ learner_response: forumResponse, status: "submitted" }),
      });
      setForumSubmitted(true);
    } catch { /* non-blocking */ }
  };

  // ── ✅ Mark video watched — tracking en BDD ───────────────────────────────

  const markVideoWatched = async (activity) => {
    setVideoWatched(true);
    try {
      await apiFetch(`/api/v1/activities/${activity.id}/submit`, {
        method: "POST",
        body: JSON.stringify({ status: "completed" }),
      });
    } catch { /* non-blocking */ }
  };

  // ── ✅ Complete lesson — tracking en BDD ──────────────────────────────────

  const completeLesson = async () => {
    try {
      await apiFetch(`/api/v1/lessons/${lessonId}/complete`, {
        method: "POST",
      });
    } catch { /* non-blocking */ }
    navigate(`/learning/module/${moduleId}/units`);
  };

  // ── Activity renderers ────────────────────────────────────────────────────

  const renderVideo = (activity) => {
    const content = lang === "fr" ? activity.content_fr : activity.content_en || activity.content_fr;
    const url = lang === "fr"
      ? lesson?.video_url_fr || content?.url_fr || content?.url
      : lesson?.video_url_en || content?.url_en || content?.url_fr || content?.url;
    const duration = content?.duration_min;

    return (
      <div className="space-y-4">
        <div className="rounded-2xl border border-sky-100 bg-sky-50 px-4 py-3">
          <p className="text-sm text-sky-800">{t[lang].videoInstruction}</p>
        </div>

        {duration && (
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <span>⏱</span>
            <span>{t[lang].duration} : {duration} {t[lang].min}</span>
          </div>
        )}

        {url ? (
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-900">
            {url.includes("youtube.com") || url.includes("youtu.be") ? (
              <iframe
                src={`https://www.youtube.com/embed/${url.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/)?.[1]}`}
                className="w-full rounded-2xl"
                style={{ aspectRatio: "16/9" }}
                allowFullScreen
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                title={activity.title_fr || "Video"}
              />
            ) : (
              <video controls className="w-full rounded-2xl">
                <source src={`http://localhost:8000${url}`} type="video/mp4" />
              </video>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50 py-16">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-sky-100 text-2xl text-sky-600">▶</div>
            <p className="text-sm font-semibold text-slate-600">
              {activity.title_fr || t[lang].video}
            </p>
            {duration && (
              <span className="rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-semibold text-sky-700">
                {duration} {t[lang].min}
              </span>
            )}
            <p className="text-xs text-slate-400">Vidéo disponible prochainement</p>
          </div>
        )}

        {/* ✅ markVideoWatched trackée en BDD */}
        <button
          onClick={() => markVideoWatched(activity)}
          className={`w-full rounded-2xl border px-4 py-3 text-sm font-semibold transition ${
            videoWatched
              ? "border-emerald-200 bg-emerald-50 text-emerald-700"
              : "border-slate-200 bg-white text-euk-dark hover:bg-slate-50"
          }`}
        >
          {videoWatched ? t[lang].watched : t[lang].markWatched}
        </button>
      </div>
    );
  };

  const renderQuiz = (activity) => {
    const questions = lang === "fr"
      ? activity.content_fr?.questions
      : activity.content_en?.questions || activity.content_fr?.questions;
    const hints = lang === "fr" ? activity.hints_fr : activity.hints_en || activity.hints_fr;

    if (!questions?.length) return (
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center text-sm text-slate-500">
        Quiz en cours de préparation
      </div>
    );

    const passThreshold = Math.ceil(questions.length * 0.7);
    const passed = quizSubmitted && quizScore >= passThreshold;

    return (
      <div className="space-y-5">
        <p className="text-sm text-slate-500">{t[lang].quizIntro}</p>

        {quizSubmitted && quizScore !== null && (
          <div className={`rounded-2xl border p-4 text-sm font-semibold ${
            passed
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-amber-200 bg-amber-50 text-amber-800"
          }`}>
            <div className="text-lg">
              {t[lang].quizScore}: {quizScore}/{questions.length} {t[lang].quizCorrect}
            </div>
            <div className="mt-1 text-sm font-normal">
              {passed ? t[lang].quizPassed : t[lang].quizFailed}
            </div>
          </div>
        )}

        <div className="space-y-5">
          {questions.map((q, idx) => {
            const optionLetters = ["A", "B", "C", "D"];
            const selected = quizAnswers[idx];
            const correctAnswer = typeof q.correct === "number"
              ? optionLetters[q.correct]
              : q.correct;

            return (
              <div
                key={idx}
                className={`rounded-2xl border p-4 transition ${
                  quizSubmitted
                    ? typeof selected !== "undefined" && optionLetters[selected] === correctAnswer
                      ? "border-emerald-200 bg-emerald-50"
                      : "border-rose-200 bg-rose-50"
                    : "border-slate-200 bg-slate-50"
                }`}
              >
                <p className="text-sm font-semibold text-slate-800">
                  {idx + 1}. {q.question}
                </p>
                <div className="mt-3 space-y-2">
                  {q.options.map((option, oIdx) => {
                    const letter = optionLetters[oIdx];
                    const isSelected = selected === oIdx;
                    const isCorrect = quizSubmitted && letter === correctAnswer;
                    const isWrong = quizSubmitted && isSelected && letter !== correctAnswer;
                    return (
                      <button
                        key={oIdx}
                        onClick={() => !quizSubmitted && setQuizAnswers(p => ({ ...p, [idx]: oIdx }))}
                        disabled={quizSubmitted}
                        className={[
                          "w-full rounded-xl border px-4 py-2.5 text-left text-sm transition",
                          isCorrect
                            ? "border-emerald-300 bg-emerald-100 text-emerald-800 font-semibold"
                            : isWrong
                            ? "border-rose-300 bg-rose-100 text-rose-800"
                            : isSelected
                            ? "border-euk-primary bg-euk-primary/10 text-euk-dark font-semibold"
                            : "border-slate-200 bg-white text-slate-600 hover:bg-slate-100",
                        ].join(" ")}
                      >
                        {option}
                      </button>
                    );
                  })}
                </div>
                {quizSubmitted && q.explanation && (
                  <p className="mt-3 text-xs text-slate-600 border-l-2 border-slate-300 pl-3">
                    {q.explanation}
                  </p>
                )}
              </div>
            );
          })}
        </div>

        {!quizSubmitted && hints?.length > 0 && hintLevel < hints.length && (
          <button
            onClick={() => { setHintLevel(h => h + 1); setHintsUsed(h => h + 1); }}
            className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-2.5 text-sm font-semibold text-amber-700 transition hover:bg-amber-100"
          >
            {hintLevel === 0 ? t[lang].showHint : t[lang].nextHint}
          </button>
        )}
        {hintLevel > 0 && hints?.slice(0, hintLevel).map((hint, i) => (
          <div key={i} className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-amber-600">
              {t[lang].hint} {hint.level}
            </p>
            <p className="mt-1 text-sm text-amber-900">{hint.text}</p>
          </div>
        ))}

        <div className="flex gap-3">
          {!quizSubmitted ? (
            <button
              onClick={submitQuiz}
              disabled={Object.keys(quizAnswers).length < questions.length}
              className="rounded-2xl bg-euk-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep disabled:cursor-not-allowed disabled:opacity-50"
            >
              {t[lang].quizSubmit}
            </button>
          ) : (
            <button
              onClick={() => { setQuizAnswers({}); setQuizSubmitted(false); setQuizScore(null); setHintLevel(0); }}
              className="rounded-2xl border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
            >
              {t[lang].quizRetry}
            </button>
          )}
        </div>
      </div>
    );
  };

  const renderExercise = (activity) => {
    const content = lang === "fr" ? activity.content_fr : activity.content_en || activity.content_fr;
    const rubric = lang === "fr" ? activity.rubric_fr : activity.rubric_en || activity.rubric_fr;
    const hints = lang === "fr" ? activity.hints_fr : activity.hints_en || activity.hints_fr;
    const steps = content?.steps;
    const totalSteps = steps?.length || 0;
    const doneSteps = Object.values(completedSteps).filter(Boolean).length;

    return (
      <div className="space-y-5">
        {content?.consigne && (
          <div className="rounded-2xl border border-amber-100 bg-amber-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-amber-600 mb-2">Consigne</p>
            <p className="text-sm leading-6 text-amber-900 whitespace-pre-line">{content.consigne}</p>
          </div>
        )}

        {steps?.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
              <span>{t[lang].step}</span>
              <span>{doneSteps}/{totalSteps} {t[lang].stepsCompleted}</span>
            </div>
            {steps.map((step, idx) => (
              <div
                key={idx}
                onClick={() => setCompletedSteps(p => ({ ...p, [idx]: !p[idx] }))}
                className={`flex cursor-pointer gap-4 rounded-2xl border p-4 transition ${
                  completedSteps[idx]
                    ? "border-emerald-200 bg-emerald-50"
                    : "border-slate-200 bg-white hover:border-euk-primary/30 hover:bg-euk-primary/5"
                }`}
              >
                <div className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
                  completedSteps[idx]
                    ? "bg-emerald-500 text-white"
                    : "bg-slate-100 text-slate-600"
                }`}>
                  {completedSteps[idx] ? "✓" : idx + 1}
                </div>
                <p className={`text-sm leading-6 ${
                  completedSteps[idx] ? "text-emerald-700 line-through" : "text-slate-700"
                }`}>
                  {step}
                </p>
              </div>
            ))}
          </div>
        )}

        {content?.livrable && (
          <div className="rounded-2xl border border-violet-100 bg-violet-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-violet-600 mb-1">Livrable</p>
            <p className="text-sm text-violet-900">{content.livrable}</p>
          </div>
        )}

        {rubric?.criteres?.length > 0 && (
          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-3">Grille d'évaluation</p>
            <div className="space-y-2">
              {rubric.criteres.map((c, i) => (
                <div key={i} className="flex items-start justify-between gap-3 text-sm">
                  <span className="text-slate-700">{c.nom}</span>
                  <span className="shrink-0 rounded-full border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs font-semibold text-slate-600">
                    {Math.round(c.poids * 100)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {!exerciseSubmitted ? (
          <div className="space-y-3">
            <textarea
              value={exerciseResponse}
              onChange={(e) => setExerciseResponse(e.target.value)}
              placeholder={t[lang].exercisePlaceholder}
              rows={6}
              className="w-full rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-euk-primary focus:ring-1 focus:ring-euk-primary"
            />

            {hints?.length > 0 && hintLevel < hints.length && (
              <button
                onClick={() => { setHintLevel(h => h + 1); setHintsUsed(h => h + 1); }}
                className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700 transition hover:bg-amber-100"
              >
                {hintLevel === 0 ? t[lang].showHint : t[lang].nextHint}
              </button>
            )}
            {hintLevel > 0 && hints?.slice(0, hintLevel).map((hint, i) => (
              <div key={i} className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-amber-600">
                  {t[lang].hint} {hint.level}
                </p>
                <p className="mt-1 text-sm text-amber-900">{hint.text}</p>
              </div>
            ))}

            <button
              onClick={submitExercise}
              disabled={!exerciseResponse.trim() || exerciseLoading}
              className="rounded-2xl bg-euk-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep disabled:cursor-not-allowed disabled:opacity-50"
            >
              {exerciseLoading ? t[lang].exerciseSubmitting : t[lang].exerciseSubmit}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
              <p className="text-sm font-semibold text-emerald-700">{t[lang].exerciseSubmitted}</p>
            </div>
            {exerciseFeedback && (
              <div className="rounded-2xl border border-violet-200 bg-violet-50 p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-violet-600 mb-2">Feedback</p>
                <p className="text-sm leading-6 text-violet-900 whitespace-pre-line">{exerciseFeedback}</p>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  const renderForum = (activity) => {
    const content = lang === "fr" ? activity.content_fr : activity.content_en || activity.content_fr;
    return (
      <div className="space-y-4">
        {content?.question && (
          <div className="rounded-2xl border border-indigo-100 bg-indigo-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600 mb-2">Sujet</p>
            <p className="text-sm leading-6 text-indigo-900">{content.question}</p>
          </div>
        )}
        {content?.consigne && (
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">Consigne</p>
            <p className="text-sm text-slate-700 whitespace-pre-line">{content.consigne}</p>
          </div>
        )}
        {!forumSubmitted ? (
          <div className="space-y-3">
            <textarea
              value={forumResponse}
              onChange={(e) => setForumResponse(e.target.value)}
              placeholder={t[lang].forumPlaceholder}
              rows={8}
              className="w-full rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-euk-primary focus:ring-1 focus:ring-euk-primary"
            />
            <button
              onClick={submitForum}
              disabled={!forumResponse.trim()}
              className="rounded-2xl bg-euk-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep disabled:cursor-not-allowed disabled:opacity-50"
            >
              {t[lang].forumSubmit}
            </button>
          </div>
        ) : (
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
            <p className="text-sm font-semibold text-emerald-700">{t[lang].forumSubmitted}</p>
          </div>
        )}
      </div>
    );
  };

  const renderTutorial = (activity) => {
    const content = lang === "fr" ? activity.content_fr : activity.content_en || activity.content_fr;
    const steps = content?.steps;
    const totalSteps = steps?.length || 0;
    const doneSteps = Object.values(completedSteps).filter(Boolean).length;

    return (
      <div className="space-y-4">
        <div className="rounded-2xl border border-teal-100 bg-teal-50 px-4 py-3">
          <p className="text-sm text-teal-800">{t[lang].tutorialInstruction}</p>
        </div>
        {steps?.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
              <span>{t[lang].step}</span>
              <span>{doneSteps}/{totalSteps} {t[lang].stepsCompleted}</span>
            </div>
            {steps.map((step, idx) => (
              <div
                key={idx}
                onClick={() => setCompletedSteps(p => ({ ...p, [idx]: !p[idx] }))}
                className={`flex cursor-pointer gap-4 rounded-2xl border p-4 transition ${
                  completedSteps[idx]
                    ? "border-teal-200 bg-teal-50"
                    : "border-slate-200 bg-white hover:border-teal-300 hover:bg-teal-50/50"
                }`}
              >
                <div className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-xl text-xs font-bold ${
                  completedSteps[idx] ? "bg-teal-500 text-white" : "bg-slate-100 text-slate-600"
                }`}>
                  {completedSteps[idx] ? "✓" : idx + 1}
                </div>
                <p className={`text-sm leading-6 ${
                  completedSteps[idx] ? "text-teal-700 line-through" : "text-slate-700"
                }`}>{step}</p>
              </div>
            ))}
          </div>
        )}
        {(!steps || steps.length === 0) && content?.duration_min && (
          <div className="flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed border-teal-200 bg-teal-50 py-12">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-100 text-xl text-teal-600">◈</div>
            <p className="text-sm font-semibold text-teal-800">{activity.title_fr || t[lang].tutorial}</p>
            <span className="rounded-full border border-teal-200 bg-white px-3 py-1 text-xs font-semibold text-teal-700">
              {content.duration_min} {t[lang].min}
            </span>
          </div>
        )}
      </div>
    );
  };

  const renderCaseStudy = (activity) => {
    const content = lang === "fr" ? activity.content_fr : activity.content_en || activity.content_fr;
    const cas = content?.cas;
    return (
      <div className="space-y-5">
        {cas?.map((c, i) => (
          <div key={i} className="rounded-2xl border border-rose-100 bg-white p-5">
            <h3 className="text-sm font-bold text-euk-dark">{c.titre}</h3>
            {c.contexte && (
              <div className="mt-3 rounded-xl border border-rose-100 bg-rose-50 p-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-rose-600 mb-1">Contexte</p>
                <p className="text-sm text-rose-900">{c.contexte}</p>
              </div>
            )}
            {c.questions?.length > 0 && (
              <div className="mt-3 space-y-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Questions</p>
                {c.questions.map((q, qi) => (
                  <div key={qi} className="flex gap-2 text-sm text-slate-700">
                    <span className="shrink-0 font-bold text-rose-500">{qi + 1}.</span>
                    <span>{q}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {!exerciseSubmitted ? (
          <div className="space-y-3">
            <textarea
              value={exerciseResponse}
              onChange={(e) => setExerciseResponse(e.target.value)}
              placeholder={t[lang].exercisePlaceholder}
              rows={8}
              className="w-full rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-700 outline-none focus:border-euk-primary focus:ring-1 focus:ring-euk-primary"
            />
            <button
              onClick={submitExercise}
              disabled={!exerciseResponse.trim() || exerciseLoading}
              className="rounded-2xl bg-euk-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep disabled:cursor-not-allowed disabled:opacity-50"
            >
              {exerciseLoading ? t[lang].exerciseSubmitting : t[lang].exerciseSubmit}
            </button>
          </div>
        ) : (
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
            <p className="text-sm font-semibold text-emerald-700">{t[lang].exerciseSubmitted}</p>
            {exerciseFeedback && (
              <p className="mt-2 text-sm text-emerald-900">{exerciseFeedback}</p>
            )}
          </div>
        )}
      </div>
    );
  };

  const renderActivity = (activity) => {
    if (!activity) return null;
    switch (activity.type) {
      case "video": return renderVideo(activity);
      case "quiz": return renderQuiz(activity);
      case "exercise": return renderExercise(activity);
      case "tutorial": return renderTutorial(activity);
      case "case_study": return renderCaseStudy(activity);
      case "forum_discussion": return renderForum(activity);
      default: return renderExercise(activity);
    }
  };

  // ── Loading / Error ───────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-3xl p-6">
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

  if (!lesson || error) {
    return (
      <div className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-3xl p-6">
          <button
            onClick={() => navigate(`/learning/module/${moduleId}/units`)}
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

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-3xl p-6">

        {/* Back */}
        <button
          onClick={() => navigate(`/learning/module/${moduleId}/units`)}
          className="mb-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
        >
          ← {t[lang].back}
        </button>

        {/* Lesson Header */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${formatColor(lesson.format)}`}>
              {formatLabel(lesson.format)}
            </span>
            {lesson.estimated_duration_min && (
              <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-700">
                {lesson.estimated_duration_min} {t[lang].min}
              </span>
            )}
            <div className="flex items-center gap-1">
              {difficultyDots(lesson.difficulty_level || 1)}
            </div>
          </div>
          <h1 className="mt-3 text-xl font-bold tracking-tight text-euk-dark md:text-2xl">
            {lessonTitle}
          </h1>
          {lesson.description_fr && (
            <p className="mt-2 text-sm leading-6 text-slate-500">
              {lang === "fr" ? lesson.description_fr : lesson.description_en || lesson.description_fr}
            </p>
          )}
        </section>

        {/* Activity tabs */}
        {activities.length > 1 && (
          <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
            {activities.map((act, idx) => (
              <button
                key={act.id}
                onClick={() => {
                  setActiveActivityIdx(idx);
                  setQuizAnswers({}); setQuizSubmitted(false); setQuizScore(null);
                  setExerciseResponse(""); setExerciseSubmitted(false); setExerciseFeedback(null);
                  setForumResponse(""); setForumSubmitted(false);
                  setHintLevel(0); setCompletedSteps({});
                }}
                className={[
                  "shrink-0 rounded-2xl border px-4 py-2 text-xs font-semibold transition",
                  activeActivityIdx === idx
                    ? `${formatColor(act.type)} shadow-sm`
                    : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50",
                ].join(" ")}
              >
                {idx + 1}. {formatLabel(act.type)}
                {act.is_assessed && <span className="ml-1 text-xs opacity-60">★</span>}
              </button>
            ))}
          </div>
        )}

        {/* Activity content */}
        <section className="mt-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-5 flex items-center justify-between">
            <div className="flex items-center gap-2">
              {activities.length > 1 && (
                <span className="text-xs text-slate-400">
                  {t[lang].activityOf} {activities.length}
                </span>
              )}
              {currentActivity?.title_fr && (
                <h2 className="text-base font-bold text-euk-dark">
                  {lang === "fr" ? currentActivity.title_fr : currentActivity.title_en || currentActivity.title_fr}
                </h2>
              )}
            </div>
            <div className="flex items-center gap-2">
              {currentActivity?.is_assessed && (
                <span className="rounded-full border border-violet-200 bg-violet-50 px-2 py-0.5 text-xs font-semibold text-violet-700">
                  ★ {t[lang].assessed}
                </span>
              )}
              {currentActivity?.passing_score > 0 && (
                <span className="rounded-full border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs font-semibold text-slate-600">
                  {t[lang].passingScore} {currentActivity.passing_score}%
                </span>
              )}
            </div>
          </div>

          {renderActivity(currentActivity)}
        </section>

        {/* ✅ Navigation corrigée */}
        <div className="mt-4 flex items-center justify-between gap-3">

          {/* Bouton GAUCHE — retour simple, jamais de tracking */}
          <button
            onClick={() => {
              if (activeActivityIdx > 0) {
                setActiveActivityIdx(i => i - 1);
              } else {
                navigate(`/learning/module/${moduleId}/units`);
              }
            }}
            className="rounded-2xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
          >
            ← {activeActivityIdx > 0 ? t[lang].prevActivity : t[lang].backToModule}
          </button>

          {/* ✅ Bouton DROIT — completeLesson() uniquement sur la dernière activité */}
          <button
            onClick={() => {
              if (activeActivityIdx < activities.length - 1) {
                setActiveActivityIdx(i => i + 1);
                setQuizAnswers({}); setQuizSubmitted(false); setQuizScore(null);
                setExerciseResponse(""); setExerciseSubmitted(false); setExerciseFeedback(null);
                setForumResponse(""); setForumSubmitted(false);
                setHintLevel(0); setCompletedSteps({});
              } else {
                completeLesson(); // ✅ tracking uniquement ici
              }
            }}
            className="rounded-2xl bg-euk-primary px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-euk-deep"
          >
            {activeActivityIdx < activities.length - 1
              ? t[lang].nextActivity
              : t[lang].backToModule} →
          </button>

        </div>

      </div>
    </div>
  );
}