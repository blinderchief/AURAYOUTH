import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Heart, Eye, EyeOff, AlertCircle } from 'lucide-react';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    username: 'testuser',
    password: 'password'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(formData.username, formData.password);

    if (result.success) {
      navigate('/chat');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="login">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <div className="login-logo">
              <Heart className="login-logo-icon" />
              <h1>AuraYouth</h1>
            </div>
            <h2>Welcome Back</h2>
            <p>Sign in to continue your mental wellness journey</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {error && (
              <div className="error-message">
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            )}

            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                placeholder="Enter your username"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="password-input">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="login-btn"
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>

          <div className="login-footer">
            <p>
              Don't have an account?{' '}
              <Link to="/crisis-support" className="crisis-link">
                Need immediate help?
              </Link>
            </p>
          </div>
        </div>

        <div className="login-info">
          <div className="info-card">
            <h3>Demo Credentials</h3>
            <p>For testing purposes, use:</p>
            <div className="demo-creds">
              <div><strong>Username:</strong> testuser</div>
              <div><strong>Password:</strong> password</div>
            </div>
          </div>

          <div className="info-card">
            <h3>Why Choose AuraYouth?</h3>
            <ul>
              <li>24/7 AI-powered support</li>
              <li>Crisis detection and intervention</li>
              <li>Multimodal emotion analysis</li>
              <li>Confidential and secure</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;