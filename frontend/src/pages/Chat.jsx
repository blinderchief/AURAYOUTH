import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { Send, Mic, Camera, Upload, AlertTriangle, Heart } from 'lucide-react';
import './Chat.css';

const Chat = () => {
  const { user, isAuthenticated } = useAuth();
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Hi! I\'m Aura, your mental wellness companion. How are you feeling today?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [multimodalEnabled, setMultimodalEnabled] = useState(false);
  const [uploadingAudio, setUploadingAudio] = useState(false);
  const [uploadingVideo, setUploadingVideo] = useState(false);
  const [websocket, setWebsocket] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  const messagesEndRef = useRef(null);
  const audioInputRef = useRef(null);
  const videoInputRef = useRef(null);
  const wsRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // WebSocket connection setup
  const connectWebSocket = useCallback(() => {
    if (!isAuthenticated || !user) return;

    const wsUrl = `ws://localhost:8000/ws/chat/${user.username}`;
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
      wsRef.current = ws;
      setWebsocket(ws);
    };

    ws.onmessage = (event) => {
      try {
        const responseData = JSON.parse(event.data);
        const botMessage = {
          id: Date.now(),
          type: 'bot',
          content: responseData.content,
          emotion: responseData.emotion,
          confidence: responseData.confidence,
          crisisDetected: responseData.crisis_detected,
          crisisType: responseData.crisis_type,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
        setLoading(false);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
        setLoading(false);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
      wsRef.current = null;
      setWebsocket(null);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
      setLoading(false);
    };

    return ws;
  }, [isAuthenticated, user]);

  // Connect WebSocket on component mount and user authentication
  useEffect(() => {
    if (isAuthenticated && user) {
      const ws = connectWebSocket();
      return () => {
        if (ws) {
          ws.close();
        }
      };
    }
  }, [isAuthenticated, user, connectWebSocket]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setLoading(true);

    try {
      // Use WebSocket for real-time chat if connected
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        const requestData = {
          id: userMessage.id,
          message: messageToSend,
          user_id: user?.username || 'anonymous',
          context: messages.slice(-5).map(msg => ({ type: msg.type, content: msg.content }))
        };

        wsRef.current.send(JSON.stringify(requestData));
        
        // Clear uploaded files if multimodal was used
        if (multimodalEnabled) {
          setAudioFile(null);
          setVideoFile(null);
        }
      } else {
        // Fallback to HTTP request if WebSocket is not available
        const requestData = {
          message: messageToSend,
          user_id: user?.username || 'anonymous',
          context: {}
        };

        // Add multimodal data if enabled and files are available
        if (multimodalEnabled) {
          if (audioFile) requestData.audio_file = audioFile;
          if (videoFile) requestData.video_file = videoFile;
        }

        const endpoint = multimodalEnabled ? '/chat/multimodal' : '/chat';
        const response = await axios.post(`http://localhost:8000${endpoint}`, requestData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: response.data.response,
          emotion: response.data.emotion,
          confidence: response.data.confidence,
          crisisDetected: response.data.crisis_detected,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, botMessage]);
        setLoading(false);

        // Clear uploaded files after use
        if (multimodalEnabled) {
          setAudioFile(null);
          setVideoFile(null);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'I\'m sorry, I\'m having trouble connecting right now. Please try again later.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleAudioUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('audio/')) {
      alert('Please select a valid audio file');
      return;
    }

    setUploadingAudio(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/upload/audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setAudioFile(response.data.file_path);
    } catch (error) {
      console.error('Error uploading audio:', error);
      alert('Failed to upload audio file');
    } finally {
      setUploadingAudio(false);
    }
  };

  const handleVideoUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('video/')) {
      alert('Please select a valid video file');
      return;
    }

    setUploadingVideo(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/upload/video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setVideoFile(response.data.file_path);
    } catch (error) {
      console.error('Error uploading video:', error);
      alert('Failed to upload video file');
    } finally {
      setUploadingVideo(false);
    }
  };

  if (!isAuthenticated()) {
    return (
      <div className="chat-unauthorized">
        <div className="unauthorized-card">
          <Heart className="unauthorized-icon" />
          <h2>Please Sign In</h2>
          <p>You need to be logged in to access the chat feature.</p>
          <a href="/login" className="login-link">Go to Login</a>
        </div>
      </div>
    );
  }

  return (
    <div className="chat">
      <div className="chat-container">
        <div className="chat-header">
          <div className="chat-info">
            <Heart className="chat-avatar" />
            <div>
              <h2>Aura</h2>
              <p>Your mental wellness companion</p>
              <div className={`connection-status ${connectionStatus}`}>
                <div className="status-indicator"></div>
                {connectionStatus === 'connected' && 'Connected'}
                {connectionStatus === 'disconnected' && 'Connecting...'}
                {connectionStatus === 'error' && 'Connection Error'}
              </div>
            </div>
          </div>
          <div className="multimodal-toggle">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={multimodalEnabled}
                onChange={(e) => setMultimodalEnabled(e.target.checked)}
              />
              <span className="toggle-slider"></span>
              Multimodal Analysis
            </label>
          </div>
        </div>

        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.type} ${message.crisisDetected ? 'crisis' : ''}`}
            >
              <div className="message-content">
                {message.crisisDetected && (
                  <div className="crisis-alert">
                    <AlertTriangle size={16} />
                    <span>Crisis Support Alert</span>
                  </div>
                )}
                <p>{message.content}</p>
                {message.emotion && (
                  <div className="message-meta">
                    <span className="emotion">Emotion: {message.emotion}</span>
                    {message.confidence && (
                      <span className="confidence">
                        Confidence: {(message.confidence * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                )}
              </div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message bot loading">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          {multimodalEnabled && (
            <div className="file-uploads">
              <input
                ref={audioInputRef}
                type="file"
                accept="audio/*"
                onChange={handleAudioUpload}
                style={{ display: 'none' }}
              />
              <button
                className={`upload-btn ${audioFile ? 'uploaded' : ''}`}
                onClick={() => audioInputRef.current?.click()}
                disabled={uploadingAudio}
                title="Upload Audio"
              >
                <Mic size={18} />
                {uploadingAudio ? 'Uploading...' : audioFile ? 'Audio ✓' : 'Audio'}
              </button>

              <input
                ref={videoInputRef}
                type="file"
                accept="video/*"
                onChange={handleVideoUpload}
                style={{ display: 'none' }}
              />
              <button
                className={`upload-btn ${videoFile ? 'uploaded' : ''}`}
                onClick={() => videoInputRef.current?.click()}
                disabled={uploadingVideo}
                title="Upload Video"
              >
                <Camera size={18} />
                {uploadingVideo ? 'Uploading...' : videoFile ? 'Video ✓' : 'Video'}
              </button>
            </div>
          )}

          <div className="input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Share how you're feeling..."
              disabled={loading}
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !inputMessage.trim()}
              className="send-btn"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;