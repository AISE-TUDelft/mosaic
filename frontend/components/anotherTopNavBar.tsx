import React from 'react';
import { Book } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Top Navigation Bar */}
      <nav className="fixed top-0 w-full bg-slate-900 border-b border-slate-800 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and Project Name - Left Side */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Book className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold">Research Hub</span>
            </div>

            {/* Navigation Items - Right Side */}
            <div className="flex space-x-6">
              <a
                href="#about"
                className="text-slate-300 hover:text-white transition-colors font-medium"
              >
                About us
              </a>
              <a
                href="#leaderboard"
                className="text-slate-300 hover:text-white transition-colors font-medium"
              >
                Leaderboard
              </a>
              <a
                href="#studies"
                className="text-slate-300 hover:text-white transition-colors font-medium"
              >
                Studies
              </a>
            </div>
          </div>
        </div>
      </nav>      
    </div>
  );
}