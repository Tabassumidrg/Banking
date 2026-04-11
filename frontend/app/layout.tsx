import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NexBank — Modern Digital Banking",
  description: "Secure, modern digital banking experience. Sign in or create your account to get started.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
