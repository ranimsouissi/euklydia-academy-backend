import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { logout } from "../services/auth";
import Logo from "../assets/images/logo-full.png";
import LanguageToggle from "../components/LanguageToggle";

export default function AppLayout() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [language, setLanguage] = useState(
    localStorage.getItem("language") || "en"
  );
  const menuRef = useRef(null);

  const t = {
    en: {
      commandCenter: "Command Center",
      roadmap: "AI Roadmap",
      learning: "Learning",
      myAccount: "My Account",
      profile: "Profile",
      logout: "Logout",
      logoAlt: "Euklydia Academy",
    },
    fr: {
      commandCenter: "Centre de commande",
      roadmap: "Feuille de route IA",
      learning: "Apprentissage",
      myAccount: "Mon compte",
      profile: "Profil",
      logout: "Déconnexion",
      logoAlt: "Euklydia Academy",
    },
  };

  useEffect(() => {
    localStorage.setItem("language", language);
  }, [language]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const linkClass = ({ isActive }) =>
    [
      "relative text-sm font-semibold transition-colors",
      isActive
        ? "text-euk-primary"
        : "text-slate-600 hover:text-euk-dark",
    ].join(" ");

  const userInitial = (() => {
    try {
      const raw = localStorage.getItem("auth_user");
      if (!raw) return "U";
      const user = JSON.parse(raw);
      const source = user?.first_name || user?.name || user?.email || "User";
      return String(source).charAt(0).toUpperCase();
    } catch {
      return "U";
    }
  })();

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-10">
            <button
              onClick={() => navigate("/dashboard")}
              className="flex shrink-0 items-center"
              type="button"
            >
              <img
                src={Logo}
                alt={t[language].logoAlt}
                className="h-12 w-auto object-contain"
              />
            </button>

            <nav className="hidden items-center gap-8 md:flex">
              <NavLink to="/dashboard" className={linkClass}>
                {t[language].commandCenter}
              </NavLink>

              <NavLink to="/roadmap" className={linkClass}>
                {t[language].roadmap}
              </NavLink>

              <NavLink to="/learning" className={linkClass}>
                {t[language].learning}
              </NavLink>
            </nav>
          </div>

          <div className="flex items-center gap-3">
            <LanguageToggle
              language={language}
              setLanguage={setLanguage}
            />

            <div className="relative" ref={menuRef}>
              <button
                type="button"
                onClick={() => setMenuOpen((prev) => !prev)}
                className="flex items-center gap-3 rounded-full border border-slate-200 bg-white px-3 py-2 shadow-sm transition hover:border-slate-300 hover:shadow"
              >
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-euk-primary text-sm font-bold text-white">
                  {userInitial}
                </div>
                <span className="hidden text-sm font-semibold text-slate-700 sm:block">
                  {t[language].myAccount}
                </span>
                <svg
                  className={`h-4 w-4 text-slate-500 transition-transform ${menuOpen ? "rotate-180" : ""}`}
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>

              {menuOpen && (
                <div className="absolute right-0 mt-3 w-48 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-lg">
                  <button
                    onClick={() => {
                      setMenuOpen(false);
                      navigate("/profile");
                    }}
                    className="block w-full px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                  >
                    {t[language].profile}
                  </button>

                  <button
                    onClick={() => {
                      setMenuOpen(false);
                      logout();
                      navigate("/", { replace: true });
                    }}
                    className="block w-full px-4 py-3 text-left text-sm font-medium text-rose-600 transition hover:bg-rose-50"
                  >
                    {t[language].logout}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-6">
        <Outlet context={{ language }} />
      </main>
    </div>
  );
}