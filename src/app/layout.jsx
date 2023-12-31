import { Inter } from 'next/font/google'

import ToastProvider from '@/providers/ToastProvider'
import '@/app/globals.css'

const inter = Inter({
  subsets: ['latin'],
})

export const metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
}

const RootLayout = ({
  children,
}) => {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ToastProvider />
        {children}
      </body>
    </html>
  )
}

export default RootLayout
