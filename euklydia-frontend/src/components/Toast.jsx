import { useEffect } from "react";

export default function Toast({ message, type = "success", onClose, duration = 3000 }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const styles = {
    success: "border-emerald-200 bg-emerald-50 text-emerald-800",
    error: "border-red-200 bg-red-50 text-red-800",
    info: "border-sky-200 bg-sky-50 text-sky-800",
  };

  const icons = {
    success: "✓",
    error: "✕",
    info: "ℹ",
  };

  const iconStyles = {
    success: "text-emerald-600",
    error: "text-red-600",
    info: "text-sky-600",
  };

  return (
    <div
      className={[
        "fixed bottom-6 right-6 z-50 flex items-center gap-3",
        "rounded-2xl border px-5 py-4 shadow-lg",
        styles[type],
      ].join(" ")}
      style={{
        animation: "slideUp 0.3s ease-out",
      }}
    >
      <style>{`
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <span className={["font-bold text-base", iconStyles[type]].join(" ")}>
        {icons[type]}
      </span>

      <span className="text-sm font-semibold">{message}</span>

      <button
        onClick={onClose}
        className="ml-2 text-slate-400 hover:text-slate-600 transition text-xs"
      >
        ✕
      </button>
    </div>
  );
}
