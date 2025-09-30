'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { MessageCircle, Heart, Brain, Shield, LogOut } from 'lucide-react';

export default function Dashboard() {
  const [user, setUser] = useState<{username: string; email: string; full_name: string} | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Fetch user info
    fetch('http://localhost:8000/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(() => router.push('/login'));
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  if (!user) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Welcome, {user.full_name}</h1>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Chat Card */}
          <Link href="/chat" className="block">
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer">
              <MessageCircle className="w-12 h-12 text-blue-600 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Chat</h3>
              <p className="text-gray-600">Talk to your AI companion in real-time</p>
            </div>
          </Link>

          {/* Digital Twin Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <Heart className="w-12 h-12 text-purple-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Digital Twin</h3>
            <p className="text-gray-600">View your personalized AI profile</p>
          </div>

          {/* Emotion Recognition Card */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <Brain className="w-12 h-12 text-green-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Emotion Analysis</h3>
            <p className="text-gray-600">Understand your emotional state</p>
          </div>
        </div>

        {/* Trust Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Shield className="w-8 h-8 text-red-600 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Your Privacy & Safety</h3>
          <ul className="space-y-2 text-gray-600">
            <li>• All conversations are confidential and encrypted</li>
            <li>• Crisis detection helps ensure your safety</li>
            <li>• Your data is never shared without consent</li>
            <li>• 24/7 support for when you need it most</li>
          </ul>
        </div>
      </main>
    </div>
  );
}