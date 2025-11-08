import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'EDGE-QI Traffic Simulation',
  description: 'High-performance 3D traffic intersection simulation with real-time analytics',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
