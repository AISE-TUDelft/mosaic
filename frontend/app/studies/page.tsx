"use client"

import { useState } from "react"
import Link from "next/link"
import "../../styles/glass-button.css"
// import "../styles/affiliation.css"

export const getAssetPath = (file: string) => {
  return process.env.NODE_ENV === "production" ? `/mosaic/${file}` : `/${file}`
}

interface Study {
  title: string
  authors: string
  venue: string
  year: string
  description: string
  pdf: string
  preview: string
}

const studies: Study[] = [
  {
    title: "Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time",
    authors: "Razvan Mihai Popescu, David Gros, Andrei Botocan, Rahul Pandita, Prem Devanbu, Maliheh Izadi",
    venue: "International Conference on Mining Software Repositories (MSR)",
    year: "2026",
    description: "In this work, we construct a novel dataset of approximately 110, 000 open-source pull requests, including associated commits, comments, reviews, issues, and file changes, collectively representing millions of lines of source code.",
    pdf: "MSR-134.pdf",
    preview: "agents_msr2026.png",
  },
]

export default function StudiesPage() {
  const [activePdf, setActivePdf] = useState<string | null>(null)

  return (
    <main className="px-6 md:px-16 lg:px-24 py-32 min-h-screen">
      
      {/* Header */}
      <div className="max-w-4xl mb-24">
        <h1 className="text-5xl md:text-6xl font-light tracking-tight text-white mb-6">
          Research Studies
        </h1>
        <p className="text-gray-400 text-lg leading-relaxed">
          Empirical investigations into trustworthy AI-enabled software
          engineering systems. Grounded in real-world autonomous agent activity.
        </p>
      </div>

      {/* Studies */}
      <div className="space-y-32 max-w-6xl">
        {studies.map((study, index) => (
          <div
            key={index}
            className="grid grid-cols-1 md:grid-cols-[1.3fr_0.7fr] gap-20 items-center"
          >
            {/* LEFT TEXT */}
            <div>
              <h2 className="text-3xl md:text-3xl font-light text-white mb-4">
                {study.title}
              </h2>

              <p className="text-sm text-gray-500 mb-6">
                {study.authors} · {study.venue}, {study.year}
              </p>
               {/* <p className="text-sm text-gray-500 mb-6">
                {study.venue} · {study.year}
              </p> */}

              <p className="text-gray-300 text-base leading-relaxed mb-8">
                {study.description}
              </p>

              <button
                onClick={() => setActivePdf(study.pdf)}
                className="glass-button-standard"
              >
                Read Paper
              </button>
            </div>

            {/* RIGHT PDF PREVIEW */}
            <div
              onClick={() => setActivePdf(study.pdf)}
              className="relative cursor-pointer group"
            >
              <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-white/5 opacity-0 group-hover:opacity-100 transition duration-500 blur-xl"></div>

              <div className="relative rounded-xl overflow-hidden border border-gray-700 bg-gradient-to-br from-gray-900/60 to-gray-800/60 backdrop-blur-xl transition duration-500 group-hover:scale-[1.02] group-hover:border-white/30">
                <img
                  src={getAssetPath(study.preview)}
                  alt="PDF preview"
                  className="w-full object-cover"
                />

                {/* Liquid Glass Overlay */}
                <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 backdrop-blur-sm transition duration-500 flex items-center justify-center">
                  <span className="text-black text-sm tracking-wide">
                    Open Paper →
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* PDF Modal */}
      {activePdf && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-10">
          <div className="relative w-full max-w-5xl h-[85vh] bg-gray-900 rounded-xl border border-gray-700 overflow-hidden">
            <button
              onClick={() => setActivePdf(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              ✕
            </button>

            <iframe
              src={getAssetPath(activePdf)}
              className="w-full h-full"
            />
          </div>
        </div>
      )}
    </main>
  )
}