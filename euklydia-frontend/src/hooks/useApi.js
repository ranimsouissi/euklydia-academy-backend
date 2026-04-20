import { useState, useEffect, useCallback } from "react";
import { apiFetch } from "../utils/api";

/**
 * Hook React pour charger des données depuis l'API.
 * Gère automatiquement :
 * - L'état loading
 * - L'état error
 * - Le refetch manuel
 * - La gestion du 401 (via apiFetch)
 *
 * Usage :
 *   const { data, loading, error, refetch } = useApi("/api/v1/roadmap");
 */
export function useApi(endpoint, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!endpoint) return;

    setLoading(true);
    setError(null);

    try {
      const res = await apiFetch(endpoint, options);

      // null = 401 géré par apiFetch (redirect déjà fait)
      if (!res) return;

      const json = await res.json().catch(() => null);

      if (!res.ok) {
        setError(json?.detail || `Error ${res.status}`);
        setData(null);
      } else {
        setData(json);
      }
    } catch (err) {
      setError(err.message || "Unexpected error");
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}