
"use client";

import { ConfidenceBar } from "@/components/passport/ConfidenceBar";
import { GitCommit, FileText, TrendingUp, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";

interface BeliefCardProps {
    skill: string;
    confidence: number;
    evidence: { type: 'github' | 'resume' | 'manual'; count: number }[];
    status: 'learning' | 'testing' | 'verifying';
    trend?: number; // +5 or -2 etc
}

export function BeliefCard({ skill, confidence, evidence, status, trend }: BeliefCardProps) {
    return (
        <motion.div
            whileHover={{ y: -4 }}
            className="glass p-6 rounded-3xl border border-white/5 space-y-4 hover:border-white/10 transition-all"
        >
            <div className="flex justify-between items-start">
                <h3 className="text-xl font-bold">{skill}</h3>
                {trend && (
                    <div className={`text-xs font-bold px-2 py-1 rounded-full ${trend > 0 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                        {trend > 0 ? '+' : ''}{trend}%
                    </div>
                )}
            </div>

            <ConfidenceBar confidence={confidence} />

            <div className="pt-2 flex gap-2">
                {evidence.map((ev, i) => (
                    <div key={i} className="flex items-center gap-1 text-[10px] uppercase font-bold text-muted-foreground bg-white/5 px-2 py-1 rounded-lg">
                        {ev.type === 'github' && <GitCommit className="w-3 h-3" />}
                        {ev.type === 'resume' && <FileText className="w-3 h-3" />}
                        <span>{ev.count} {ev.type}</span>
                    </div>
                ))}
            </div>

            <div className="pt-2 text-xs text-muted-foreground italic">
                Status: <span className="text-white font-medium uppercase">{status}</span>
            </div>
        </motion.div>
    );
}
