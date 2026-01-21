"use client"

import Link from "next/link"
import { DashboardBento } from "./leaderboard"

export function Hero() {
  return (
    <>
      <section className="relative w-screen left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] flex flex-col items-center justify-start px-6 text-center pt-12 sm:pt-16 md:pt-20 lg:pt-24 pb-12 sm:pb-16 md:pb-20">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-light tracking-wider mb-4 bg-gradient-to-b from-[#4a8bc2] to-[#2a5a8a] bg-clip-text text-transparent">
          AISE
        </h1>

        <h2 className="text-4xl md:text-5xl lg:text-6xl font-light tracking-tight text-white mb-8">
          AI for Software Engineering
        </h2>

        <p className="max-w-2xl text-gray-300 text-base md:text-lg leading-relaxed text-balance">
          Our lab's mission is advance interdisciplinary approaches for building and assessing trustworthy AI-enabled
          software engineering systems that operate in real development workflows and measurably improve software
          efficiency and developer productivity.
        </p>
      </section>

      {/* Pages Navigation Section */}
      <section className="px-6 py-32 md:px-16 lg:px-24">
        <h2 className="text-4xl md:text-5xl font-light tracking-tight text-white text-center mb-16">
          Explore Our Work
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* About Us Card */}
          <Link href="/about" className="group">
            <div className="h-full p-8 rounded-lg border border-gray-700 hover:border-[#4a8bc2] transition-all duration-300 hover:shadow-lg hover:shadow-[#4a8bc2]/20 cursor-pointer bg-gradient-to-br from-gray-900/50 to-gray-800/50">
              <h3 className="text-2xl font-semibold text-white mb-3 group-hover:text-[#4a8bc2] transition-colors">
                About Us
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Learn more about our research lab, our team, and the interdisciplinary approaches we use to advance AI-enabled software engineering.
              </p>
            </div>
          </Link>

          {/* Studies Card */}
          <Link href="/studies" className="group">
            <div className="h-full p-8 rounded-lg border border-gray-700 hover:border-[#4a8bc2] transition-all duration-300 hover:shadow-lg hover:shadow-[#4a8bc2]/20 cursor-pointer bg-gradient-to-br from-gray-900/50 to-gray-800/50">
              <h3 className="text-2xl font-semibold text-white mb-3 group-hover:text-[#4a8bc2] transition-colors">
                Studies
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Explore our latest research studies and empirical findings on trustworthy AI systems and software engineering practices.
              </p>
            </div>
          </Link>

          {/* Leaderboard Card */}
          <Link href="/leaderboard" className="group">
            <div className="h-full p-8 rounded-lg border border-gray-700 hover:border-[#4a8bc2] transition-all duration-300 hover:shadow-lg hover:shadow-[#4a8bc2]/20 cursor-pointer bg-gradient-to-br from-gray-900/50 to-gray-800/50">
              <h3 className="text-2xl font-semibold text-white mb-3 group-hover:text-[#4a8bc2] transition-colors">
                Leaderboard
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                View performance metrics and rankings of AI-enabled software engineering tools and systems in real-world scenarios.
              </p>
            </div>
          </Link>
        </div>
      </section>

      {/* Uncomment to show Dashboard
      <section className="w-full mt-12 min-h-[600px]">
        <DashboardBento />
      </section>
      */}
    </>
  )
}
  