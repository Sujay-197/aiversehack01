"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    Upload,
    FileText,
    CheckCircle2,
    Loader2,
    ArrowRight,
    ShieldCheck
} from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

export default function Onboarding() {
    const [step, setStep] = useState(1);
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const startAnalysis = () => {
        setIsUploading(true);
        // Simulate API call
        setTimeout(() => {
            setIsUploading(false);
            setStep(2);
        }, 3000);
    };

    return (
        <div className="min-h-[80vh] flex items-center justify-center">
            <div className="max-w-2xl w-full space-y-8">
                <div className="text-center space-y-4">
                    <motion.div
                        initial={{ scale: 0.5, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="w-20 h-20 bg-primary/20 rounded-3xl flex items-center justify-center mx-auto"
                    >
                        <ShieldCheck className="w-10 h-10 text-primary" />
                    </motion.div>
                    <h2 className="text-4xl font-black tracking-tight italic uppercase">Researcher Onboarding</h2>
                    <p className="text-muted-foreground text-lg">Initialize your Failure Passport by providing evidence of your current skills.</p>
                </div>

                <div className="glass rounded-[40px] p-10 relative overflow-hidden">
                    <AnimatePresence mode="wait">
                        {step === 1 ? (
                            <motion.div
                                key="step1"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="space-y-8"
                            >
                                <div className="space-y-4">
                                    <h3 className="text-xl font-bold flex items-center gap-2">
                                        <span className="w-8 h-8 rounded-full bg-primary/20 text-primary flex items-center justify-center text-sm">1</span>
                                        Upload Your Resume
                                    </h3>

                                    <label className={cn(
                                        "block w-full h-48 border-2 border-dashed rounded-3xl cursor-pointer transition-all flex flex-col items-center justify-center gap-4 group",
                                        file ? "border-primary bg-primary/5" : "border-white/10 hover:border-primary/50 hover:bg-white/5"
                                    )}>
                                        <input type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
                                        {file ? (
                                            <>
                                                <FileText className="w-12 h-12 text-primary" />
                                                <div className="text-center">
                                                    <p className="font-bold">{file.name}</p>
                                                    <p className="text-xs text-muted-foreground uppercase mt-1 tracking-widest">File matches requirements</p>
                                                </div>
                                            </>
                                        ) : (
                                            <>
                                                <Upload className="w-12 h-12 text-muted-foreground group-hover:text-primary transition-colors" />
                                                <div className="text-center">
                                                    <p className="font-bold">Drop your PDF here</p>
                                                    <p className="text-sm text-muted-foreground mt-1">or click to browse files</p>
                                                </div>
                                            </>
                                        )}
                                    </label>
                                </div>

                                <button
                                    disabled={!file || isUploading}
                                    onClick={startAnalysis}
                                    className="w-full py-5 bg-primary text-white rounded-2xl font-black uppercase tracking-widest shadow-xl shadow-primary/20 hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center justify-center gap-3"
                                >
                                    {isUploading ? (
                                        <>
                                            <Loader2 className="w-6 h-6 animate-spin" />
                                            Analyzing Records...
                                        </>
                                    ) : (
                                        <>
                                            Begin Analysis <ArrowRight className="w-6 h-6" />
                                        </>
                                    )}
                                </button>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="step2"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="text-center space-y-8"
                            >
                                <div className="w-20 h-20 bg-verifying/20 rounded-full flex items-center justify-center mx-auto border-2 border-verifying/20">
                                    <CheckCircle2 className="w-10 h-10 text-verifying" />
                                </div>

                                <div className="space-y-2">
                                    <h3 className="text-2xl font-bold italic tracking-tight uppercase">Analysis Complete</h3>
                                    <p className="text-muted-foreground">We extracted 6 core beliefs and 14 pieces of technical evidence from your resume.</p>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-left">
                                        <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-widest">Top Belief</p>
                                        <p className="text-lg font-bold">Python Engineering</p>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-left">
                                        <p className="text-[10px] uppercase font-bold text-muted-foreground tracking-widest">Avg Confidence</p>
                                        <p className="text-lg font-bold text-verifying">42%</p>
                                    </div>
                                </div>

                                <Link
                                    href="/passport"
                                    className="block w-full py-5 bg-foreground text-background rounded-2xl font-black uppercase tracking-widest hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-3"
                                >
                                    Enter Laboratory <ArrowRight className="w-6 h-6" />
                                </Link>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Progress Indicator */}
                    <div className="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
                        <div className={cn("w-2 h-2 rounded-full transition-all", step === 1 ? "bg-primary w-6" : "bg-white/20")} />
                        <div className={cn("w-2 h-2 rounded-full transition-all", step === 2 ? "bg-primary w-6" : "bg-white/20")} />
                    </div>
                </div>
            </div>
        </div>
    );
}
