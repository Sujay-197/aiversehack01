"use client";

import { motion } from "framer-motion";
import {
    FlaskConical,
    Play,
    CheckCircle2,
    XCircle,
    Timer,
    ChevronRight,
    PlusCircle
} from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

const experiments = [
    {
        id: 1,
        title: "Backend Series A Test",
        company: "Scale AI",
        hypothesis: "If I apply to Backend roles, then my Python confidence will be validated at 0.8+.",
        status: "Active",
        started: "2025-12-23",
        type: "Verification"
    },
    {
        id: 2,
        title: "Fintech Growth Leap",
        company: "Stripe",
        hypothesis: "If I pass the technical screen, then my React expertise matches high-frequency trading latency needs.",
        status: "Completed",
        outcome: "Failed",
        reason: "Lacked deep understanding of Concurrent React rendering patterns.",
        started: "2025-12-15",
        type: "Learning"
    },
    {
        id: 3,
        title: "Sass Startup Pivot",
        company: "Loom",
        hypothesis: "If I contribute to the core dashboard, then I'll learn TypeScript generics in depth.",
        status: "Proposed",
        started: "-",
        type: "Discovery"
    },
];

export default function Experiments() {
    return (
        <div className="space-y-10">
            <header className="flex items-center justify-between">
                <div className="space-y-1">
                    <h2 className="text-3xl font-bold flex items-center gap-2">
                        <FlaskConical className="w-8 h-8 text-primary" />
                        Experimentation Log
                    </h2>
                    <p className="text-muted-foreground italic">Every application is just another data point in the career experiment.</p>
                </div>
                <button className="px-6 py-3 bg-white/5 border border-white/10 hover:bg-white/10 rounded-2xl transition-colors font-bold">
                    Archive
                </button>
            </header>

            <div className="space-y-6">
                {experiments.map((exp, index) => (
                    <Link href={`/experiments/${exp.id}`} key={exp.id} className="block group">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="glass rounded-3xl p-8 relative overflow-hidden transition-all hover:scale-[1.01] hover:shadow-2xl hover:shadow-primary/5 hover:border-primary/20"
                        >
                            {/* Status light */}
                            <div className={cn(
                                "absolute top-0 right-0 w-1.5 h-full",
                                exp.status === "Active" ? "bg-primary" :
                                    exp.status === "Completed" ? (exp.outcome === "Failed" ? "bg-learning" : "bg-verifying") :
                                        "bg-muted"
                            )} />

                            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                                <div className="lg:col-span-3 space-y-4">
                                    <div className="flex items-center gap-4">
                                        <div className={cn(
                                            "px-3 py-1 rounded-full text-[10px] uppercase font-black italic tracking-widest border",
                                            exp.type === "Verification" ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                                                exp.type === "Learning" ? "bg-orange-500/10 text-orange-400 border-orange-500/20" :
                                                    "bg-purple-500/10 text-purple-400 border-purple-500/20"
                                        )}>
                                            {exp.type}
                                        </div>
                                        <h3 className="text-2xl font-bold uppercase tracking-tight">{exp.title}</h3>
                                        <span className="text-muted-foreground font-mono">@ {exp.company}</span>
                                    </div>

                                    <div className="p-4 rounded-xl bg-white/5 border border-white/5 border-l-4 border-l-primary/30">
                                        <p className="text-sm font-bold uppercase text-primary/70 tracking-tighter italic">Hypothesis:</p>
                                        <p className="mt-1 text-lg font-medium leading-tight">&ldquo;{exp.hypothesis}&rdquo;</p>
                                    </div>

                                    {exp.status === "Completed" && (
                                        <div className="space-y-2">
                                            <div className="flex items-center gap-2">
                                                <XCircle className="w-5 h-5 text-learning" />
                                                <span className="font-bold text-learning">Learning Detected:</span>
                                            </div>
                                            <p className="text-muted-foreground italic pl-7">{exp.reason}</p>
                                        </div>
                                    )}
                                </div>

                                <div className="flex flex-col justify-between border-l border-white/5 pl-8">
                                    <div className="space-y-4">
                                        <div className="space-y-1">
                                            <span className="text-[10px] uppercase font-bold text-muted-foreground">Experiment Status</span>
                                            <div className="flex items-center gap-2 font-bold uppercase">
                                                {exp.status === "Active" ? <Timer className="w-4 h-4 text-primary animate-pulse" /> :
                                                    exp.status === "Completed" ? <CheckCircle2 className="w-4 h-4 text-verifying" /> :
                                                        <Play className="w-4 h-4 text-muted-foreground" />}
                                                {exp.status}
                                            </div>
                                        </div>
                                        <div className="space-y-1">
                                            <span className="text-[10px] uppercase font-bold text-muted-foreground">Started On</span>
                                            <div className="font-mono text-sm">{exp.started}</div>
                                        </div>
                                    </div>

                                    <div className="mt-6 flex items-center justify-between gap-2 px-4 py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all group-hover:border-primary/30">
                                        <span className="font-bold">View Experiment</span>
                                        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </Link>
                ))}

                <motion.button
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                    className="w-full py-8 border-2 border-dashed border-white/10 rounded-3xl text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all flex flex-col items-center gap-2 group"
                >
                    <PlusCircle className="w-8 h-8 group-hover:text-primary transition-colors" />
                    <span className="font-bold uppercase tracking-widest text-xs">Initialize New Experiment</span>
                </motion.button>
            </div>
        </div>
    );
}
