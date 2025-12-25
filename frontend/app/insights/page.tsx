"use client";

import { motion } from "framer-motion";
import { Lightbulb, Calendar, ArrowRightLeft, MessageSquareQuote } from "lucide-react";

const reflections = [
    {
        id: 1,
        date: "2025-12-24",
        title: "Resume Keyword Mismatch",
        attribute: "Python Proficiency",
        change: "0.85 → 0.72",
        insight: "Confidence dropped after 5 ghostings at Series A startups. Hypothesis: Resume lacks 'Asyncio' and 'FastAPI' specific metrics.",
    },
    {
        id: 2,
        date: "2025-12-20",
        title: "The Fintech Gap",
        attribute: "React Expertise",
        change: "0.42 → 0.25",
        insight: "Failed technical screen at Stripe. Realized that 'knowing React' != 'understanding high-concurrency state management'.",
    },
];

export default function Insights() {
    return (
        <div className="space-y-10">
            <header className="space-y-2">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Lightbulb className="w-8 h-8 text-amber-400" />
                    Insights Log
                </h2>
                <p className="text-muted-foreground italic">The scientific record of your career evolution.</p>
            </header>

            <div className="relative border-l border-white/10 ml-4 pl-10 space-y-12 pb-20">
                {reflections.map((ref, index) => (
                    <motion.div
                        key={ref.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="relative"
                    >
                        {/* Timeline dot */}
                        <div className="absolute -left-[50px] top-1 w-5 h-5 rounded-full bg-background border-4 border-amber-400" />

                        <div className="glass rounded-3xl p-8 space-y-6">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <span className="text-xs font-bold text-muted-foreground uppercase flex items-center gap-1">
                                        <Calendar className="w-3 h-3" /> {ref.date}
                                    </span>
                                    <h3 className="text-2xl font-bold italic tracking-tight">{ref.title}</h3>
                                </div>
                                <div className="px-4 py-2 rounded-xl bg-amber-400/10 border border-amber-400/20 text-amber-400 font-bold flex items-center gap-2">
                                    <ArrowRightLeft className="w-4 h-4" /> {ref.change}
                                </div>
                            </div>

                            <div className="p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4">
                                <div className="flex items-center gap-2 text-primary font-bold uppercase text-[10px] tracking-widest">
                                    <MessageSquareQuote className="w-4 h-4" /> Reflection Data
                                </div>
                                <p className="text-lg text-foreground italic leading-relaxed">
                                    &ldquo;{ref.insight}&rdquo;
                                </p>
                            </div>

                            <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground">Impacted Attribute:</span>
                                <span className="px-2 py-0.5 rounded-lg bg-white/5 border border-white/5 text-xs font-mono">{ref.attribute}</span>
                            </div>
                        </div>
                    </motion.div>
                ))}

                <div className="text-center py-10 opacity-50">
                    <p className="text-sm font-mono tracking-tighter">-- END OF CURRENT RECORD --</p>
                </div>
            </div>
        </div>
    );
}
