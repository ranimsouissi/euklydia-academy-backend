import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API = process.env.REACT_APP_API_URL;

// Mapping score → profil IA (mêmes seuils que assessment_rules.py)
function getAIProfile(globalScore) {
  if (globalScore === null || globalScore === undefined) return "—";
  if (globalScore <= 49) return "Novice IA";
  if (globalScore <= 74) return "Praticien IA";
  return "Leader IA";
}

export default function ProfilePage() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState({
    fullName: "",
    email: "",
    role: "",
    company: "Euklydia Academy",
  });
  const [assessmentData, setAssessmentData] = useState({
    status: "—",
    globalScore: null,
    aiProfile: "—",
  });
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState("");
  const [saving, setSaving] = useState(false);

  // Charger profil + assessment status
  useEffect(() => {
    const loadAll = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/auth", { replace: true });
        return;
      }

      try {
        // 1. Profil user
        const meRes = await fetch(`${API}/api/v1/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!meRes.ok) throw new Error("Failed to load profile");
        const me = await meRes.json();
        setProfile({
          fullName: me.full_name || "Utilisateur",
          email: me.email || "",
          role: me.career_path || "—",   // ← affiche "AI Sales Specialist"
          company: "Euklydia Academy",
        });
        localStorage.setItem("auth_user", JSON.stringify(me));

        // 2. Assessment status (pour le vrai niveau)
        const statusRes = await fetch(`${API}/api/v1/assessment/status`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (statusRes.ok) {
          const st = await statusRes.json();
          const score = st.global_score_percent;
          setAssessmentData({
            status: st.has_scores ? "Completed" : "Not started",
            globalScore: score,
            aiProfile: getAIProfile(score),
          });
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    loadAll();
  }, [navigate]);

  const startEdit = () => {
    setEditedName(profile.fullName);
    setIsEditing(true);
  };

  const cancelEdit = () => {
    setIsEditing(false);
    setEditedName("");
  };

  const saveName = async () => {
    const trimmed = editedName.trim();
    if (trimmed.length < 2) {
      alert("Le nom doit contenir au moins 2 caractères");
      return;
    }

    setSaving(true);
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API}/api/v1/auth/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ full_name: trimmed }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Échec de la mise à jour");
      }

      const updated = await res.json();
      setProfile((p) => ({ ...p, fullName: updated.full_name }));
      localStorage.setItem("auth_user", JSON.stringify(updated));
      setIsEditing(false);
    } catch (e) {
      alert(e.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 p-10 text-slate-500">
        Chargement du profil...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <section className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-50 p-6 shadow-sm">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-3 inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                Account and learning context
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-euk-dark md:text-3xl">Profile</h1>
              <p className="mt-2 text-sm leading-6 text-slate-600 md:text-base">
                View and edit your personal information and learning context.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => navigate("/assessment")}
                className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
              >
                Retake Assessment
              </button>
            </div>
          </div>
        </section>

        {/* Top summary — 4 cartes */}
        <section className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-medium text-slate-500">Role</div>
            <div className="mt-3 text-xl font-bold tracking-tight text-euk-dark">{profile.role}</div>
            <div className="mt-3 text-sm text-slate-500">Current learning profile used for recommendations.</div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-medium text-slate-500">Assessment Status</div>
            <div className="mt-3 text-xl font-bold tracking-tight text-euk-dark">{assessmentData.status}</div>
            <div className="mt-3 text-sm text-slate-500">Latest assessment state used to generate your insights.</div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-medium text-slate-500">AI Profile</div>
            <div className="mt-3 text-xl font-bold tracking-tight text-euk-dark">{assessmentData.aiProfile}</div>
            <div className="mt-3 text-sm text-slate-500">
              {assessmentData.globalScore !== null
                ? `Based on your global score of ${assessmentData.globalScore}%.`
                : "Complete your assessment to define your AI profile."}
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="text-sm font-medium text-slate-500">Roadmap Cycle</div>
            <div className="mt-3 text-xl font-bold tracking-tight text-euk-dark">90 days</div>
            <div className="mt-3 text-sm text-slate-500">Recommended duration before reassessment.</div>
          </div>
        </section>

        {/* Personal Information */}
        <section className="mt-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-lg font-bold text-euk-dark">Personal Information</h2>
                <p className="mt-1 text-sm text-slate-500">Your account details and current platform identity.</p>
              </div>
              {!isEditing && (
                <button
                  onClick={startEdit}
                  className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
                >
                  Modifier
                </button>
              )}
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {/* Full Name — éditable */}
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Full Name</div>
                {isEditing ? (
                  <div className="mt-2 flex flex-col gap-2 sm:flex-row">
                    <input
                      type="text"
                      value={editedName}
                      onChange={(e) => setEditedName(e.target.value)}
                      className="flex-1 rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-euk-dark outline-none focus:border-emerald-500"
                      placeholder="Votre nom complet"
                      autoFocus
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={saveName}
                        disabled={saving}
                        className="rounded-xl bg-euk-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-euk-deep disabled:opacity-50"
                      >
                        {saving ? "..." : "Enregistrer"}
                      </button>
                      <button
                        onClick={cancelEdit}
                        disabled={saving}
                        className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
                      >
                        Annuler
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-2 text-sm font-medium text-euk-dark">{profile.fullName}</div>
                )}
              </div>

              {/* Email */}
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Email</div>
                <div className="mt-2 text-sm font-medium text-euk-dark">{profile.email}</div>
              </div>

              {/* Role */}
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Role</div>
                <div className="mt-2 text-sm font-medium text-euk-dark">{profile.role}</div>
              </div>

              {/* Organization */}
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">Organization</div>
                <div className="mt-2 text-sm font-medium text-euk-dark">{profile.company}</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}