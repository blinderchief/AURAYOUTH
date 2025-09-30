import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AuraYouth - AI-Powered Mental Wellness for Youth",
  description: "Empathetic, confidential AI mental health support designed for young people. Build trust with advanced AI technology.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className="antialiased"
        suppressHydrationWarning={true}
      >
        {children}
      </body>
    </html>
  );
}
