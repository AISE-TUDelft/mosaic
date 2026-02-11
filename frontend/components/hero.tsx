"use client"

import Link from "next/link"
// import { DashboardBento } from "./leaderboard"
import { InteractiveLogo } from "./interactive-logo"
import "../styles/glass-button.css"
import "../styles/affiliation.css"

export function Hero() {
  return (
    <>
      <section className="relative w-screen left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] h-screen flex flex-col items-start justify-start px-6 md:px-12 lg:px-24 pt-40">
        <div className="flex w-full gap-15 max-w-7xl mx-auto items-start">
          <div className="flex-1 min-w-3">
            {/* <Link href="/" className="flex items-center">
              <img 
                src="/mosaiclogo5.png" 
                alt="MOSAIC" 
                className="h-15 w-auto"
                style={{ imageRendering: 'crisp-edges' }}
              />
            </Link> */}

            <h2 className="text-4xl md:text-6xl lg:text-4xl font-light tracking-tight text-white mb-8 pt-5">
              Monitoring Open-Source Autonomous Agentic Activity in Collaborative Coding Environments
            </h2>

            <p className="text-gray-300 text-base md:text-lg leading-relaxed">
              MOSAIC brings real-world visibility to autonomous coding agents. Our approach democratizes agentic evaluation and supports the development of trustworthy AI-powered software engineering systems.
            </p>
            <div className="mt-8">
              <Link href="/contact" className="glass-button">
                Inquiries
              </Link>
            </div>
          </div>

          <div className="hidden lg:flex flex-1 items-start justify-center flex-shrink-0 pt-2">
            <InteractiveLogo />
          </div>
        </div>
      </section>

{/* We monitor agent activity in open-source collaborative coding environments, delivering transparent, real-world insight into agent behavior and collaboration. */}
      {/* Sponsors/Partnership Band */}
      <section className="affiliation-standard w-full bg-gradient-to-r from-gray-900/50 via-gray-800/50 to-gray-900/50 border-y border-gray-700 py-0 flex items-center justify-center h-25 -mt-10">
        <div className="flex items-center justify-between w-full max-w-7xl px-8 h-full">
          <div className="flex items-center h-full flex-1 justify-center pb-3">
            <img 
              src="/mosaic/international-logo_white_rgb@16x.png" 
              alt="International Logo" 
              className="h-35 w-auto object-contain"
              style={{ imageRendering: 'crisp-edges' }}
            />
          </div>
          <div className="flex items-center h-full flex-1 justify-center pt-2">
            <img 
              src="/mosaic/ucdavislogowhite.png" 
              alt="UC Davis Logo" 
              className="h-23 w-auto object-contain"
              style={{ imageRendering: 'crisp-edges' }}
            />
          </div>
          <div className="flex items-center h-full flex-1 justify-center pt-1">
            <img 
              src="/mosaic/githublogowhite.png" 
              alt="GitHub Logo" 
              className="h-10 w-auto object-contain"
              style={{ imageRendering: 'crisp-edges' }}
            />
          </div>
        </div>
      </section>

      {/* Pages Navigation Section */}
      <section className="px-6 py-85 md:px-16 lg:px-24">
        
        {/* Agent Monitor Section */}
        <div className="mb-85">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-light tracking-tight text-white mb-6">
                Agent Monitor
              </h2>
              <p className="text-gray-300 text-base md:text-lg leading-relaxed mb-8">
                Real-time monitoring of autonomous coding agents. Track agent behavior, performance metrics, and collaborative interactions in open-source environments.
              </p>
              <Link href="/mosaic" className="glass-button-standard">
                Explore Agent Monitor
              </Link>
            </div>
            <div className="h-80 bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-lg border border-gray-700 flex items-center justify-center">
              <p className="text-gray-500">Interactive Plot or Image</p>
            </div>
          </div>
        </div>

        {/* Leaderboards Section */}
        <div className="mb-85">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
            <div className="h-80 bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-lg border border-gray-700 flex items-center justify-center order-2 md:order-1">
              <p className="text-gray-500">Interactive Plot or Image</p>
            </div>
            <div className="order-1 md:order-2">
              <h2 className="text-4xl md:text-5xl font-light tracking-tight text-white mb-6">
                Leaderboards
              </h2>
              <p className="text-gray-300 text-base md:text-lg leading-relaxed mb-8">
                Comprehensive rankings and performance metrics of AI-enabled software engineering tools and systems. Compare agents across real-world scenarios and benchmarks.
              </p>
              <Link href="/leaderboard" className="glass-button-standard">
                View Leaderboards
              </Link>
            </div>
          </div>
        </div>

        {/* Studies Section */}
        <div className="mb-85">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-light tracking-tight text-white mb-6">
                Studies
              </h2>
              <p className="text-gray-300 text-base md:text-lg leading-relaxed mb-8">
                Explore our latest research studies and empirical findings on trustworthy AI systems and software engineering practices. Discover insights from real-world agent evaluation.
              </p>
              <Link href="/studies" className="glass-button-standard">
                Read Studies
              </Link>
            </div>
            <div className="h-80 bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-lg border border-gray-700 flex items-center justify-center">
              <p className="text-gray-500">Interactive Plot or Image</p>
            </div>
          </div>
        </div>

        {/* About Us Section */}
        <div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto items-center">
            <div className="h-80 bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-lg border border-gray-700 flex items-center justify-center order-2 md:order-1">
              <p className="text-gray-500">Interactive Plot or Image</p>
            </div>
            <div className="order-1 md:order-2">
              <h2 className="text-4xl md:text-5xl font-light tracking-tight text-white mb-6">
                About Us
              </h2>
              <p className="text-gray-300 text-base md:text-lg leading-relaxed mb-8">
                Learn more about our research lab, our team, and the interdisciplinary approaches we use to advance AI-enabled software engineering. Discover our mission and vision.
              </p>
              <Link href="/about" className="glass-button-standard">
                Learn More
              </Link>
            </div>
          </div>
        </div>

      </section>

      {/* Footer */}
      <footer className="w-full bg-gradient-to-br from-gray-900/50 to-gray-800/50 border-t border-gray-700 py-8 px-6 md:px-16 lg:px-24">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <p className="text-gray-400 text-sm">
            © 2026 MOSAIC. All rights reserved.
          </p>
          <div className="flex items-center gap-8">
            <Link href="/privacy" className="text-gray-400 text-sm hover:text-white transition-colors">
              Privacy
            </Link>
            <Link href="/terms" className="text-gray-400 text-sm hover:text-white transition-colors">
              Terms
            </Link>
            <Link href="/contact" className="text-gray-400 text-sm hover:text-white transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </footer>

      {/* Uncomment to show Dashboard
      <section className="w-full mt-12 min-h-[600px]">
        <DashboardBento />
      </section>
      */}
    </>
  )
}
  