import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ClientLayout } from "@/components/layout/ClientLayout";
import { GlobalLoader } from "@/components/ui/GlobalLoader";
import { Toaster } from "sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Career Scientist | The Failure Passport",
  description: "An Agentic AI system for career discovery through experimental testing of beliefs.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} flex min-h-screen bg-background text-foreground`}>
        <GlobalLoader />
        <Toaster position="bottom-right" theme="dark" />
        <ClientLayout>
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}
