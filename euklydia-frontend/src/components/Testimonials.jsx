import Container from "./ui/Container";
import avatarSara from "../assets/images/avatar-sara.jpeg";
import avatarKarim from "../assets/images/avatar-karim.jpeg";
import avatarMehdi from "../assets/images/avatar-mehdi.jpeg";

const testimonials = [
  {
    avatar: avatarSara,
    name: "Sara Cherni",
    role: "Directrice Marketing",
    company: "Startup Fintech — Tunis",
    borderColor: "#006355",
    rating: 5,
    quote:
      "J'utilisais ChatGPT au hasard sans vraiment savoir ce que je faisais. Le test de niveau m'a montré exactement où j'en étais skill par skill. En 3 semaines, j'ai automatisé tout mon calendrier de contenu et mes campagnes email. Le fait que tout soit adapté à mon rôle de Marketing Manager change tout.",
    highlight: "Calendrier contenu automatisé en 3 semaines",
  },
  {
    avatar: avatarKarim,
    name: "Karim Aït Yahia",
    role: "Chef de Projet Digital",
    company: "Agence conseil — Alger",
    borderColor: "#00B3A0",
    rating: 5,
    quote:
      "Les formations disponibles sur le marché étaient soit trop techniques, soit en anglais, soit trop chères. Euklydia est la première plateforme où j'ai senti que le contenu était fait pour moi — pour mon contexte, mes clients, mes outils. Le test par skill est brillant : je n'ai pas perdu de temps sur ce que je savais déjà.",
    highlight: "Parcours 100% adapté à son niveau réel",
  },
  {
    avatar: avatarMehdi,
    name: "Mehdi Benali",
    role: "Responsable Commercial",
    company: "PME Distribution — Casablanca",
    borderColor: "#004E4C",
    rating: 5,
    quote:
      "En tant que commercial, je pensais que l'AI c'était pour les développeurs. Euklydia m'a prouvé le contraire. J'ai appris à utiliser HubSpot AI et Apollo.io pour prospecter, et j'ai réduit mon temps de prospection de 60%. Le module sur l'éthique AI m'a aussi aidé à rassurer mes clients.",
    highlight: "60% de réduction du temps de prospection",
  },
];

export default function Testimonials() {
  return (
    <section id="testimonials" style={{ padding: "90px 0", background: "#F2FBF9" }}>
      <Container>

        {/* Header */}
        <div style={{ maxWidth: 640, marginBottom: 48 }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 10,
            padding: "8px 14px", borderRadius: 999,
            border: "1px solid rgba(0,179,160,0.22)",
            background: "rgba(0,179,160,0.10)",
            color: "#006355", fontWeight: 900, fontSize: 13, marginBottom: 12,
          }}>
            ⭐ Testimonials
          </div>

          <h2 style={{
            fontSize: 38, margin: "0 0 12px", lineHeight: 1.1,
            letterSpacing: -0.5, fontWeight: 900, color: "#0B3C3B",
          }}>
            What our learners say about Euklydia Academy
          </h2>

          <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7, fontSize: 16 }}>
            Professionals across the region who transformed their AI skills — role by role, skill by skill.
          </p>
        </div>

        {/* Testimonials grid */}
        <div
          className="testimonialsGrid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 20,
            marginBottom: 40,
          }}
        >
          {testimonials.map((t) => (
            <div
              key={t.name}
              style={{
                background: "#fff",
                border: "1px solid rgba(15,23,42,0.08)",
                borderRadius: 22,
                padding: 28,
                display: "flex",
                flexDirection: "column",
                gap: 20,
                boxShadow: "0 4px 24px rgba(2,6,23,0.06)",
                position: "relative",
                overflow: "hidden",
              }}
            >
              {/* Guillemet décoratif */}
              <div style={{
                position: "absolute", top: 20, right: 24,
                fontSize: 64, lineHeight: 1,
                color: "rgba(0,179,160,0.10)",
                fontFamily: "Georgia, serif",
                fontWeight: 900,
                userSelect: "none",
              }}>
                "
              </div>

              {/* Stars */}
              <div style={{ display: "flex", gap: 3 }}>
                {Array.from({ length: t.rating }).map((_, i) => (
                  <span key={i} style={{ color: "#F59E0B", fontSize: 14 }}>★</span>
                ))}
              </div>

              {/* Citation */}
              <p style={{
                fontSize: 14, color: "#334155", lineHeight: 1.75,
                margin: 0, position: "relative", zIndex: 1,
                fontStyle: "italic",
              }}>
                "{t.quote}"
              </p>

              {/* Highlight */}
              <div style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                padding: "6px 12px", borderRadius: 99,
                background: "rgba(0,179,160,0.08)",
                border: "1px solid rgba(0,179,160,0.15)",
                width: "fit-content",
              }}>
                <span style={{ color: "#00B3A0", fontSize: 12 }}>✓</span>
                <span style={{ fontSize: 11, fontWeight: 800, color: "#006355" }}>
                  {t.highlight}
                </span>
              </div>

              {/* Profil avec vraie photo */}
              <div style={{
                display: "flex", alignItems: "center", gap: 12,
                borderTop: "1px solid #F1F5F9", paddingTop: 16,
              }}>
                <img
                  src={t.avatar}
                  alt={t.name}
                  style={{
                    width: 52, height: 52,
                    borderRadius: "50%",
                    objectFit: "cover",
                    objectPosition: "center top",
                    border: `2.5px solid ${t.borderColor}`,
                    flexShrink: 0,
                  }}
                />
                <div>
                  <div style={{ fontWeight: 900, fontSize: 14, color: "#0f172a" }}>
                    {t.name}
                  </div>
                  <div style={{ fontSize: 12, color: "#64748b", fontWeight: 600 }}>
                    {t.role}
                  </div>
                  <div style={{ fontSize: 11, color: "#94a3b8", fontWeight: 600 }}>
                    {t.company}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA final */}
        <div style={{
          background: "#006355",
          borderRadius: 22,
          padding: "32px 36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 20,
          flexWrap: "wrap",
        }}>
          <div>
            <div style={{ fontWeight: 900, color: "#fff", fontSize: 20, marginBottom: 6 }}>
              Ready to build your AI roadmap?
            </div>
            <div style={{ color: "rgba(255,255,255,0.75)", fontSize: 14 }}>
              Start with a free 10-minute skills test. Get your personalized learning path instantly.
            </div>
          </div>
          <a
            href="/onboarding"
            style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "14px 26px", borderRadius: 12,
              background: "#fff", color: "#006355",
              fontWeight: 900, fontSize: 14,
              textDecoration: "none", whiteSpace: "nowrap",
              transition: "transform 0.2s ease",
            }}
            onMouseEnter={e => e.currentTarget.style.transform = "translateY(-2px)"}
            onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
          >
            Start free assessment →
          </a>
        </div>

        <style>{`
          @media (max-width: 1024px) {
            .testimonialsGrid { grid-template-columns: repeat(2, 1fr) !important; }
          }
          @media (max-width: 640px) {
            .testimonialsGrid { grid-template-columns: 1fr !important; }
          }
        `}</style>

      </Container>
    </section>
  );
}