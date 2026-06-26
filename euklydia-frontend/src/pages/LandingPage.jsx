import Hero from "../components/Hero";
import WhyEuklydiaAcademy from "../components/WhyEuklydiaAcademy";
import HowItWorks from "../components/HowItWorks";
import ProfessionalRoles from "../components/ProfessionalRoles";
import Testimonials from "../components/Testimonials";
import Footer from "../components/Footer";

export default function LandingPage() {
  return (
    <>
      <Hero />
      <WhyEuklydiaAcademy />
      <HowItWorks />
      <ProfessionalRoles />
      <Testimonials />
      <Footer />
    </>
  );
}