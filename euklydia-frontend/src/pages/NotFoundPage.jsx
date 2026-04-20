import { useNavigate } from "react-router-dom";

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="text-center max-w-md">
        <div className="text-8xl font-bold text-euk-primary">404</div>
        <h1 className="mt-4 text-2xl font-bold text-euk-dark">
          Page introuvable
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          La page que vous cherchez n'existe pas ou a été déplacée.
        </p>
        <div className="mt-8 flex gap-3 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50"
          >
            Retour
          </button>
          <button
            onClick={() => navigate("/dashboard")}
            className="rounded-2xl bg-euk-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-euk-deep"
          >
            Tableau de bord
          </button>
        </div>
      </div>
    </div>
  );
}
