
"use client";

import { useEffect, useState } from "react";
import { useOnboardingStore } from "@/lib/store/onboarding";
import { CheckCircle2, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";

export function StepReveal() {
    // Mock processing delay
    const [analyzing, setAnalyzing] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setAnalyzing(false);
        }, 2000);
        return () => clearTimeout(timer);
    }, []);

    if (analyzing) {
        return (
            <div className="text-center space-y-6 py-12 animate-in fade-in duration-500">
                <div className="relative w-24 h-24 mx-auto">
                    <div className="absolute inset-0 border-4 border-white/10 rounded-full" />
                    <div className="absolute inset-0 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="space-y-2">
                    <h2 className="text-xl font-bold animate-pulse">Synthesizing Belief State...</h2>
                    <p className="text-muted-foreground text-sm">Extracting evidence from GitHub commit history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="text-center space-y-8 animate-in fade-in zoom-in-95 duration-500">
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="w-24 h-24 bg-verifying/20 rounded-full flex items-center justify-center mx-auto border-4 border-verifying/20"
            >
                <CheckCircle2 className="w-12 h-12 text-verifying" />
            </motion.div>

            <div className="space-y-2">
                <h2 className="text-3xl font-bold">Passport Generated</h2>
                <p className="text-muted-foreground max-w-sm mx-auto">
                    We've established an initial belief state based on your provided evidence.
                </p>
            </div>

            <div className="grid grid-cols-2 gap-4 max-w-sm mx-auto">
                <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
                    <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-widest mb-1">Strongest Belief</p>
                    <p className="text-lg font-bold text-white">Python</p>
                    <p className="text-xs text-verifying mt-1">High Confidence</p>
                </div>
                <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
                    <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-widest mb-1">Testing Ground</p>
                    <p className="text-lg font-bold text-white">Backend Eng</p>
                    <p className="text-xs text-blue-400 mt-1">Recommended</p>
                </div>
            </div>

            <div className="pt-4">
                <Link
                    href="/dashboard"
                    className="w-full py-4 bg-white text-black rounded-xl font-bold shadow-[0_0_20px_rgba(255,255,255,0.2)] hover:shadow-[0_0_30px_rgba(255,255,255,0.4)] hover:scale-[1.02] transition-all flex items-center justify-center gap-2"
                >
                    Enter Laboratory <ArrowRight className="w-5 h-5" />
                </Link>
            </div>
        </div>
    );
}
