// ═══════════════════════════════════════════════════════════════════
// SOURCE UNIQUE DE VÉRITÉ pour les 4 rôles professionnels
// Utilisé par : ProfessionalRoles.jsx + OnboardingPage.jsx
// ═══════════════════════════════════════════════════════════════════

export const roles = [
  {
    id: "sales",
    name: "AI Sales Specialist",
    title: "AI Sales Specialist",
    tag: "Sales",
    tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
    forWho: "Sales managers, account executives, business developers",
    desc: "Master AI to qualify leads faster, personalize outreach at scale, and prepare every sales call with data-driven insights.",
    roleContext: "The AI Sales Specialist uses AI as a force multiplier — not a replacement. Your role is to identify where AI creates leverage in the sales funnel: from prospecting to closing.",
    useCases: [
      {
        name: "Lead Qualification Automation",
        kpiBefore: "Low conversion rate (~10–15%)",
        kpiAfter: "+25–40% qualified leads",
        blueprint: "AI Lead Scoring Agent Blueprint",
      },
      {
        name: "Personalized Outreach at Scale",
        kpiBefore: "Low reply rate (~5–10%)",
        kpiAfter: "2–3x reply rate",
        blueprint: "Hyper-Personalization Engine",
      },
      {
        name: "Sales Call Preparation",
        kpiBefore: "Low close rate",
        kpiAfter: "+15–25% close rate",
        blueprint: "AI Sales Copilot System",
      },
    ],
  },
  {
    id: "marketing",
    name: "AI Marketing Strategist",
    title: "AI Marketing Strategist",
    tag: "Go-to-Market",
    tagColor: { bg: "rgba(212,83,126,0.10)", color: "#993556" },
    forWho: "Marketing managers, content managers, growth leads",
    desc: "Accelerate content production, sharpen campaign targeting, and turn marketing data into strategic insight — with AI as your growth engine.",
    roleContext: "The AI Marketing Strategist builds scalable growth systems. Your role is to orchestrate AI across content, campaigns, and analytics to create measurable business impact.",
    useCases: [
      {
        name: "Content Strategy Optimization",
        kpiBefore: "Low engagement",
        kpiAfter: "+30–50% engagement",
        blueprint: "AI Content Engine System",
      },
      {
        name: "Campaign Performance Optimization",
        kpiBefore: "High CAC",
        kpiAfter: "-20–30% CAC",
        blueprint: "AI Growth Loop Framework",
      },
      {
        name: "Audience Insights & Segmentation",
        kpiBefore: "Poor targeting",
        kpiAfter: "+25% conversion",
        blueprint: "AI Persona Intelligence System",
      },
    ],
  },
  {
    id: "designer",
    name: "AI Designer",
    title: "AI Designer",
    tag: "Creativity",
    tagColor: { bg: "rgba(127,119,221,0.10)", color: "#534AB7" },
    forWho: "Designers, architects, creative directors",
    desc: "Accelerate your design process — from rapid concept generation to scalable design systems — using AI to ideate faster, optimize user experience, and automate design consistency.",
    roleContext: "The AI Designer keeps human creativity at the helm. Your role is to use AI to remove friction from your workflow, explore more ideas faster, and deliver higher-quality outputs.",
    useCases: [
      {
        name: "Rapid Concept Generation",
        kpiBefore: "Slow ideation",
        kpiAfter: "5x faster ideation",
        blueprint: "AI Design Ideation System",
      },
      {
        name: "UX Optimization",
        kpiBefore: "Low engagement",
        kpiAfter: "+20–30% engagement",
        blueprint: "AI UX Intelligence Framework",
      },
      {
        name: "Design System Automation",
        kpiBefore: "Inconsistency",
        kpiAfter: "+40% consistency",
        blueprint: "AI Design System Builder",
      },
    ],
  },
  {
    id: "pm",
    name: "AI Project Manager",
    title: "AI Project Manager",
    tag: "Delivery",
    tagColor: { bg: "rgba(56,130,221,0.10)", color: "#1a5fa8" },
    forWho: "Project managers, PMOs, coordinators",
    desc: "Deliver AI projects on time and on scope — by mastering planning, risk anticipation, and team productivity in an AI-driven environment.",
    roleContext: "The AI Project Manager bridges strategy and execution. Your role is to own the end-to-end delivery of AI initiatives while managing the human, organizational and technical complexity they bring.",
    useCases: [
      {
        name: "Project Planning Automation",
        kpiBefore: "Slow planning",
        kpiAfter: "50–70% time saved",
        blueprint: "AI Planning Engine",
      },
      {
        name: "Risk Identification",
        kpiBefore: "Reactive issues",
        kpiAfter: "-30% delays",
        blueprint: "AI Risk Intelligence System",
      },
      {
        name: "Team Productivity Optimization",
        kpiBefore: "Low efficiency",
        kpiAfter: "+25% productivity",
        blueprint: "AI Execution Optimization System",
      },
    ],
  },
];

// ═══════════════════════════════════════════════════════════════════
// Items "What You'll Get" — communs aux 4 rôles
// ═══════════════════════════════════════════════════════════════════
export const whatYoullGetItems = [
  { icon: "📦", label: "3 ready-to-use AI Blueprints" },
  { icon: "📚", label: "Templates, prompts & playbooks" },
  { icon: "📊", label: "Initial KPI → Projected KPI tracker" },
  { icon: "🎯", label: "Personalized learning pathway" },
];

// ═══════════════════════════════════════════════════════════════════
// Helper : retrouve un rôle par son nom (utilisé dans OnboardingPage)
// ═══════════════════════════════════════════════════════════════════
export const getRoleByName = (name) => roles.find((r) => r.name === name);

// ═══════════════════════════════════════════════════════════════════
// Helper : map { "AI Sales Specialist": {...}, ... }
// Pour compatibilité avec l'ancien code OnboardingPage
// ═══════════════════════════════════════════════════════════════════
export const ROLE_DETAILS = roles.reduce((acc, role) => {
  acc[role.name] = role;
  return acc;
}, {});