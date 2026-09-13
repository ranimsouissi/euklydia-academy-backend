export const roles = [
  { id: 1, tag: "AI SALES SPECIALIST", title: "AI Sales Specialist", forWho: "For Sales & Business Development", desc: "Automate prospecting, personalize outreach at scale, and forecast pipeline with AI-driven insights.", tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" } },
  { id: 2, tag: "AI MARKETING STRATEGIST", title: "AI Marketing Strategist", forWho: "For Marketing & Growth", desc: "Generate campaigns, optimize content performance, and segment audiences using AI-powered analytics.", tagColor: { bg: "rgba(99,102,241,0.10)", color: "#4338ca" } },
  { id: 3, tag: "AI DESIGNER", title: "AI Designer", forWho: "For Design & Creative", desc: "Accelerate visual production, generate briefs, and iterate on creative assets with generative AI tools.", tagColor: { bg: "rgba(236,72,153,0.10)", color: "#be185d" } },
  { id: 4, tag: "AI PROJECT MANAGER", title: "AI Project Manager", forWho: "For Project & Operations", desc: "Automate status reports, detect risks early, and optimize resource allocation with AI-assisted workflows.", tagColor: { bg: "rgba(245,158,11,0.10)", color: "#b45309" } },
];

export const ROLE_DETAILS = {
  "AI Sales Specialist": {
    tag: "AI SALES SPECIALIST",
    forWho: "Sales & Business Development",
    desc: "Automate prospecting, personalize outreach at scale, and forecast pipeline with AI-driven insights.",
    tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
    roleContext: "You spend your days prospecting, qualifying leads, and closing deals. This path gives you AI blueprints to automate repetitive tasks and focus on high-value conversations.",
    useCases: [
      { name: "Intelligent Prospecting", kpiBefore: "5 qualified leads/week, 3h prospecting/day", kpiAfter: "20 qualified leads/week, 45min prospecting/day", blueprint: "AI Prospecting Workflow + Scoring Template" },
      { name: "Personalized Outreach at Scale", kpiBefore: "12% email open rate, 2% reply rate", kpiAfter: "35% open rate, 8% reply rate", blueprint: "GPT Outreach Generator + A/B Testing Kit" },
      { name: "Pipeline Forecast & AI Insights", kpiBefore: "60% forecast accuracy, reactive pipeline review", kpiAfter: "85% forecast accuracy, proactive risk alerts", blueprint: "AI Pipeline Tracker + Weekly Insight Report" },
    ],
  },
  "AI Marketing Strategist": {
    tag: "AI MARKETING STRATEGIST",
    forWho: "Marketing & Growth",
    desc: "Generate campaigns, optimize content performance, and segment audiences using AI-powered analytics.",
    tagColor: { bg: "rgba(99,102,241,0.10)", color: "#4338ca" },
    roleContext: "You run campaigns, analyze performance, and manage content calendars. This path gives you AI blueprints to generate content faster and make data-driven decisions.",
    useCases: [
      { name: "AI Campaign Generation", kpiBefore: "3 campaigns/month, 2 weeks production time", kpiAfter: "12 campaigns/month, 3 days production time", blueprint: "Campaign Brief Generator + Content Matrix" },
      { name: "Campaign Performance Optimization", kpiBefore: "CAC 450 TND, iteration cycle 2-3 weeks", kpiAfter: "CAC 315 TND (-30%), iteration cycle 3-5 days", blueprint: "AI Performance Loop + A/B Testing Workflow" },
      { name: "AI Audience Segmentation", kpiBefore: "2 audience segments, 18% email CTR", kpiAfter: "8 dynamic segments, 34% email CTR", blueprint: "Segmentation Playbook + Persona Generator" },
    ],
  },
  "AI Designer": {
    tag: "AI DESIGNER",
    forWho: "Design & Creative",
    desc: "Accelerate visual production, generate briefs, and iterate on creative assets with generative AI tools.",
    tagColor: { bg: "rgba(236,72,153,0.10)", color: "#be185d" },
    roleContext: "You create visuals, manage briefs, and iterate on creative assets. This path gives you AI workflows to produce more in less time without sacrificing quality.",
    useCases: [
      { name: "Accelerated Visual Production", kpiBefore: "4 visual variants/day, 2h per concept", kpiAfter: "20 visual variants/day, 25min per concept", blueprint: "AI Image Workflow + Prompt Library" },
      { name: "AI Brief Generation", kpiBefore: "Brief writing: 3h, 40% client revision rate", kpiAfter: "Brief writing: 30min, 15% client revision rate", blueprint: "Brief Generator + Feedback Capture Template" },
      { name: "Creative Asset Iteration", kpiBefore: "3 iteration rounds, 5 days per campaign", kpiAfter: "1 iteration round, 1.5 days per campaign", blueprint: "AI Iteration Playbook + Review Checklist" },
    ],
  },
  "AI Project Manager": {
    tag: "AI PROJECT MANAGER",
    forWho: "Project & Operations",
    desc: "Automate status reports, detect risks early, and optimize resource allocation with AI-assisted workflows.",
    tagColor: { bg: "rgba(245,158,11,0.10)", color: "#b45309" },
    roleContext: "You coordinate teams, track deliverables, and manage stakeholders. This path gives you AI tools to automate reporting and catch risks before they become blockers.",
    useCases: [
      { name: "Automated Status Reports", kpiBefore: "3h/week on reporting, 1-day delay on updates", kpiAfter: "20min/week on reporting, real-time updates", blueprint: "AI Report Generator + Status Dashboard" },
      { name: "Early Risk Detection", kpiBefore: "Risks identified after impact, 35% reactive fixes", kpiAfter: "Risks flagged 5 days early, 80% proactive fixes", blueprint: "Risk Scoring Matrix + AI Alert Workflow" },
      { name: "Resource Optimization", kpiBefore: "65% team utilization, manual allocation", kpiAfter: "88% team utilization, AI-assisted allocation", blueprint: "Capacity Planner + Workload Balancer" },
    ],
  },
};

export const whatYoullGetItems = [
  { icon: "🎯", label: "Real business use cases" },
  { icon: "📊", label: "KPIs Before → After" },
  { icon: "📦", label: "Ready-to-use AI Blueprints" },
  { icon: "🚀", label: "Personalized learning path" },
];