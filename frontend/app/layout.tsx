import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
// import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { Header } from "@/components/header"

const _geist = Geist({ subsets: ["latin"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AISE - AI for Software Engineering",
  description:
    "Advancing interdisciplinary approaches for building and assessing trustworthy AI-enabled software engineering systems",
  generator: "v0.app",
  // icons: {
  //   icon: [
  //     {
  //       url: "/icon-light-32x32.png",
  //       media: "(prefers-color-scheme: light)",
  //     },
  //     {
  //       url: "/icon-dark-32x32.png",
  //       media: "(prefers-color-scheme: dark)",
  //     },
  //     {
  //       url: "/icon.svg",
  //       type: "image/svg+xml",
  //     },
  //   ],
  //   apple: "/apple-icon.png",
  // },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans antialiased`}>
         <main className="relative min-h-screen bg-[#0a0e17] text-white overflow-hidden">
              <div
                className="absolute inset-0 bg-cover bg-center bg-no-repeat bg-fixed opacity-20"
                style={{ backgroundImage: "url('/background.png')" }}
              />    
              <div className="absolute inset-0 bg-gradient-to-b from-[#0a0e17]/80 via-transparent to-[#0a0e17]/90" />      
              {/* Content */}
              <div className="relative z-10">
                <Header />
                {children}
              </div>
            </main>
      </body>
    </html>
  )
}
