"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
    name: string;
    value: string;
    icon: LucideIcon;
    color?: string;
    index?: number;
}

export function StatCard({ name, value, icon: Icon, color, index = 0 }: StatCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            className="glass p-6 rounded-2xl glass-hover relative overflow-hidden group"
        >
            <div className="flex items-center justify-between relative z-10">
                <span className="text-muted-foreground font-semibold text-sm uppercase tracking-wider">{name}</span>
                <div className={cn("p-2 rounded-xl bg-white/5 group-hover:bg-primary/10 transition-colors", color)}>
                    <Icon className="w-5 h-5" />
                </div>
            </div>
            <div className="mt-4 text-4xl font-black tracking-tighter relative z-10 italic">
                {value}
            </div>

            {/* Background decoration */}
            <div className="absolute -bottom-2 -right-2 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity">
                <Icon className="w-24 h-24 rotate-12" />
            </div>
        </motion.div>
    );
}
