import Link from "next/link"
import Image from "next/image"

export function Header() {
  return (
    <header className="flex items-center justify-between px-8 py-10 md:px-16 lg:px-24">
      <Link href="/" className="text-xl font-bold tracking-wide text-white">
        MOSAIC
      </Link>

      <nav className="flex items-center gap-12">
        <Link href="/mosaic" className="text-sm text-gray-300 hover:text-white transition-colors">
        Agent Monitor
        </Link>
        <Link href="/leaderboard" className="text-sm text-gray-300 hover:text-white transition-colors">
          Leaderboards 
        </Link>
        <Link href="/studies" className="text-sm text-gray-300 hover:text-white transition-colors">
          Studies
        </Link>
        <Link href="/about" className="text-sm text-gray-300 hover:text-white transition-colors">
          About us
        </Link>
      </nav>
    </header>
  )
}
