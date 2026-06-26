// src/layouts/AuthLayout.jsx
//
// Layout minimaliste pour les pages d'authentification.
// Pattern UX standard (Stripe, Linear, Notion) : juste le logo,
// pour garder l'utilisateur focalisé sur le formulaire.

import { Outlet, useNavigate } from "react-router-dom";
import Logo from "../assets/images/logo-full.png";
import PageContainer from "../components/PageContainer";

export default function AuthLayout() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-euk-soft">
      {/* ─── Navbar minimaliste : juste le logo ─────────────────── */}
      <header className="bg-white/90 backdrop-blur border-b border-slate-100">
        <PageContainer>
          <div className="flex items-center justify-between py-5">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="flex items-center shrink-0 transition hover:opacity-90 -ml-4 lg:-ml-6"
            >
              <img
                src={Logo}
                alt="Euklydia Academy"
                className="h-20 lg:h-24 w-auto object-contain"
              />
            </button>

            {/* Lien de retour vers la landing (optionnel, aide à rassurer l'utilisateur) */}
            <button
              type="button"
              onClick={() => navigate("/")}
              className="text-sm lg:text-base font-semibold text-slate-500 hover:text-euk-primary transition-colors"
            >
              ← Back to home
            </button>
          </div>
        </PageContainer>
      </header>

      {/* ─── Main (formulaire centré) ───────────────────────────── */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}