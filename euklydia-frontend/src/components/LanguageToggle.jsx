export default function LanguageToggle({ language, setLanguage }) {
  return (
    <div className="inline-flex items-center rounded-2xl border border-slate-200 bg-white p-1 shadow-sm">
      <button
        onClick={() => setLanguage("en")}
        className={[
          "rounded-xl px-3 py-2 text-sm font-semibold transition",
          language === "en"
            ? "bg-euk-primary text-white"
            : "text-slate-600 hover:bg-slate-50",
        ].join(" ")}
      >
        EN
      </button>

      <button
        onClick={() => setLanguage("fr")}
        className={[
          "rounded-xl px-3 py-2 text-sm font-semibold transition",
          language === "fr"
            ? "bg-euk-primary text-white"
            : "text-slate-600 hover:bg-slate-50",
        ].join(" ")}
      >
        FR
      </button>
    </div>
  );
}