import { useNavigate } from "react-router-dom";
import Container from "./ui/Container";

export default function Footer() {
  const navigate = useNavigate();

  const colTitle = { fontWeight: 900, marginBottom: 12, fontSize: 14 };
  const linkStyle = {
    margin: "10px 0",
    opacity: 0.85,
    cursor: "pointer",
    fontSize: 14,
    textDecoration: "none",
    color: "#fff",
    display: "block",
    transition: "opacity 0.2s ease",
  };

  // Helper: smooth scroll to anchor on landing page
  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  // Helper: navigate to route
  const goTo = (path) => navigate(path);

  // Social icon style — "Coming soon" mode (subtle, non-clickable)
  const socialIconStyle = {
    width: 40,
    height: 40,
    borderRadius: 12,
    background: "rgba(255,255,255,0.08)",
    display: "grid",
    placeItems: "center",
    color: "rgba(255,255,255,0.55)",
    cursor: "not-allowed",
    transition: "background 0.2s ease",
    position: "relative",
  };

  return (
    <footer style={{ background: "#0B3C3B", color: "#fff", padding: "70px 0 28px" }}>
      <Container>
        <div
          className="footerGrid"
          style={{
            display: "grid",
            gridTemplateColumns: "2fr 1fr 1fr 1fr",
            gap: 40,
          }}
        >
          {/* ─── Colonne 1 : Brand ──────────────────────── */}
          <div>
            <div style={{ fontWeight: 900, fontSize: 22, marginBottom: 10 }}>
              Euklydia <span style={{ color: "#00B3A0" }}>Academy</span>
            </div>
            <div style={{ opacity: 0.85, lineHeight: 1.7, maxWidth: 420, fontSize: 14 }}>
              The first use case-driven AI learning platform for North African leaders.
            </div>

            <div style={{ marginTop: 22, fontWeight: 900, opacity: 0.9, fontSize: 14 }}>
              Follow us
            </div>
            <div style={{ display: "flex", gap: 12, marginTop: 12, alignItems: "center" }}>
              {/* LinkedIn — Coming soon */}
              <div
                title="Coming soon"
                aria-label="LinkedIn — Coming soon"
                style={socialIconStyle}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
              </div>

              {/* YouTube — Coming soon */}
              <div
                title="Coming soon"
                aria-label="YouTube — Coming soon"
                style={socialIconStyle}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </div>

              {/* "Coming soon" label */}
              <span style={{
                fontSize: 11,
                fontStyle: "italic",
                opacity: 0.5,
                marginLeft: 4,
              }}>
                Coming soon
              </span>
            </div>
          </div>

          {/* ─── Colonne 2 : Product ──────────────────────── */}
          <div>
            <div style={colTitle}>Product</div>
            <div
              style={linkStyle}
              onClick={() => scrollTo("platform")}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Platform
            </div>
            <div
              style={linkStyle}
              onClick={() => scrollTo("how")}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              How it works
            </div>
            <div
              style={linkStyle}
              onClick={() => scrollTo("paths")}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Roles
            </div>
            <div
              style={linkStyle}
              onClick={() => goTo("/auth")}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              AI Diagnostic
            </div>
          </div>

          {/* ─── Colonne 3 : Company ──────────────────────── */}
          <div>
            <div style={colTitle}>Company</div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              About
            </div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              FAQ
            </div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Contact
            </div>
          </div>

          {/* ─── Colonne 4 : Legal ──────────────────────── */}
          <div>
            <div style={colTitle}>Legal</div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Privacy Policy
            </div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Terms of Service
            </div>
            <div
              style={linkStyle}
              onMouseEnter={e => e.currentTarget.style.opacity = "1"}
              onMouseLeave={e => e.currentTarget.style.opacity = "0.85"}
            >
              Cookie Policy
            </div>
          </div>
        </div>

        {/* ─── Bottom bar ──────────────────────── */}
        <div
          style={{
            marginTop: 40,
            paddingTop: 18,
            borderTop: "1px solid rgba(255,255,255,0.18)",
            display: "flex",
            justifyContent: "space-between",
            gap: 18,
            flexWrap: "wrap",
            opacity: 0.85,
            fontSize: 13,
          }}
        >
          <div>
            Made by <span style={{ color: "#00B3A0", fontWeight: 900 }}>EUKLYDIA</span> | AI Scaling Agency
          </div>
          <div>© 2026 Euklydia Academy</div>
        </div>

        <style>{`
          @media (max-width: 980px) {
            .footerGrid {
              grid-template-columns: 1fr 1fr !important;
            }
          }
          @media (max-width: 620px) {
            .footerGrid {
              grid-template-columns: 1fr !important;
            }
          }
        `}</style>
      </Container>
    </footer>
  );
}