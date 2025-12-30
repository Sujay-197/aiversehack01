"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
    CheckSquare,
    Square,
    ExternalLink,
    ChevronLeft,
    Clock,
    CheckCircle2
} from "lucide-react";
import { cn } from "@/lib/utils";

interface ActiveExperimentViewProps {
    experiment: any;
    onComplete: (result: string, feedback: string) => void; // Opens modal in parent
    onAbandon: () => void; // Just returns to main view
    requestCompletion: () => void; // Triggers the modal open in parent
}

export function ActiveExperimentView({ experiment, requestCompletion, onAbandon }: ActiveExperimentViewProps) {
    const defaultSteps = experiment.action_plan || [
        "Review requirements",
        "Prepare materials",
        "Execute task",
        "Verify results"
    ];

    // Local state for checking off items (persisted just in memory for session)
    const [checkedState, setCheckedState] = useState<boolean[]>(new Array(defaultSteps.length).fill(false));

    const toggleStep = (idx: number) => {
        const newState = [...checkedState];
        newState[idx] = !newState[idx];
        setCheckedState(newState);
    };

    const progress = Math.round((checkedState.filter(Boolean).length / defaultSteps.length) * 100);

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-8"
        >
            <div className="flex items-center gap-4 text-muted-foreground mb-4">
                <button
                    onClick={onAbandon}
                    className="flex items-center gap-1 hover:text-white transition-colors text-sm"
                >
                    <ChevronLeft className="w-4 h-4" /> Back to Planning
                </button>
                <div className="h-4 w-[1px] bg-white/10" />
                <span className="text-xs font-mono uppercase tracking-widest text-primary flex items-center gap-2">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                    </span>
                    Constrained Development Mode
                </span>
            </div>

            {/* Header Card */}
            <div className="glass rounded-3xl p-8 border-l-4 border-l-primary relative overflow-hidden">
                <div className="relative z-10">
                    <h1 className="text-3xl font-bold mb-2">{experiment.title}</h1>
                    <p className="text-xl text-muted-foreground italic">&ldquo;{experiment.hypothesis}&rdquo;</p>

                    <div className="flex items-center gap-6 mt-6">
                        {experiment.company && (
                            <div className="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-sm font-medium">
                                Target: {experiment.company}
                            </div>
                        )}
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Clock className="w-4 h-4" /> Started today
                        </div>
                    </div>
                </div>
                {/* Background Decoration */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: Action Plan */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h3 className="text-xl font-bold">Action Plan</h3>
                        <span className="text-sm font-mono text-muted-foreground">{progress}% Complete</span>
                    </div>

                    <div className="space-y-3">
                        {defaultSteps.map((step: string, idx: number) => (
                            <div
                                key={idx}
                                onClick={() => toggleStep(idx)}
                                className={cn(
                                    "p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-4 group",
                                    checkedState[idx]
                                        ? "bg-primary/5 border-primary/20"
                                        : "bg-white/5 border-white/5 hover:bg-white/10"
                                )}
                            >
                                <div className={cn(
                                    "mt-1 w-5 h-5 rounded border flex items-center justify-center transition-colors",
                                    checkedState[idx] ? "bg-primary border-primary text-black" : "border-white/20 group-hover:border-white/40"
                                )}>
                                    {checkedState[idx] && <CheckSquare className="w-3 h-3" />}
                                </div>
                                <span className={cn(
                                    "text-lg",
                                    checkedState[idx] ? "text-muted-foreground line-through" : "text-foreground"
                                )}>{step}</span>
                            </div>
                        ))}
                    </div>

                    <div className="pt-6">
                        <button
                            onClick={requestCompletion}
                            className="w-full py-4 bg-green-500/10 hover:bg-green-500/20 text-green-400 border border-green-500/20 rounded-2xl font-bold transition-all flex items-center justify-center gap-3"
                        >
                            <CheckCircle2 className="w-5 h-5" />
                            Mark Experiment as Complete
                        </button>
                    </div>
                </div>

                {/* Right: Resources & Focus */}
                <div className="space-y-6">
                    <div className="glass rounded-2xl p-6 space-y-4">
                        <h4 className="font-bold text-sm uppercase tracking-wider text-muted-foreground">Resources</h4>
                        <div className="space-y-2">
                            <a href="#" className="flex items-center gap-2 text-primary hover:underline text-sm truncate">
                                <ExternalLink className="w-3 h-3" /> Search Google for {experiment.role || "Topic"}
                            </a>
                            <a href="#" className="flex items-center gap-2 text-primary hover:underline text-sm truncate">
                                <ExternalLink className="w-3 h-3" /> GitHub: Similar Repos
                            </a>
                        </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-gradient-to-br from-purple-500/10 to-blue-500/5 border border-purple-500/10 text-center">
                        <p className="font-bold mb-2">Focus Mode On</p>
                        <p className="text-xs text-muted-foreground">
                            Suggestions are hidden to prevent context switching. Complete this task to unlock new hypotheses.
                        </p>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
