"use client"

import { useState } from "react"
import Link from "next/link"
import { Menu, X } from "lucide-react"

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="relative z-20 border-b border-gray-800/30 bg-black/50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="text-2xl font-bold text-white hover:text-gray-300 transition-colors">
            AISE
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex flex-1 items-center justify-center gap-8">
            <Link href="#about" className="text-gray-300 hover:text-white transition-colors font-medium">
              About Us
            </Link>
            <Link href="#studies" className="text-gray-300 hover:text-white transition-colors font-medium">
              Studies
            </Link>
            <Link href="#leaderboard" className="text-gray-300 hover:text-white transition-colors font-medium">
              Leaderboard
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-gray-300 hover:text-white transition-colors"
            aria-label="Toggle menu"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-3">
            <Link href="#about" className="block text-gray-300 hover:text-white transition-colors font-medium py-2">
              About Us
            </Link>
            <Link href="#studies" className="block text-gray-300 hover:text-white transition-colors font-medium py-2">
              Studies
            </Link>
            <Link
              href="#leaderboard"
              className="block text-gray-300 hover:text-white transition-colors font-medium py-2"
            >
              Leaderboard
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
