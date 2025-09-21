import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Heart, MessageCircle, Shield, Users, ArrowRight, Play } from 'lucide-react';
import './Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <h1 className="hero-title">
              Your Mental Wellness
              <span className="hero-highlight"> Companion</span>
            </h1>
            <p className="hero-subtitle">
              AuraYouth provides AI-powered emotional support, crisis intervention,
              and personalized mental health guidance for youth worldwide.
            </p>
            <div className="hero-actions">
              {isAuthenticated() ? (
                <Link to="/chat" className="btn-primary">
                  Start Chat
                  <ArrowRight size={20} />
                </Link>
              ) : (
                <Link to="/login" className="btn-primary">
                  Get Started
                  <ArrowRight size={20} />
                </Link>
              )}
              <button className="btn-secondary">
                <Play size={20} />
                Watch Demo
              </button>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-card">
              <div className="chat-preview">
                <div className="chat-header">
                  <Heart className="chat-icon" />
                  <span>Aura</span>
                </div>
                <div className="chat-messages">
                  <div className="message bot">Hi! I'm here to listen and support you. How are you feeling today?</div>
                  <div className="message user">I've been feeling a bit anxious lately...</div>
                  <div className="message bot">I hear you. Anxiety can be really challenging. Would you like to try some breathing exercises together?</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <div className="section-header">
            <h2>Comprehensive Mental Health Support</h2>
            <p>Advanced AI technology combined with proven mental health practices</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <MessageCircle />
              </div>
              <h3>24/7 AI Chat Support</h3>
              <p>Empathetic conversations powered by advanced AI, available whenever you need support.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">
                <Shield />
              </div>
              <h3>Crisis Detection</h3>
              <p>Automatic detection of crisis situations with immediate connection to emergency resources.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">
                <Users />
              </div>
              <h3>Multimodal Analysis</h3>
              <p>Advanced emotion recognition using text, audio, and video for comprehensive understanding.</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">
                <Heart />
              </div>
              <h3>Personalized Care</h3>
              <p>AI-driven insights and recommendations tailored to your unique mental health journey.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Available Support</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">50+</div>
              <div className="stat-label">Countries Served</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">95%</div>
              <div className="stat-label">Accuracy Rate</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">10k+</div>
              <div className="stat-label">Lives Supported</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Start Your Journey?</h2>
            <p>Join thousands of youth who have found support and guidance through AuraYouth.</p>
            <div className="cta-actions">
              {isAuthenticated() ? (
                <Link to="/chat" className="btn-primary">
                  Continue Chat
                  <ArrowRight size={20} />
                </Link>
              ) : (
                <>
                  <Link to="/login" className="btn-primary">
                    Get Started Free
                    <ArrowRight size={20} />
                  </Link>
                  <Link to="/crisis-support" className="btn-secondary">
                    Need Help Now?
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;