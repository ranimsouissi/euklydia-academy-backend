// src/components/Hero.jsx
import { useNavigate } from "react-router-dom";
import PageContainer from "./PageContainer";
import heroImage from "../assets/leaders.jpg"; // ← adapte le chemin si besoin

export default function Hero() {
  const navigate = useNavigate();

  return (
    <section className="bg-white">
      <PageContainer>
         <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center pt-6 pb-16 lg:pt-8 lg:pb-20">

          {/* ─── Colonne gauche : texte ──────────────────────────── */}
          <div className="flex flex-col">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 self-start rounded-full border border-euk-border bg-euk-soft px-4 py-2 text-sm font-semibold text-euk-primary mb-8">
              <span className="text-amber-500">⚡</span>
              Use case-driven AI learning
            </div>

            {/* Titre principal — ÉCHELLE RESPONSIVE */}
            <h1 className="text-hero-sm md:text-hero-md lg:text-hero-lg text-euk-dark">
              Master AI through real <span className="text-euk-accent">business use cases</span>.
            </h1>

            {/* Sous-titre */}
            <p className="mt-6 lg:mt-8 text-lg lg:text-xl text-slate-600 leading-relaxed max-w-xl">
              Diagnose your gaps on real use cases, follow a personalized
              pathway by role, and unlock measurable KPI improvements.
            </p>

            {/* Boutons CTA */}
            <div className="mt-10 flex flex-wrap gap-4">
              <button
                onClick={() => navigate("/auth")}
                className="rounded-2xl bg-euk-primary px-7 py-4 text-base lg:text-lg font-bold text-white shadow-card transition hover:bg-euk-deep hover:shadow-elevated"
              >
                Start free diagnostic →
              </button>
              <button
                onClick={() => {
                  document.getElementById("paths")?.scrollIntoView({ behavior: "smooth" });
                }}
                className="rounded-2xl border-2 border-euk-primary bg-white px-7 py-4 text-base lg:text-lg font-bold text-euk-primary transition hover:bg-euk-soft"
              >
                Explore roles
              </button>
            </div>

            {/* Réassurance */}
            <div className="mt-6 text-sm text-slate-500 font-medium">
              <span className="text-euk-primary">✓</span> 10 minutes
              <span className="mx-2">·</span>
              No credit card required
              <span className="mx-2">·</span>
              Instant roadmap
            </div>
          </div>

          {/* ─── Colonne droite : image ──────────────────────────── */}
          <div className="relative">
            <div className="relative rounded-3xl overflow-hidden shadow-elevated">
              <img
                src={heroImage}
                alt="AI learning session"
                className="w-full h-auto object-cover aspect-[4/3] lg:aspect-[5/4]"
              />

              {/* Badge haut-gauche */}
              <div className="absolute top-6 left-6 inline-flex items-center gap-2 rounded-full bg-white px-4 py-2 text-sm font-bold text-euk-dark shadow-card">
                <span className="h-2 w-2 rounded-full bg-euk-accent"></span>
                AI Diagnostic · 3 use cases per role
              </div>

              {/* Badge bas-droit */}
              <div className="absolute bottom-6 right-6 rounded-2xl bg-euk-primary px-5 py-3 text-white shadow-elevated">
                <div className="text-2xl font-extrabold leading-none">10 min</div>
                <div className="text-xs font-semibold opacity-90 mt-1">To your roadmap</div>
              </div>
            </div>
          </div>
        </div>
      </PageContainer>

      {/* ─── Bandeau statistiques (4 métriques) ────────────────── */}
      <PageContainer>
        <div className="border-t border-slate-100 grid grid-cols-2 lg:grid-cols-4 divide-x divide-slate-100">
          {[
            { value: "4", label: "Professional Roles", desc: "Sales · Marketing · Design · PM" },
            { value: "3", label: "Use Cases per Role", desc: "Real business scenarios" },
            { value: "9", label: "Diagnostic Questions", desc: "3 use cases × 3 questions" },
            { value: "100%", label: "Execution-driven", desc: "From diagnosis to KPI impact" },
          ].map((m) => (
            <div key={m.label} className="px-6 py-10 lg:py-14 text-center">
              <div className="text-5xl lg:text-6xl font-extrabold text-euk-primary leading-none">
                {m.value}
              </div>
              <div className="mt-3 text-base font-bold text-euk-dark">{m.label}</div>
              <div className="mt-1 text-sm text-slate-500">{m.desc}</div>
            </div>
          ))}
        </div>
      </PageContainer>
    </section>
  );
}