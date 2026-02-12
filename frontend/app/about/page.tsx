"use client"

import Link from "next/link"
import { Header } from "../../components/header"
import { InteractiveLogo } from "../../components/interactive-logo"
import "../../styles/affiliation.css"
import "../../styles/glass-button.css"

const members = [
  {
    name: "Placeholder Name",
    role: "Principal Investigator · TU Delft",
    description:
      "Placeholder description",
    image: "/placeholder-member.png",
    links: {
      website: "#",
      github: "#",
      linkedin: "#",
    },
  },
  {
    name: "Placeholder Name",
    role: "PhD Researcher · UC Davis",
    description:
      "Placeholder description",
    image: "/placeholder-member.png",
    links: {
      website: "#",
      github: "#",
      linkedin: "#",
    },
  },
]

export default function AboutPage() {
  return (
    <main className="px-6 md:px-16 lg:px-24 py-32 min-h-screen">

      {/* Header */}
      <div className="max-w-4xl mb-24">
        <h1 className="text-5xl md:text-6xl font-light tracking-tight text-white mb-6">
          About MOSAIC
        </h1>
        <p className="text-gray-400 text-lg leading-relaxed">
          An interdisciplinary research initiative monitoring autonomous agent
          activity in collaborative coding environments.
        </p>
      </div>

      {/* Lab / Institution Section */}
      <div className="mb-32">
        <h2 className="text-3xl md:text-4xl font-light text-white mb-16 border-b border-gray-700 pb-6">
          AI & Software Engineering Lab
        </h2>

        <div className="space-y-28">
          {members.map((member, index) => (
            <div
              key={index}
              className="grid grid-cols-1 md:grid-cols-[1.6fr_0.4fr] gap-16 items-center"
            >
              {/* LEFT TEXT */}
              <div>
                <h3 className="text-2xl md:text-3xl font-light text-white mb-2">
                  {member.name}
                </h3>

                <p className="text-sm text-gray-500 mb-6 italic">
                  {member.role}
                </p>

                <p className="text-gray-300 leading-relaxed mb-8 max-w-2xl">
                  {member.description}
                </p>

                <div className="flex gap-6 text-sm text-gray-400">
                  <Link
                    href={member.links.website}
                    className="hover:text-white transition-colors"
                  >
                    Website
                  </Link>
                  <Link
                    href={member.links.github}
                    className="hover:text-white transition-colors"
                  >
                    GitHub
                  </Link>
                  <Link
                    href={member.links.linkedin}
                    className="hover:text-white transition-colors"
                  >
                    LinkedIn
                  </Link>
                </div>
              </div>

              {/* RIGHT PHOTO */}
              <div className="flex justify-end">
                <div className="relative w-52 h-64 rounded-2xl overflow-hidden border border-gray-700 bg-gradient-to-br from-gray-900/60 to-gray-800/60 backdrop-blur-xl shadow-2xl shadow-black/40 group transition duration-500 hover:scale-[1.03]">
                  
                  {/* Placeholder image */}
                  <img
                    src={member.image}
                    alt={member.name}
                    className="w-full h-full object-cover"
                  />

                  {/* Subtle glass overlay */}
                  <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition duration-500 backdrop-blur-sm" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Optional second institution example */}
      <div>
        <h2 className="text-3xl md:text-4xl font-light text-white mb-16 border-b border-gray-700 pb-6">
          Collaborating Institutions
        </h2>

        <p className="text-gray-400 max-w-3xl">
          MOSAIC is a collaboration between research groups at TU Delft,
          UC Davis, and open-source AI communities worldwide.
        </p>
      </div>

    </main>
  )
}