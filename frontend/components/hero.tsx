import { DashboardBento } from "./dashboard-bento";

export function Hero() {
    return (
      <section className="flex flex-col items-center justify-center px-6 pt-24 pb-32 md:pt-32 md:pb-48 text-center">
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
        <div className="w-full mt-12 min-h-[600px]">
          <DashboardBento />
        </div>
      </section>

    )
  }
  