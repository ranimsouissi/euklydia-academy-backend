import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import AuthPage from "./pages/AuthPage";
import AuthCallback from "./pages/AuthCallback";
import DashboardPage from "./pages/DashboardPage";
import AIRoadmapPage from "./pages/AIRoadmapPage";
import LearningPage from "./pages/LearningPage";
import OnboardingPage from "./pages/OnboardingPage";
import DiagnosticPage from "./pages/DiagnosticPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import ProfilePage from "./pages/ProfilePage";
import NotFoundPage from "./pages/NotFoundPage";
import AdminDashboardPage from "./pages/AdminDashboardPage"; // ← NEW
import RequireAuth from "./routes/RequireAuth";
import AppLayout from "./layouts/AppLayout";
import PublicLayout from "./layouts/PublicLayout";
import AuthLayout from "./layouts/AuthLayout";
import ModulePage from "./pages/ModulePage";
import AdminRoute from "./components/AdminRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
        </Route>

        <Route path="/auth" element={<AuthPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />

        <Route element={<AuthLayout />}>
          <Route path="/auth/callback" element={<AuthCallback />} />
        </Route>

        <Route element={<RequireAuth />}>
          <Route element={<AppLayout />}>
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/roadmap" element={<AIRoadmapPage />} />
            <Route path="/learning" element={<LearningPage />} />
            <Route path="/learning/module/:moduleId" element={<Navigate to="units" replace />} />
            <Route path="/learning/module/:moduleId/units" element={<ModulePage />} />
            <Route path="/diagnostic" element={<DiagnosticPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/admin" element={<AdminRoute><AdminDashboardPage /></AdminRoute>} />
          </Route>
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}