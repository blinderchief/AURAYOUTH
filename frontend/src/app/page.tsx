import { Heart, Shield, Brain, MessageCircle } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Hero Section */}
      <section className="px-6 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Your AI Companion for
            <span className="text-blue-600"> Mental Wellness</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            AuraYouth provides empathetic, confidential AI-powered support tailored for young people.
            Experience the future of mental health care with trust, originality, and real human-like understanding.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/login" className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg">
              Get Started
            </Link>
            <button className="border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
              Learn More
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose AuraYouth?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6 rounded-lg hover:shadow-lg transition-shadow duration-200">
              <MessageCircle className="w-12 h-12 text-blue-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Chatbot</h3>
              <p className="text-gray-600">24/7 empathetic conversations powered by advanced AI.</p>
            </div>
            <div className="text-center p-6 rounded-lg hover:shadow-lg transition-shadow duration-200">
              <Brain className="w-12 h-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Emotion Recognition</h3>
              <p className="text-gray-600">Understand your feelings through intelligent analysis.</p>
            </div>
            <div className="text-center p-6 rounded-lg hover:shadow-lg transition-shadow duration-200">
              <Heart className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Digital Twin</h3>
              <p className="text-gray-600">Your personalized AI companion that grows with you.</p>
            </div>
            <div className="text-center p-6 rounded-lg hover:shadow-lg transition-shadow duration-200">
              <Shield className="w-12 h-12 text-red-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Confidential</h3>
              <p className="text-gray-600">Your privacy is our top priority. Fully secure and anonymous.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="px-6 py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Built with Trust in Mind
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Inspired by successful startups on Product Hunt, AuraYouth combines cutting-edge AI technology
            with a human-centered design approach. Our platform reflects the originality and realness
            that users trust in modern mental health solutions.
          </p>
          <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-500">
            <span className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              End-to-End Encrypted
            </span>
            <span className="flex items-center gap-2">
              <Brain className="w-5 h-5" />
              AI-Powered Insights
            </span>
            <span className="flex items-center gap-2">
              <Heart className="w-5 h-5" />
              Youth-Focused Design
            </span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-8 bg-gray-900 text-white text-center">
        <p>&copy; 2025 AuraYouth. Empowering youth mental wellness with AI.</p>
      </footer>
    </div>
  );
}
