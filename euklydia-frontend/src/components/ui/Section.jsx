// src/components/ui/Section.jsx
import Container from "./Container";

export default function Section({ id, children, bg = "#F2FBF9" }) {
  return (
    <section
      id={id}
      style={{
        padding: "90px 0",
        background: bg,
      }}
    >
      <Container>{children}</Container>
    </section>
  );
}