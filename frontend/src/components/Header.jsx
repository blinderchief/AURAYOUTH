import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Heart, User, LogOut, MessageCircle, Home, AlertTriangle } from 'lucide-react';
import './Header.css';

const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <Link to="/" className="logo">
            <Heart className="logo-icon" />
            <span className="logo-text">AuraYouth</span>
          </Link>
          <nav className="nav">
            <Link to="/" className="nav-link">
              <Home size={18} />
              <span>Home</span>
            </Link>
            {isAuthenticated() && (
              <>
                <Link to="/chat" className="nav-link">
                  <MessageCircle size={18} />
                  <span>Chat</span>
                </Link>
                <Link to="/profile" className="nav-link">
                  <User size={18} />
                  <span>Profile</span>
                </Link>
              </>
            )}
            <Link to="/crisis-support" className="nav-link crisis-link">
              <AlertTriangle size={18} />
              <span>Crisis Support</span>
            </Link>
          </nav>
        </div>

        <div className="header-right">
          {isAuthenticated() ? (
            <div className="user-section">
              <span className="welcome-text">
                Welcome, {user?.full_name || user?.username}
              </span>
              <button onClick={handleLogout} className="logout-btn">
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <Link to="/login" className="login-btn">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;