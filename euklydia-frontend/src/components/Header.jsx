// src/components/Header.jsx
import { useNavigate } from "react-router-dom";
import Logo from "../assets/images/logo-full.png";
import PageContainer from "./PageContainer";

export default function Header() {
  const navigate = useNavigate();
  const goToAuth = () => navigate("/auth");

  const navItems = [
    { label: "Platform", href: "#platform" },
    { label: "How it works", href: "#how" },
    { label: "Roles", href: "#paths" },
    { label: "AI Diagnostic", action: goToAuth },
  ];

  const handleNavClick = (e, item) => {
    if (item.action) {
      e.preventDefault();
      item.action();
      return;
    }
    const id = item.href?.replace("#", "");
    const el = id ? document.getElementById(id) : null;
    if (el) {
      e.preventDefault();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-100">
      <PageContainer>
        <div className="flex items-center justify-between gap-8 py-5">
          {/* Logo — décalé à gauche pour compenser le padding transparent du PNG */}
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

          {/* Nav items */}
          <nav className="hidden md:flex items-center gap-10">
            {navItems.map((item) => (
              <a
                key={item.label}
                href={item.href || "#"}
                onClick={(e) => handleNavClick(e, item)}
                className="text-base lg:text-lg font-bold text-euk-dark hover:text-euk-primary transition-colors"
              >
                {item.label}
              </a>
            ))}
          </nav>

          {/* CTA */}
          <button
            type="button"
            onClick={goToAuth}
            className="shrink-0 rounded-2xl bg-euk-primary px-7 py-3.5 text-base lg:text-lg font-bold text-white shadow-card transition hover:bg-euk-deep hover:shadow-elevated"
          >
            Get Started
          </button>
        </div>
      </PageContainer>
    </header>
  );
}