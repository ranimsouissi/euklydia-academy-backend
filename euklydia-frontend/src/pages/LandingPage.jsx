import Hero from "../components/Hero";
import WhyEuklydia from "../components/WhyEuklydia";
import HowItWorks from "../components/HowItWorks";
import LearningPaths from "../components/LearningPaths";
import Testimonials from "../components/Testimonials";
import Footer from "../components/Footer";

export default function LandingPage() {
  return (
    <>
      <Hero />
      <WhyEuklydia />
      <HowItWorks />
      <LearningPaths />
      <Testimonials />
      <Footer />
    </>
  );
}