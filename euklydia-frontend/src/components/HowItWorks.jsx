import { Fragment } from "react";
import Section from "./ui/Section";
import SectionHeader from "./ui/SectionHeader";

const steps = [
  {
    step: "01",
    title: "Diagnose",
    desc: "Identify your real gaps across 3 business use cases per role — no generic scoring, no guesswork.",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="#006355" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
      </svg>
    ),
    detail: "10 min · 9 questions · 3 use cases × 3 questions · Role-personalized",
  },
  {
    step: "02",
    title: "Prioritize",
    desc: "Get your personalized learning pathway instantly — focused on the use cases where you have the highest impact potential.",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="#006355" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
      </svg>
    ),
    detail: "Use case priority · Personalized pathway · Business alignment",
  },
  {
    step: "03",
    title: "Execute & Measure",
    desc: "Follow role-based modules with templates, prompts, and AI agent blueprints. Track your progress from Initial KPI to Projected KPI.",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="#006355" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
      </svg>
    ),
    detail: "Real templates · AI blueprints · Measurable KPI impact",
  },
];

function Arrow() {
  return (
    <div style={{
      display: "flex", alignItems: "center", justifyContent: "center",
      flexShrink: 0, color: "#00B3A0",
    }}>
      <svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="#00B3A0" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
      </svg>
    </div>
  );
}

export default function HowItWorks() {
  return (
    <Section id="how" bg="#F2FBF9">
      <SectionHeader
        kicker="How it works ?"
        title="A simple path from diagnostic to business impact"
      />

      <div
        style={{
          marginTop: 28,
          display: "grid",
          gridTemplateColumns: "1fr auto 1fr auto 1fr",
          gap: 0,
          alignItems: "start",
        }}
        className="howWrapper"
      >
        {steps.map((s, idx) => (
          <Fragment key={s.step}>
            <div
              style={{
                background: "#fff",
                border: "1px solid rgba(15,23,42,0.08)",
                borderRadius: 22, padding: 24,
                boxShadow: "0 18px 55px rgba(2,6,23,0.06)",
                position: "relative", overflow: "hidden",
                height: "100%",
              }}
            >
              <div style={{
                position: "absolute", inset: 0,
                background: idx === 1
                  ? "linear-gradient(180deg, rgba(0,179,160,0.10), rgba(255,255,255,0))"
                  : "linear-gradient(180deg, rgba(11,60,59,0.06), rgba(255,255,255,0))",
                pointerEvents: "none",
              }} />

              <div style={{ position: "relative" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
                  <div style={{
                    fontSize: 13, fontWeight: 900, color: "#006355",
                    background: "rgba(0,179,160,0.10)",
                    padding: "4px 10px", borderRadius: 99,
                  }}>
                    {s.step}
                  </div>
                  <div style={{
                    width: 38, height: 38, borderRadius: 10,
                    background: "rgba(0,179,160,0.10)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                  }}>
                    {s.icon}
                  </div>
                </div>

                <div style={{ fontWeight: 900, color: "#0B3C3B", fontSize: 18, marginBottom: 8 }}>
                  {s.title}
                </div>

                <div style={{ color: "#64748b", lineHeight: 1.7, fontSize: 14, marginBottom: 14 }}>
                  {s.desc}
                </div>

                <div style={{
                  fontSize: 12, fontWeight: 700, color: "#006355",
                  borderTop: "1px solid rgba(0,179,160,0.15)",
                  paddingTop: 12,
                }}>
                  {s.detail}
                </div>
              </div>
            </div>

            {idx < steps.length - 1 && (
              <div style={{ padding: "0 8px", marginTop: 60 }}>
                <Arrow />
              </div>
            )}
          </Fragment>
        ))}
      </div>

      <div style={{
        marginTop: 24, textAlign: "center",
        color: "#64748b", fontSize: 14,
      }}>
        Ready to start?{" "}
        <a href="/onboarding" style={{ color: "#006355", fontWeight: 800, textDecoration: "none" }}>
          Begin your free diagnostic →
        </a>
      </div>

      <style>{`
        @media (max-width: 980px) {
          .howWrapper {
            grid-template-columns: 1fr !important;
          }
          .howWrapper > *[data-arrow] {
            display: none !important;
          }
        }
      `}</style>
    </Section>
  );
}