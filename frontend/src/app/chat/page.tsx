'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Send, Mic, Video } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  emotion?: string;
  confidence?: number;
  crisis_detected?: boolean;
  timestamp: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [userId, setUserId] = useState('');
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Get user info to set userId
    fetch('http://localhost:8000/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => {
        setUserId(data.username);
        connectWebSocket(data.username);
      })
      .catch(() => router.push('/login'));
  }, [router]);

  const connectWebSocket = (uid: string) => {
    console.log('Connecting to WebSocket for user:', uid);
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${uid}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Received message:', data);
      const newMessage: Message = {
        id: data.id || Date.now().toString(),
        type: 'bot',
        content: data.content,
        emotion: data.emotion,
        confidence: data.confidence,
        crisis_detected: data.crisis_detected,
        timestamp: data.timestamp,
      };
      setMessages(prev => [...prev, newMessage]);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };
  };

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current || !isConnected) return;

    console.log('Sending message:', input);
    const messageId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const userMessage: Message = {
      id: messageId,
      type: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);

    const messageData = {
      id: messageId,
      message: input,
      context: messages.slice(-5), // Last 5 messages for context
    };

    wsRef.current.send(JSON.stringify(messageData));
    setInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">AI Chat Companion</h1>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 max-w-4xl mx-auto w-full px-6 py-4 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-900 shadow-md'
                }`}
              >
                <p>{message.content}</p>
                {message.emotion && message.type === 'bot' && (
                  <div className="mt-2 text-xs opacity-75">
                    Emotion: {message.emotion} ({Math.round((message.confidence || 0) * 100)}% confidence)
                    {message.crisis_detected && (
                      <span className="ml-2 text-red-500 font-semibold">⚠️ Crisis Detected</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-4">
          <div className="flex-1 flex items-center gap-2">
            <button className="p-2 text-gray-500 hover:text-gray-700">
              <Mic className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-500 hover:text-gray-700">
              <Video className="w-5 h-5" />
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 placeholder-gray-500"
              disabled={!isConnected}
              style={{ color: 'black' }}
            />
          </div>
          <button
            onClick={sendMessage}
            disabled={!input.trim() || !isConnected}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white p-2 rounded-lg transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}