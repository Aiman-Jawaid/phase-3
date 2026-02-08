import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Todo Dashboard',
  description: 'A clean, professional todo dashboard application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-light-gray min-h-screen">
        <div className="container mx-auto px-4 py-8">
          {children}
        </div>
      </body>
    </html>
  );
}