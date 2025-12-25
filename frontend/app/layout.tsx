import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
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
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8 relative">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>

          {/* Subtle background glow */}
          <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none -mr-48 -mt-48" />
          <div className="fixed bottom-0 left-0 w-[400px] h-[400px] bg-accent/5 blur-[100px] rounded-full pointer-events-none -ml-32 -mb-32" />
        </main>
      </body>
    </html>
  );
}
