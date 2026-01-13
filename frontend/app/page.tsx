import { Header } from "../components/header"
import { Hero } from "../components/hero"

export default function Home() {
  return (
    <main className="relative min-h-screen bg-[#0a0e17] text-white overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-60"
        style={{ backgroundImage: "url('/background.png')" }}
      />

      <div className="absolute inset-0 bg-gradient-to-b from-[#0a0e17]/80 via-transparent to-[#0a0e17]/90" />

      {/* Content */}
      <div className="relative z-10">
        <Header />
        <Hero />
      </div>
    </main>
  )
}
