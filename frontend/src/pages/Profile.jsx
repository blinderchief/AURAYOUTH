import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { User, Settings, Heart, Calendar, MessageCircle } from 'lucide-react';
import './Profile.css';

const Profile = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data for demonstration
  const mockStats = {
    totalChats: 24,
    crisisDetected: 2,
    avgMood: 'Stable',
    lastActivity: '2 hours ago'
  };

  const mockHistory = [
    { date: '2025-01-20', emotion: 'anxious', summary: 'Discussed work stress' },
    { date: '2025-01-19', emotion: 'happy', summary: 'Shared positive news' },
    { date: '2025-01-18', emotion: 'sad', summary: 'Talked about difficult day' },
  ];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: User },
    { id: 'history', label: 'Chat History', icon: MessageCircle },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  return (
    <div className="profile">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar">
            <User size={48} />
          </div>
          <div className="profile-info">
            <h1>{user?.full_name || user?.username}</h1>
            <p>Member since January 2025</p>
          </div>
        </div>

        <div className="profile-tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={18} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        <div className="profile-content">
          {activeTab === 'overview' && (
            <div className="overview">
              <div className="stats-grid">
                <div className="stat-card">
                  <MessageCircle className="stat-icon" />
                  <div className="stat-content">
                    <h3>{mockStats.totalChats}</h3>
                    <p>Total Chats</p>
                  </div>
                </div>
                <div className="stat-card">
                  <Heart className="stat-icon" />
                  <div className="stat-content">
                    <h3>{mockStats.avgMood}</h3>
                    <p>Average Mood</p>
                  </div>
                </div>
                <div className="stat-card">
                  <Calendar className="stat-icon" />
                  <div className="stat-content">
                    <h3>{mockStats.lastActivity}</h3>
                    <p>Last Activity</p>
                  </div>
                </div>
              </div>

              <div className="mood-tracker">
                <h3>Mood Trends</h3>
                <div className="mood-chart">
                  <div className="chart-placeholder">
                    <p>Mood tracking visualization would go here</p>
                    <small>Feature coming soon</small>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div className="history">
              <h3>Recent Conversations</h3>
              <div className="history-list">
                {mockHistory.map((item, index) => (
                  <div key={index} className="history-item">
                    <div className="history-date">{item.date}</div>
                    <div className="history-content">
                      <div className="history-emotion">{item.emotion}</div>
                      <div className="history-summary">{item.summary}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="settings">
              <h3>Account Settings</h3>
              <div className="settings-section">
                <h4>Profile Information</h4>
                <div className="form-group">
                  <label>Full Name</label>
                  <input type="text" value={user?.full_name || ''} readOnly />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input type="email" value={user?.email || ''} readOnly />
                </div>
                <div className="form-group">
                  <label>Username</label>
                  <input type="text" value={user?.username || ''} readOnly />
                </div>
              </div>

              <div className="settings-section">
                <h4>Privacy Settings</h4>
                <div className="setting-item">
                  <label>
                    <input type="checkbox" defaultChecked />
                    Allow mood tracking
                  </label>
                </div>
                <div className="setting-item">
                  <label>
                    <input type="checkbox" defaultChecked />
                    Enable crisis notifications
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;