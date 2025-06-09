import './globals.css'

export const metadata = {
  title: 'Summer Camp Chatbot',
  description: 'Find the perfect summer camp for your child',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
