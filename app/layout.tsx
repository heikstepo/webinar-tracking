import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sol Twenty — Tracking Dashboard",
  description: "Unified funnel & revenue tracking across all sources",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
