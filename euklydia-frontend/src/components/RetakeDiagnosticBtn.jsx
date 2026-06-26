// src/components/RetakeDiagnosticBtn.jsx
/**
 * Bouton "Refaire le diagnostic" — toujours affiché.
 *
 * Comportements :
 *   - canRetake=true  → bouton cliquable → ouvre ConfirmModal
 *   - canRetake=false → bouton désactivé → affiche "Disponible le JJ/MM/YYYY"
 */

export default function RetakeDiagnosticBtn({ canRetake, nextAllowedAt, onClick, tx, lang }) {

  // Formater la date de disponibilité
  const formatDate = (isoDate) => {
    if (!isoDate) return null;
    try {
      return new Date(isoDate).toLocaleDateString(
        lang === "fr" ? "fr-FR" : "en-GB",
        { day: "2-digit", month: "long", year: "numeric" }
      );
    } catch {
      return null;
    }
  };

  const availableDate = formatDate(nextAllowedAt);

  const labelAvailable = lang === "fr"
    ? `Disponible le ${availableDate}`
    : `Available on ${availableDate}`;

  if (canRetake) {
    return (
      <button
        onClick={onClick}
        className="rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-euk-dark transition hover:bg-slate-50 shrink-0"
      >
        {tx.retakeDiagnostic || tx.redodiagnostic}
      </button>
    );
  }

  // Parcours en cours — bouton désactivé avec date de disponibilité
  return (
    <div className="flex flex-col items-end gap-1 shrink-0">
      <button
        disabled
        className="rounded-2xl border border-slate-200 bg-slate-50 px-5 py-3 text-sm font-semibold text-slate-400 cursor-not-allowed"
      >
        {tx.retakeDiagnostic || tx.redodiagnostic}
      </button>
      {availableDate && (
        <span className="text-xs text-slate-400">
          📅 {labelAvailable}
        </span>
      )}
    </div>
  );
}
