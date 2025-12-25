"use client";

import { motion } from "framer-motion";
import { cn, formatConfidence, getConfidenceBg, getConfidenceColor } from "@/lib/utils";
import { History, Info } from "lucide-react";
import { ConfidenceBar } from "@/components/ui/ConfidenceBar";

interface BeliefCardProps {
    name: string;
    category: string;
    confidence: number;
    basis: string;
    experience: number;
    index: number;
}

export function BeliefCard({ name, category, confidence, basis, experience, index }: BeliefCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            className="glass p-6 rounded-3xl glass-hover space-y-4 group overflow-hidden relative"
        >
            <div className="flex justify-between items-start">
                <div className="space-y-1">
                    <div className="flex items-center gap-2">
                        <h4 className="text-xl font-bold">{name}</h4>
                        <span className="text-[10px] uppercase tracking-widest px-2 py-0.5 rounded-full bg-white/5 border border-white/5 text-muted-foreground">
                            {category}
                        </span>
                    </div>
                    <p className="text-sm text-muted-foreground font-mono">{experience} years exp</p>
                </div>
                <button className="p-2 rounded-lg hover:bg-white/5 text-muted-foreground hover:text-foreground transition-colors">
                    <History className="w-4 h-4" />
                </button>
            </div>

            <div className="space-y-2">
                <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground font-medium italic">Confidence</span>
                    <span className={cn("font-bold", getConfidenceColor(confidence))}>
                        {formatConfidence(confidence)}
                    </span>
                </div>
                <ConfidenceBar value={confidence} index={index} />
            </div>

            <div className="pt-4 border-t border-white/5">
                <div className="flex items-start gap-2">
                    <Info className="w-4 h-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-muted-foreground italic leading-tight">
                        &ldquo;{basis}&rdquo;
                    </p>
                </div>
            </div>

            {/* Decorative background number */}
            <div className="absolute -bottom-6 -right-6 text-8xl font-black text-white/[0.02] select-none pointer-events-none group-hover:text-primary/[0.02] transition-colors">
                {index + 1}
            </div>
        </motion.div>
    );
}
