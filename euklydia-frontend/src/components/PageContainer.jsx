// src/components/layout/PageContainer.jsx
//
// Wrapper de largeur standard pour toute la plateforme.
// Remplace partout :  <div className="mx-auto max-w-6xl px-8">  →  <PageContainer>
//
// Variants :
//   - default : max-w-page (1440px) — pour sections marketing, dashboards
//   - narrow  : max-w-content (1200px) — pour formulaires, articles, diagnostic
//   - full    : w-full — pleine largeur, utile pour sections colorées de fond

export default function PageContainer({
  children,
  variant = "default",
  className = "",
  as: Tag = "div",
}) {
  const widthClass =
    variant === "narrow"
      ? "max-w-content"
      : variant === "full"
      ? "w-full"
      : "max-w-page";

  return (
    <Tag
      className={[
        "mx-auto w-full",
        widthClass,
        // Padding horizontal responsive : 16px mobile, 32px tablet, 48px+ desktop
        "px-4 sm:px-6 lg:px-10 xl:px-12",
        className,
      ].join(" ")}
    >
      {children}
    </Tag>
  );
}