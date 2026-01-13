import Link from "next/link"

export function Header() {
  return (
    <header className="flex items-center justify-between px-8 py-6 md:px-16 lg:px-24">
      <Link href="/" className="text-xl font-bold tracking-wide">
        AISE
      </Link>

      <nav className="flex items-center gap-12">
        <Link href="/about" className="text-sm text-gray-300 hover:text-white transition-colors">
          About Us
        </Link>
        <Link href="/studies" className="text-sm text-gray-300 hover:text-white transition-colors">
          Studies
        </Link>
        <Link href="/leaderboard" className="text-sm text-gray-300 hover:text-white transition-colors">
          Leaderboard
        </Link>
      </nav>
    </header>
  )
}
