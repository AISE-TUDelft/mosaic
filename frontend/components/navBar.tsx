'use client';

import React from 'react';
import Link from 'next/link';
import { LayoutDashboard } from 'lucide-react';
import { Button } from '@headlessui/react';

export default function Navbar() {
  const navItems = [
    { href: '/', label: 'About Us' },
    { href: '/', label: 'Studies'},
    { href: '/', label: 'Leaderboard'},
  ];

  return (
    <nav className="sticky top-0 w-full bg-slate-900 border-b border-slate-800 z-50">
      <div>
        <div className="flex items-center justify-between">
          {/* Logo and Desktop Nav */}
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-2 no-underline">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <LayoutDashboard className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">AISE</span>
            </Link>
          </div>
          {/* Navigation Links - Right Side */}
          <div className="grid grid-flow-col grid-cols-1 gap-y-4">
            {navItems.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className="no-underline text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors px-4 py-2"
              >
                {item.label}                
              </Link>
            ))}          
            <Link href="/" className="no-underline text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors px-4 py-2" >hello</Link>

          </div>
        </div>
      </div>
    </nav>
  );
}