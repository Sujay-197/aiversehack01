
"use client";

import { signIn } from "next-auth/react";
import { Copy, Github } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#0F172A] text-white relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none -mr-48 -mt-48" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-purple-500/10 blur-[100px] rounded-full pointer-events-none -ml-32 -mb-32" />

      <main className="z-10 flex flex-col items-center text-center space-y-8 px-4 max-w-3xl">
        <div className="space-y-4">
          <div className="inline-flex items-center px-3 py-1 rounded-full border border-white/10 bg-white/5 text-sm font-medium text-blue-400 mb-4">
            <span className="flex h-2 w-2 rounded-full bg-blue-400 mr-2 animate-pulse"></span>
            System Status: Nominal
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-gradient-to-b from-white to-white/60 bg-clip-text text-transparent pb-2">
            The Career Scientist
          </h1>

          <p className="text-xl md:text-2xl text-slate-400 font-light max-w-2xl mx-auto leading-relaxed">
            Stop guessing. Start testing. <br />
            Turn your job search into a <span className="text-white font-medium">scientific loop</span>.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-lg mt-8">
          <div className="p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <h3 className="font-semibold text-white mb-1">Identity</h3>
            <p className="text-sm text-slate-400">Stable Experiment Subject</p>
          </div>
          <div className="p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <h3 className="font-semibold text-white mb-1">Failure</h3>
            <p className="text-sm text-slate-400">Valuable Data Point</p>
          </div>
        </div>

        <div className="pt-8">
          <button
            onClick={() => signIn("github", { callbackUrl: "/dashboard" })}
            className="group relative inline-flex items-center gap-3 px-8 py-4 bg-white text-slate-900 rounded-full font-semibold text-lg hover:bg-slate-200 transition-all duration-200 shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:shadow-[0_0_30px_rgba(255,255,255,0.5)]"
          >
            <Github className="w-6 h-6" />
            <span>Login with GitHub</span>
            <div className="absolute inset-0 rounded-full ring-2 ring-white/50 group-hover:ring-white/80 transition-all duration-300 animate-pulse" />
          </button>

          <p className="mt-4 text-sm text-slate-500">
            By logging in, you accept the <span className="underline decoration-slate-600 underline-offset-4">Protocol</span>.
          </p>
        </div>
      </main>
    </div>
  );
}
