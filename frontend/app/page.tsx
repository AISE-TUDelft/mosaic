import { Header } from "../components/header"
import { Hero } from "../components/hero"

export default function Home() {
  return (
    <main >     
      {/* Content */}
      <div className="relative z-10">
        <Hero />
      </div>
    </main>
  )
}
