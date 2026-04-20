import { useState } from "react";
import Container from "./ui/Container";

const roles = [
  {
    id: "sales",
    title: "AI Sales Specialist",
    tag: "Sales",
    tagColor: { bg: "rgba(0,179,160,0.10)", color: "#006355" },
    forWho: "Sales managers, account executives, business developers",
    desc: "Leverage AI to close more deals, personalize outreach at scale, and automate your sales workflow — while keeping human relationships at the center.",
    roleContext: "The AI Sales Specialist uses AI as a force multiplier — not a replacement. Your role is to identify where AI creates leverage in the sales funnel: from prospecting to closing.",
    skills: [
      {
        name: "Prospection AI",
        icon: "🎯",
        description: "Utilisez l'AI pour identifier, qualifier et prioriser vos prospects plus rapidement. Construisez des workflows de sourcing automatisés qui font remonter les meilleures opportunités.",
        questions: [
          "Vous avez 200 prospects à contacter cette semaine. Quel est le meilleur moyen d'utiliser l'AI pour prioriser votre travail ?",
          "Vous utilisez LinkedIn Sales Navigator AI pour prospecter des PME. L'AI vous suggère 50 prospects mais vous n'avez le temps de contacter que 10. Comment choisissez-vous ?",
        ],
      },
      {
        name: "CRM et Scoring de Leads",
        icon: "⚙️",
        description: "Maîtrisez les outils CRM avec AI et l'interprétation du scoring pour vous concentrer sur les prospects les plus chauds et automatiser vos suivis.",
        questions: [
          "Votre CRM HubSpot AI montre que 3 prospects ont un score de 90/100. Qu'est-ce que ce score signifie ?",
          "Votre HubSpot AI vous dit : ce prospect a visité votre site 5 fois, ouvert 3 emails et téléchargé votre catalogue. Son score est 85/100. Que faites-vous ?",
        ],
      },
      {
        name: "Communication et Emails AI",
        icon: "✉️",
        description: "Rédigez et personnalisez des emails de prospection avec l'AI — en adaptant le ton, la langue et le contexte culturel à chaque prospect.",
        questions: [
          "Vous utilisez ChatGPT pour rédiger un email de prospection pour un client. Quelle est la meilleure approche ?",
          "Vous devez envoyer 100 emails personnalisés à 100 prospects différents. Sans AI cela prendrait 5 heures. Comment utilisez-vous l'AI pour faire cela en 30 minutes ?",
        ],
      },
      {
        name: "Analyse des Données Ventes",
        icon: "📊",
        description: "Lisez et exploitez les données AI pour anticiper les résultats, optimiser vos actions commerciales et prendre des décisions basées sur les données.",
        questions: [
          "Votre AI prédit que votre chiffre d'affaires ce mois sera inférieur à votre objectif. Que faites-vous ?",
          "Google Analytics AI vous montre que 80% de vos clients consultent vos offres entre 19h et 21h sur mobile. Comment utilisez-vous cette information ?",
        ],
      },
      {
        name: "Ethique AI dans la Vente",
        icon: "🛡️",
        description: "Appliquez les bonnes pratiques éthiques dans l'utilisation de l'AI en vente — respect de la vie privée, consentement et transparence avec vos clients.",
        questions: [
          "L'AI vous donne accès à des données personnelles très détaillées sur vos prospects. Quelle est la pratique éthique ?",
          "Un prospect vous demande si vous utilisez l'AI pour analyser son comportement en ligne. Comment répondez-vous de manière transparente ?",
        ],
      },
    ],
    tasks: [
      "Prospecter et qualifier des leads plus rapidement avec Apollo.io et LinkedIn Sales Navigator AI",
      "Personnaliser des emails et propositions à grande échelle avec HubSpot AI",
      "Automatiser les tâches répétitives du CRM et les séquences de relance",
      "Lire et exploiter les données ventes pour anticiper les résultats",
      "Utiliser l'AI de façon éthique et responsable dans les interactions clients",
    ],
    deliverables: [
      "AI Sales Playbook personnalisé",
      "Bibliothèque de prompts de prospection",
      "Séquences d'emails automatisées HubSpot",
      "Tableau de bord commercial AI",
    ],
  },
  {
    id: "marketing",
    title: "AI Marketing Strategist",
    tag: "Go-to-Market",
    tagColor: { bg: "rgba(212,83,126,0.10)", color: "#993556" },
    forWho: "Marketing managers, content managers, growth leads",
    desc: "Accelerate content production, sharpen campaign targeting, and turn marketing data into strategic insight — with AI as your growth engine.",
    roleContext: "The AI Marketing Strategist builds scalable growth systems. Your role is to orchestrate AI across content, campaigns, and analytics to create measurable business impact.",
    skills: [
      {
        name: "Création de Contenu AI",
        icon: "✍️",
        description: "Créez du contenu marketing adapté au marché en grande quantité et rapidement — posts, articles, visuels — en combinant les bons outils AI.",
        questions: [
          "Vous devez créer 30 posts pour le mois de Ramadan pour une entreprise. Quel est le meilleur outil AI à utiliser ?",
          "Votre client vous demande de créer en 2 heures : 10 posts Instagram, 5 emails et 3 visuels. Comment utilisez-vous l'AI ?",
        ],
      },
      {
        name: "Gestion Réseaux Sociaux AI",
        icon: "📱",
        description: "Maîtrisez les outils AI pour planifier, publier et analyser vos réseaux sociaux automatiquement depuis un seul tableau de bord.",
        questions: [
          "Vous gérez les réseaux sociaux d'une PME. Quel outil AI vous permet de planifier et publier automatiquement sur tous les réseaux en même temps ?",
          "Meta Business Suite AI vous montre que vos posts avec des images reçoivent 3 fois plus d'engagement que les posts texte. Que faites-vous ?",
        ],
      },
      {
        name: "Email Marketing AI",
        icon: "📧",
        description: "Créez et optimisez des campagnes email avec l'AI — séquences automatisées, personnalisation et optimisation du timing d'envoi.",
        questions: [
          "Votre taux d'ouverture est de 8%. Brevo AI vous montre que vos clients ouvrent leurs emails le soir. Que faites-vous ?",
          "Vous devez créer une séquence de 5 emails automatiques pour accueillir de nouveaux apprenants. Comment organisez-vous cette séquence avec l'AI ?",
        ],
      },
      {
        name: "Publicité AI",
        icon: "📣",
        description: "Maîtrisez la publicité digitale avec l'AI — ciblage précis, optimisation des mots clés et maximisation du ROI publicitaire.",
        questions: [
          "Vous lancez une campagne Facebook Ads AI pour promouvoir une formation. Quel ciblage choisissez-vous pour maximiser les inscriptions ?",
          "Votre campagne Google Ads AI a un coût par clic élevé et votre budget est limité. Comment utilisez-vous l'AI pour optimiser vos mots clés ?",
        ],
      },
      {
        name: "Analyse des Données Marketing",
        icon: "📊",
        description: "Lisez et exploitez les données AI pour prendre des décisions marketing basées sur les faits et améliorer continuellement vos performances.",
        questions: [
          "Google Analytics AI vous montre que 70% de vos visiteurs quittent votre site en moins de 10 secondes. Qu'est-ce que cela signifie et que faites-vous ?",
          "Vos données AI montrent que votre taux de conversion est 2x plus élevé le week-end. Comment adaptez-vous votre stratégie marketing ?",
        ],
      },
    ],
    tasks: [
      "Créer 30 posts, 5 emails et 3 visuels en 2 heures avec ChatGPT et Canva AI",
      "Planifier et automatiser 1 mois de contenu réseaux sociaux avec Buffer AI",
      "Lancer des campagnes publicitaires Facebook et Google Ads optimisées par AI",
      "Analyser les données marketing et adapter sa stratégie en temps réel",
      "Créer des campagnes email automatisées et personnalisées avec Brevo AI",
    ],
    deliverables: [
      "Calendrier de contenu AI — 1 mois complet",
      "Bibliothèque de prompts marketing",
      "Campagne publicitaire complète (Facebook + Google)",
      "Dashboard marketing AI avec KPIs",
    ],
  },
  {
    id: "designer",
    title: "AI Designer",
    tag: "Creativity",
    tagColor: { bg: "rgba(127,119,221,0.10)", color: "#534AB7" },
    forWho: "Designers, architects, creative directors",
    desc: "Supercharge your creative process — from concept to delivery — using AI as an ideation partner, production accelerator, and creative co-pilot.",
    roleContext: "The AI Designer keeps human creativity at the helm. Your role is to use AI to remove friction from your workflow, explore more ideas faster, and deliver higher-quality outputs.",
    skills: [
      {
        name: "Génération d'Images AI",
        icon: "🎨",
        description: "Générez des images adaptées au marché avec les outils AI leaders — en maîtrisant le prompting culturel pour des résultats pertinents et professionnels.",
        questions: [
          "Vous devez créer une affiche publicitaire pour une marque. Quel outil AI utilisez-vous pour générer des images uniques et créatives ?",
          "Vous utilisez Midjourney et l'AI génère une image avec des personnages aux traits occidentaux pour un client local. Que faites-vous ?",
        ],
      },
      {
        name: "Design UI/UX avec AI",
        icon: "📐",
        description: "Maîtrisez les outils AI pour concevoir des interfaces rapidement — wireframes, maquettes et expériences utilisateur adaptées au contexte local.",
        questions: [
          "Vous devez créer une maquette d'application mobile pour une startup. Quel outil AI vous aide à générer des wireframes rapidement ?",
          "Votre client vous demande de créer une interface d'application en arabe. Quels éléments spécifiques devez-vous prendre en compte dans votre design ?",
        ],
      },
      {
        name: "Création Vidéo et Animation AI",
        icon: "🎬",
        description: "Produisez des vidéos professionnelles avec l'AI sans équipe de tournage — voix off en arabe et français, animations et publicités vidéo.",
        questions: [
          "Vous devez créer une courte vidéo publicitaire de 30 secondes pour une PME sans équipe de tournage. Quel outil AI utilisez-vous ?",
          "Votre client veut une vidéo avec une voix off en arabe. Comment utilisez-vous l'AI pour créer cette voix off ?",
        ],
      },
      {
        name: "Brand Assets avec AI",
        icon: "✨",
        description: "Créez des identités visuelles complètes avec l'AI — logos, palettes, typographie arabe et templates cohérents adaptés au marché local.",
        questions: [
          "Un client vous demande de créer son identité visuelle complète avec l'AI. Par quoi commencez-vous ?",
          "Votre client veut son logo avec calligraphie arabe et design moderne. Comment procédez-vous avec l'AI ?",
        ],
      },
      {
        name: "Ethique et Propriété Intellectuelle AI",
        icon: "🛡️",
        description: "Appliquez les bonnes pratiques éthiques en design AI — droits commerciaux, propriété intellectuelle et transparence avec vos clients.",
        questions: [
          "Vous générez une image avec Midjourney pour un client qui veut l'utiliser commercialement. Que devez-vous vérifier avant de livrer ?",
          "Votre client vous demande si les visuels AI que vous créez lui appartiennent. Comment gérez-vous cette question de propriété intellectuelle ?",
        ],
      },
    ],
    tasks: [
      "Générer des visuels et affiches professionnelles avec Midjourney et Adobe Firefly",
      "Créer des interfaces UI/UX bilingues arabe/français avec Figma AI et Uizard",
      "Produire des vidéos publicitaires avec voix off arabe via Runway ML et ElevenLabs",
      "Construire une identité visuelle complète avec calligraphie arabe et design moderne",
      "Maîtriser les droits commerciaux et la propriété intellectuelle des créations AI",
    ],
    deliverables: [
      "Identité visuelle complète (logo + palette + typographie)",
      "Maquettes UI/UX bilingues arabe/français",
      "Vidéo publicitaire AI avec voix off",
      "Bibliothèque de prompts visuels",
    ],
  },
  {
    id: "pm",
    title: "AI Project Manager",
    tag: "Delivery",
    tagColor: { bg: "rgba(56,130,221,0.10)", color: "#1a5fa8" },
    forWho: "Project managers, PMOs, coordinators",
    desc: "Deliver AI projects on time and on scope — by mastering planning, stakeholder alignment, risk management and team coordination in an AI-driven environment.",
    roleContext: "The AI Project Manager bridges strategy and execution. Your role is to own the end-to-end delivery of AI initiatives while managing the human, organizational and technical complexity they bring.",
    skills: [
      {
        name: "Planification de Projets avec AI",
        icon: "🗺️",
        description: "Générez et gérez des plannings complets avec l'AI — tâches, délais, responsables — et adaptez-les aux contraintes réelles de votre équipe.",
        questions: [
          "Vous devez planifier le lancement d'une nouvelle formation en 3 mois. Quel outil AI vous aide à générer automatiquement le planning complet ?",
          "L'AI vous propose un planning mais certaines tâches semblent impossibles dans les délais. Que faites-vous ?",
        ],
      },
      {
        name: "Outils de Gestion de Projet AI",
        icon: "⚙️",
        description: "Maîtrisez les outils AI de gestion de projet pour automatiser les tâches répétitives, centraliser plusieurs projets et coordonner efficacement votre équipe.",
        questions: [
          "Votre équipe utilise Trello mais vous voulez intégrer l'AI pour automatiser les tâches répétitives. Quelle est la meilleure alternative ?",
          "Vous gérez 3 projets simultanément pour des clients. Comment utilisez-vous l'AI pour tout coordonner efficacement depuis un seul endroit ?",
        ],
      },
      {
        name: "Analyse des Risques et Données AI",
        icon: "📊",
        description: "Prédisez et gérez les risques projet avec l'AI — détectez les surcharges, anticipez les retards et prenez des décisions basées sur les données.",
        questions: [
          "L'AI de votre outil prédit que votre projet a 70% de risque de dépasser le délai prévu. Que faites-vous ?",
          "Votre tableau de bord AI montre que 3 membres de votre équipe sont surchargés à 150% de leur capacité. Que faites-vous ?",
        ],
      },
      {
        name: "Orchestration Humain-AI",
        icon: "🤝",
        description: "Coordonnez efficacement humains et AI dans vos projets — gérez la résistance au changement et gardez la décision finale dans les situations complexes.",
        questions: [
          "Votre équipe résiste à l'utilisation des outils AI. Certains membres disent que l'AI va les remplacer. Comment gérez-vous cette situation ?",
          "L'AI propose automatiquement d'assigner une tâche sensible à un collaborateur déjà surchargé. Comment réagissez-vous ?",
        ],
      },
      {
        name: "Gouvernance et Ethique AI",
        icon: "🛡️",
        description: "Appliquez les bonnes pratiques éthiques en gestion de projet AI — encadrez les décisions automatisées, assurez la transparence et gardez l'humain au centre.",
        questions: [
          "Votre entreprise veut utiliser l'AI pour évaluer automatiquement les performances des membres de l'équipe. Quelle est votre réaction ?",
          "Comment assurez-vous que les décisions prises par l'AI dans vos projets sont transparentes et traçables pour toutes les parties prenantes ?",
        ],
      },
    ],
    tasks: [
      "Générer des plannings complets automatiquement avec ClickUp AI et Notion AI",
      "Centraliser et coordonner plusieurs projets depuis un seul tableau de bord AI",
      "Prédire les risques et retards avant qu'ils surviennent avec l'AI",
      "Former son équipe à l'AI et gérer la résistance au changement",
      "Encadrer les décisions AI avec des règles éthiques et de gouvernance claires",
    ],
    deliverables: [
      "Planning projet complet généré par AI",
      "Tableau de bord risques et ressources",
      "AI Delivery Checklist",
      "Politique de gouvernance AI",
    ],
  },
];

