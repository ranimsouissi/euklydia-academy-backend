import { useNavigate } from "react-router-dom";
import Logo from "../assets/images/logo-full.png";

export default function Header() {
  const navigate = useNavigate();
  const goToAuth = () => navigate("/auth");

  const navItems = [
    { label: "Platform", href: "#platform" },
    { label: "How it works", href: "#how" },
    { label: "Learning Paths", href: "#paths" },
    { label: "AI Assessment", action: goToAuth },
  ];

  const handleNavClick = (e, item) => {
    if (item.action) {
      e.preventDefault();
      item.action();
      return;
    }

    const id = item.href?.replace("#", "");
    const isHome = window.location.pathname === "/";

    if (isHome) {
      // On est déjà sur la landing — scroll smooth vers la section
      const el = id ? document.getElementById(id) : null;
      if (el) {
        e.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    } else {
      // On est sur une autre page — naviguer vers / puis scroller
      e.preventDefault();
      navigate("/");
      // Petit délai pour laisser la page se charger avant de scroller
      setTimeout(() => {
        const el = document.getElementById(id);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200">
      <div className="mx-auto max-w-6xl px-8 py-4 flex items-center justify-between gap-8">
        <button
          type="button"
          onClick={() => navigate("/")}
          className="flex items-center shrink-0"
        >
          <img
            src={Logo}
            alt="Euklydia Academy"
            className="h-28 w-auto object-contain"
          />
        </button>

        <nav className="hidden md:flex items-center gap-6">
          {navItems.map((item) => (
            <a
              key={item.label}
              href={item.href || "#"}
              onClick={(e) => handleNavClick(e, item)}
              className="font-extrabold text-euk-dark hover:text-euk-primary transition"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <button
          type="button"
          onClick={goToAuth}
          className="shrink-0 rounded-xl bg-euk-primary px-5 py-3 font-extrabold text-white hover:bg-euk-deep transition"
        >
          Get Started
        </button>
      </div>
    </header>
  );
}
