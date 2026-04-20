import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import AuthPage from "./pages/AuthPage";
import AuthCallback from "./pages/AuthCallback";
import CommandCenterPage from "./pages/CommandCenterPage";
import AIRoadmapPage from "./pages/AIRoadmapPage";
import LearningPage from "./pages/LearningPage";
import OnboardingPage from "./pages/OnboardingPage";
import AssessmentPage from "./pages/AssessmentPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import ProfilePage from "./pages/ProfilePage";
import NotFoundPage from "./pages/NotFoundPage";
import RequireAuth from "./routes/RequireAuth";
import AppLayout from "./layouts/AppLayout";
import PublicLayout from "./layouts/PublicLayout";
import ModuleUnitsPage from "./pages/ModuleUnitsPage";
import LessonPlayerPage from "./pages/LessonPlayerPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Pages publiques */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
        </Route>

        {/* Pages privées */}
        <Route element={<RequireAuth />}>
          <Route element={<AppLayout />}>
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/dashboard" element={<CommandCenterPage />} />
            <Route path="/roadmap" element={<AIRoadmapPage />} />
            <Route path="/learning" element={<LearningPage />} />
            {/* ✅ Redirection automatique vers /units */}
            <Route path="/learning/module/:moduleId" element={<Navigate to="units" replace />} />
            <Route path="/learning/module/:moduleId/units" element={<ModuleUnitsPage />} />
            <Route path="/learning/module/:moduleId/units/:unitId/lessons/:lessonId" element={<LessonPlayerPage />} />
            <Route path="/assessment" element={<AssessmentPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>
        </Route>

        {/* Page 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}