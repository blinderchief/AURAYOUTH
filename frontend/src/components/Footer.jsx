import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Phone, Mail, MapPin, ExternalLink } from 'lucide-react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-logo">
              <Heart className="footer-logo-icon" />
              <span className="footer-logo-text">AuraYouth</span>
            </div>
            <p className="footer-description">
              AI-powered mental wellness platform for youth, providing empathetic support
              and crisis intervention when you need it most.
            </p>
          </div>

          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/chat">Chat Support</Link></li>
              <li><Link to="/profile">My Profile</Link></li>
              <li><Link to="/crisis-support">Crisis Support</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Crisis Hotlines</h3>
            <ul className="crisis-links">
              <li>
                <a href="tel:988" className="crisis-link">
                  <Phone size={16} />
                  US: 988 (24/7)
                </a>
              </li>
              <li>
                <a href="tel:116123" className="crisis-link">
                  <Phone size={16} />
                  UK: 116 123
                </a>
              </li>
              <li>
                <a href="tel:988" className="crisis-link">
                  <Phone size={16} />
                  Canada: 988
                </a>
              </li>
              <li>
                <a href="tel:131114" className="crisis-link">
                  <Phone size={16} />
                  Australia: 13 11 14
                </a>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Resources</h3>
            <ul>
              <li>
                <a href="https://www.who.int/health-topics/mental-disorders" target="_blank" rel="noopener noreferrer">
                  WHO Mental Health <ExternalLink size={14} />
                </a>
              </li>
              <li>
                <a href="https://www.befrienders.org" target="_blank" rel="noopener noreferrer">
                  International Hotlines <ExternalLink size={14} />
                </a>
              </li>
              <li>
                <a href="https://www.nami.org" target="_blank" rel="noopener noreferrer">
                  NAMI <ExternalLink size={14} />
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <p>&copy; 2025 AuraYouth. All rights reserved.</p>
            <div className="footer-links">
              <a href="#privacy">Privacy Policy</a>
              <a href="#terms">Terms of Service</a>
              <a href="#contact">Contact</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;