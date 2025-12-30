"use client";

import { useOnboardingStore, type OnboardingStep } from "@/lib/store/onboarding";
import { StepIngestion } from "@/components/onboarding/StepIngestion";
import { StepClarification } from "@/components/onboarding/StepClarification";
import { StepReveal } from "@/components/onboarding/StepReveal";
import { ShieldCheck } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function OnboardingPage() {
    const { step } = useOnboardingStore();
    const { status } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (status === "unauthenticated") {
            router.push("/");
        }
    }, [status, router]);

    if (status === "loading" || status === "unauthenticated") {
        return null; // Or a spinner
    }

    return (
        <div className="min-h-[90vh] flex items-center justify-center py-12">
            <div className="max-w-xl w-full space-y-8 px-4">
                {/* Header - Hidden on Reveal step to focus attention */}
                {step !== 'reveal' && (
                    <div className="text-center space-y-4 animate-in fade-in slide-in-from-top-4 duration-700">
                        <motion.div
                            initial={{ scale: 0.5, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            className="w-16 h-16 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center mx-auto shadow-2xl shadow-primary/20"
                        >
                            <ShieldCheck className="w-8 h-8 text-primary" />
                        </motion.div>
                        <h1 className="text-3xl font-black tracking-tighter italic uppercase bg-gradient-to-br from-white to-white/50 bg-clip-text text-transparent">
                            Protocol Initialization
                        </h1>

                        {/* Progress Steps */}
                        <div className="flex items-center justify-center gap-2 mt-4">
                            <div className={`h-1 rounded-full transition-all duration-500 ${step === 'ingestion' ? 'w-8 bg-primary' : 'w-2 bg-white/20'}`} />
                            <div className={`h-1 rounded-full transition-all duration-500 ${step === 'clarification' ? 'w-8 bg-primary' : 'w-2 bg-white/20'}`} />
                            <div className={`h-1 rounded-full transition-all duration-500 ${(step as OnboardingStep) === 'reveal' ? 'w-8 bg-primary' : 'w-2 bg-white/20'}`} />
                        </div>
                    </div>
                )}

                {/* Main Content Area */}
                <div className="glass rounded-[40px] p-8 md:p-12 relative overflow-hidden ring-1 ring-white/10 shadow-2xl">
                    <AnimatePresence mode="wait">
                        {step === 'ingestion' && (
                            <motion.div key="ingestion" exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }}>
                                <StepIngestion />
                            </motion.div>
                        )}
                        {step === 'clarification' && (
                            <motion.div key="clarification" exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }}>
                                <StepClarification />
                            </motion.div>
                        )}
                        {step === 'reveal' && (
                            <motion.div key="reveal" exit={{ opacity: 0, scale: 0.95 }} transition={{ duration: 0.3 }}>
                                <StepReveal />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}
