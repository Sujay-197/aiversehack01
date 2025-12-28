
"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ConfidenceBarProps {
    confidence: number; // 0 to 1
    className?: string;
    showLabel?: boolean;
}

export function ConfidenceBar({ confidence, className, showLabel = true }: ConfidenceBarProps) {
    const percentage = Math.round(confidence * 100);

    let colorClass = "bg-primary";
    if (confidence >= 0.7) colorClass = "bg-verifying";
    else if (confidence >= 0.4) colorClass = "bg-testing";
    else colorClass = "bg-learning";

    return (
        <div className={cn("w-full space-y-1", className)}>
            {showLabel && (
                <div className="flex justify-between text-xs uppercase font-bold tracking-wider text-muted-foreground">
                    <span>Confidence</span>
                    <span>{percentage}%</span>
                </div>
            )}
            <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className={cn("h-full rounded-full", colorClass)}
                />
            </div>
        </div>
    );
}