export default function LearningPaths() {
  const [activeId, setActiveId] = useState(null);
  const [activeSkillIdx, setActiveSkillIdx] = useState(null);
  const active = roles.find((r) => r.id === activeId);

  const handleRoleClick = (id) => {
    setActiveId(activeId === id ? null : id);
    setActiveSkillIdx(null);
  };

  return (
    <section id="paths" style={{ padding: "80px 0", background: "#ffffff" }}>
      <Container>

        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: 10,
            padding: "8px 14px", borderRadius: 999,
            border: "1px solid #E5E7EB", background: "rgba(0,179,160,0.08)",
            color: "#006355", fontWeight: 900, fontSize: 13, marginBottom: 12,
          }}>
            📚 Learning Paths
          </div>
          <h2 style={{ fontSize: 36, margin: "0 0 10px", lineHeight: 1.12, letterSpacing: -0.5, fontWeight: 900, color: "#0f172a" }}>
            Role-based pathways designed for real work
          </h2>
          <p style={{ margin: 0, color: "#64748b", lineHeight: 1.7, fontSize: 16, maxWidth: 580 }}>
            Each path is built for a specific role — with a personalized AI Assessment of 5 skills × 2 questions. Click your profile to explore.
          </p>
        </div>

        {/* Grid — 4 roles, 2×2 */}
        <div className="pathsGrid" style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
          {roles.map((r) => {
            const isActive = activeId === r.id;
            return (
              <div
                key={r.id}
                onClick={() => handleRoleClick(r.id)}
                className="pathCard"
                style={{
                  background: "#fff",
                  border: isActive ? "2px solid #006355" : "1px solid #E5E7EB",
                  borderRadius: 20, padding: 24, cursor: "pointer",
                  transition: "all 0.2s ease", position: "relative", overflow: "hidden",
                  boxShadow: isActive
                    ? "0 0 0 4px rgba(0,99,85,0.08)"
                    : "0 4px 20px rgba(2,6,23,0.06)",
                }}
              >
                <div style={{
                  position: "absolute", top: -20, right: -20,
                  width: 70, height: 70, borderRadius: "50%",
                  background: r.tagColor.bg, opacity: 0.6,
                }} />

                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
                  <div style={{ flex: 1 }}>
                    <div style={{
                      display: "inline-flex", padding: "5px 10px", borderRadius: 999, marginBottom: 12,
                      background: isActive ? "rgba(0,99,85,0.10)" : r.tagColor.bg,
                      color: isActive ? "#006355" : r.tagColor.color,
                      fontWeight: 800, fontSize: 11,
                    }}>
                      {r.tag}
                    </div>

                    <h3 style={{ margin: "0 0 4px", fontSize: 17, fontWeight: 900, color: "#0f172a" }}>
                      {r.title}
                    </h3>

                    <div style={{ fontSize: 12, fontWeight: 700, marginBottom: 8, color: "#94a3b8" }}>
                      {r.forWho}
                    </div>

                    <p style={{ margin: "0 0 14px", fontSize: 13, lineHeight: 1.6, color: "#64748b" }}>
                      {r.desc}
                    </p>
                  </div>

                  <div style={{
                    flexShrink: 0,
                    background: "rgba(0,179,160,0.08)",
                    borderRadius: 12, padding: "6px 10px",
                    textAlign: "center",
                    border: "1px solid rgba(0,179,160,0.15)",
                  }}>
                    <div style={{ fontSize: 16, fontWeight: 900, color: "#006355" }}>5</div>
                    <div style={{ fontSize: 9, fontWeight: 700, color: "#64748b", lineHeight: 1.2 }}>skills<br/>assessed</div>
                  </div>
                </div>

                <div style={{
                  display: "flex", alignItems: "center", gap: 6,
                  fontWeight: 800, fontSize: 13,
                  borderTop: "1px solid #F1F5F9", paddingTop: 12,
                  color: isActive ? "#006355" : "#94a3b8",
                }}>
                  {isActive ? (
                    <>
                      <span style={{
                        width: 16, height: 16, borderRadius: "50%",
                        background: "#006355",
                        display: "inline-flex", alignItems: "center", justifyContent: "center",
                      }}>
                        <svg width="8" height="8" fill="none" viewBox="0 0 24 24" stroke="#fff" strokeWidth={3}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      </span>
                      <span>Selected — hide details ↑</span>
                    </>
                  ) : (
                    <span>Explore this path →</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Panneau de détail */}
        {active && (
          <div style={{
            marginTop: 16,
            background: "rgba(0,179,160,0.04)",
            border: "1px solid rgba(0,179,160,0.18)",
            borderRadius: 24, padding: 32,
          }}>
            {/* Header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16, marginBottom: 24 }}>
              <div>
                <h3 style={{ fontSize: 21, fontWeight: 900, color: "#0f172a", margin: "0 0 6px" }}>{active.title}</h3>
                <div style={{ fontSize: 13, color: "#006355", fontWeight: 700, marginBottom: 8 }}>For: {active.forWho}</div>
                <p style={{ fontSize: 14, color: "#64748b", lineHeight: 1.7, margin: 0, maxWidth: 600 }}>
                  {active.roleContext}
                </p>
              </div>
              <a href="/onboarding" style={{
                display: "inline-flex", padding: "10px 18px", borderRadius: 12,
                background: "#006355", color: "#fff", fontWeight: 900, fontSize: 13,
                textDecoration: "none", whiteSpace: "nowrap",
              }}>
                Start free assessment →
              </a>
            </div>

            {/* Skills accordéon */}
            <div style={{ marginBottom: 28 }}>
              <div style={{ fontSize: 11, fontWeight: 900, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 14 }}>
                AI Assessment — 5 skills · 2 questions each
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {active.skills.map((skill, idx) => {
                  const isOpen = activeSkillIdx === idx;
                  return (
                    <div key={skill.name} style={{
                      background: "#fff",
                      border: isOpen ? "1.5px solid #006355" : "1px solid #E5E7EB",
                      borderRadius: 14, overflow: "hidden",
                      transition: "all 0.2s",
                    }}>
                      <div
                        onClick={() => setActiveSkillIdx(isOpen ? null : idx)}
                        style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 16px", cursor: "pointer" }}
                      >
                        <span style={{ fontSize: 18, flexShrink: 0 }}>{skill.icon}</span>
                        <div style={{ flex: 1 }}>
                          <div style={{ fontWeight: 800, fontSize: 14, color: "#0f172a" }}>
                            Skill {idx + 1} — {skill.name}
                          </div>
                          <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>{skill.description}</div>
                        </div>
                        <div style={{ fontSize: 11, fontWeight: 700, color: isOpen ? "#006355" : "#94a3b8", flexShrink: 0 }}>
                          {isOpen ? "Masquer ↑" : "2 questions ↓"}
                        </div>
                      </div>

                      {isOpen && (
                        <div style={{
                          borderTop: "1px solid rgba(0,179,160,0.15)",
                          background: "rgba(0,179,160,0.03)",
                          padding: "14px 16px",
                          display: "flex", flexDirection: "column", gap: 10,
                        }}>
                          {skill.questions.map((q, qi) => (
                            <div key={qi} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                              <div style={{
                                flexShrink: 0, width: 22, height: 22,
                                borderRadius: 6, background: "#006355",
                                display: "flex", alignItems: "center", justifyContent: "center",
                                color: "#fff", fontSize: 11, fontWeight: 900,
                              }}>
                                Q{qi + 1}
                              </div>
                              <div style={{ fontSize: 13, color: "#334155", lineHeight: 1.6 }}>{q}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* What you'll learn + produce */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
              <div>
                <div style={{ fontSize: 11, fontWeight: 900, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 12 }}>
                  Ce que vous apprendrez à faire
                </div>
                <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                  {active.tasks.map((t) => (
                    <li key={t} style={{ display: "flex", alignItems: "flex-start", gap: 8, padding: "7px 0", borderBottom: "1px solid rgba(0,0,0,0.05)" }}>
                      <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#00B3A0", marginTop: 6, flexShrink: 0 }} />
                      <span style={{ fontSize: 13, color: "#334155", lineHeight: 1.55 }}>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <div style={{ fontSize: 11, fontWeight: 900, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 12 }}>
                  Ce que vous produirez
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {active.deliverables.map((d) => (
                    <div key={d} style={{
                      display: "flex", alignItems: "center", gap: 10,
                      background: "#fff", border: "1px solid #E5E7EB",
                      borderRadius: 10, padding: "10px 14px",
                    }}>
                      <span style={{ fontSize: 14 }}>📄</span>
                      <span style={{ fontSize: 13, fontWeight: 700, color: "#0f172a" }}>{d}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        <style>{`
          .pathCard:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(2,6,23,0.10) !important; }
          @media (max-width: 768px) { .pathsGrid { grid-template-columns: 1fr !important; } }
        `}</style>

      </Container>
    </section>
  );
}