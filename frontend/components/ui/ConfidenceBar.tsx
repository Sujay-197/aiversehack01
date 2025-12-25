"use client";

import { motion } from "framer-motion";
import { cn, getConfidenceBg } from "@/lib/utils";

interface ConfidenceBarProps {
    value: number; // 0.0 to 1.0
    className?: string;
    animate?: boolean;
    index?: number;
}

export function ConfidenceBar({ value, className, animate = true, index = 0 }: ConfidenceBarProps) {
    return (
        <div className={cn("h-3 w-full bg-white/5 rounded-full overflow-hidden border border-white/5 p-[1px]", className)}>
            <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${value * 100}%` }}
                transition={animate ? { duration: 1, ease: "easeOut", delay: index * 0.1 } : { duration: 0 }}
                className={cn("h-full rounded-full transition-all duration-1000", getConfidenceBg(value))}
            />
        </div>
    );
}
