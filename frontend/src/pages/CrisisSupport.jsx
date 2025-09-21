import React, { useState } from 'react';
import { Phone, MessageCircle, MapPin, Clock, Heart, Shield, Users, BookOpen } from 'lucide-react';
import './CrisisSupport.css';

const CrisisSupport = () => {
  const [selectedCountry, setSelectedCountry] = useState('US');

  const crisisResources = {
    US: {
      name: 'United States',
      hotlines: [
        {
          name: 'National Suicide Prevention Lifeline',
          number: '988',
          description: '24/7 suicide prevention and crisis support',
          website: 'https://988lifeline.org'
        },
        {
          name: 'Crisis Text Line',
          number: 'Text HOME to 741741',
          description: 'Free 24/7 crisis support via text message',
          website: 'https://www.crisistextline.org'
        },
        {
          name: 'National Alliance on Mental Illness (NAMI) Helpline',
          number: '1-800-950-NAMI (6264)',
          description: 'Mental health information and support',
          website: 'https://www.nami.org/help'
        }
      ],
      resources: [
        {
          name: 'Mental Health America',
          description: 'Screening tools and mental health resources',
          website: 'https://www.mhanational.org'
        },
        {
          name: 'SAMHSA Treatment Locator',
          description: 'Find mental health treatment facilities',
          website: 'https://findtreatment.samhsa.gov'
        }
      ]
    },
    UK: {
      name: 'United Kingdom',
      hotlines: [
        {
          name: 'Samaritans',
          number: '116 123',
          description: '24/7 emotional support',
          website: 'https://www.samaritans.org'
        },
        {
          name: 'NHS 111',
          number: '111',
          description: 'Medical advice and mental health support',
          website: 'https://www.nhs.uk/using-the-nhs/nhs-services/urgent-and-emergency-care/nhs-111/'
        }
      ],
      resources: [
        {
          name: 'Mind',
          description: 'Mental health charity providing support',
          website: 'https://www.mind.org.uk'
        }
      ]
    },
    CA: {
      name: 'Canada',
      hotlines: [
        {
          name: 'Canada Suicide Prevention Service',
          number: '988',
          description: '24/7 suicide prevention and crisis support',
          website: 'https://www.canada.ca/en/public-health/services/mental-health-services/canadian-suicide-prevention-service.html'
        },
        {
          name: 'Crisis Services Canada',
          number: '988',
          description: '24/7 crisis support',
          website: 'https://www.crisisservicescanada.ca'
        }
      ],
      resources: [
        {
          name: 'Canadian Mental Health Association',
          description: 'Mental health support and resources',
          website: 'https://cmha.ca'
        }
      ]
    }
  };

  const countries = Object.keys(crisisResources);

  const immediateHelp = [
    {
      title: 'If You\'re in Immediate Danger',
      description: 'Call emergency services immediately',
      icon: Shield,
      urgent: true
    },
    {
      title: 'Talk to Someone Now',
      description: 'Connect with a crisis counselor 24/7',
      icon: Phone,
      urgent: false
    },
    {
      title: 'Text for Support',
      description: 'Send a text message for immediate help',
      icon: MessageCircle,
      urgent: false
    }
  ];

  const copingStrategies = [
    {
      title: 'Breathing Exercises',
      description: 'Deep breathing techniques to calm anxiety',
      icon: Heart
    },
    {
      title: 'Grounding Techniques',
      description: '5-4-3-2-1 method to stay present',
      icon: Users
    },
    {
      title: 'Self-Care Activities',
      description: 'Healthy ways to care for your mental health',
      icon: BookOpen
    }
  ];

  return (
    <div className="crisis-support">
      <div className="crisis-container">
        {/* Emergency Header */}
        <div className="emergency-header">
          <div className="emergency-alert">
            <Shield className="alert-icon" />
            <div className="alert-content">
              <h2>Need Help Right Now?</h2>
              <p>If you're in crisis or having thoughts of self-harm, please reach out immediately.</p>
            </div>
          </div>
        </div>

        {/* Immediate Help Section */}
        <section className="immediate-help">
          <h2>Immediate Support Options</h2>
          <div className="help-grid">
            {immediateHelp.map((help, index) => {
              const Icon = help.icon;
              return (
                <div key={index} className={`help-card ${help.urgent ? 'urgent' : ''}`}>
                  <Icon className="help-icon" />
                  <h3>{help.title}</h3>
                  <p>{help.description}</p>
                  {help.urgent && (
                    <div className="urgent-badge">URGENT</div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Country Selection */}
        <section className="country-section">
          <h2>Crisis Resources by Country</h2>
          <div className="country-selector">
            <label htmlFor="country-select">Select your country:</label>
            <select
              id="country-select"
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
            >
              {countries.map(country => (
                <option key={country} value={country}>
                  {crisisResources[country].name}
                </option>
              ))}
            </select>
          </div>
        </section>

        {/* Hotlines */}
        <section className="hotlines">
          <h3>24/7 Crisis Hotlines - {crisisResources[selectedCountry].name}</h3>
          <div className="hotline-grid">
            {crisisResources[selectedCountry].hotlines.map((hotline, index) => (
              <div key={index} className="hotline-card">
                <div className="hotline-header">
                  <Phone className="hotline-icon" />
                  <h4>{hotline.name}</h4>
                </div>
                <div className="hotline-contact">
                  <strong>{hotline.number}</strong>
                </div>
                <p>{hotline.description}</p>
                <a
                  href={hotline.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hotline-link"
                >
                  Visit Website
                </a>
              </div>
            ))}
          </div>
        </section>

        {/* Additional Resources */}
        <section className="resources">
          <h3>Additional Resources</h3>
          <div className="resource-grid">
            {crisisResources[selectedCountry].resources.map((resource, index) => (
              <div key={index} className="resource-card">
                <h4>{resource.name}</h4>
                <p>{resource.description}</p>
                <a
                  href={resource.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="resource-link"
                >
                  Learn More
                </a>
              </div>
            ))}
          </div>
        </section>

        {/* Coping Strategies */}
        <section className="coping-section">
          <h2>Coping Strategies</h2>
          <div className="coping-grid">
            {copingStrategies.map((strategy, index) => {
              const Icon = strategy.icon;
              return (
                <div key={index} className="coping-card">
                  <Icon className="coping-icon" />
                  <h3>{strategy.title}</h3>
                  <p>{strategy.description}</p>
                  <button className="coping-btn">Learn More</button>
                </div>
              );
            })}
          </div>
        </section>

        {/* Professional Help */}
        <section className="professional-help">
          <h2>Find Professional Help</h2>
          <div className="professional-content">
            <div className="help-types">
              <div className="help-type">
                <Users className="type-icon" />
                <h3>Therapists & Counselors</h3>
                <p>Find licensed mental health professionals in your area</p>
                <button className="help-btn">Find Therapists</button>
              </div>
              <div className="help-type">
                <MapPin className="type-icon" />
                <h3>Mental Health Clinics</h3>
                <p>Locate treatment centers and mental health facilities</p>
                <button className="help-btn">Find Clinics</button>
              </div>
              <div className="help-type">
                <Clock className="type-icon" />
                <h3>Support Groups</h3>
                <p>Connect with others who understand your experiences</p>
                <button className="help-btn">Find Groups</button>
              </div>
            </div>
          </div>
        </section>

        {/* Footer Note */}
        <div className="support-footer">
          <p>
            <strong>Remember:</strong> You're not alone. Help is available 24/7.
            If you're having thoughts of self-harm, please call emergency services immediately.
          </p>
        </div>
      </div>
    </div>
  );
};

export default CrisisSupport;