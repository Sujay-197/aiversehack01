"use client";

import { useAuth } from "@/context/AuthContext";
import { Lightbulb, ArrowRight, TrendingDown, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Insight = {
    id: number;
    date: string;
    trigger: string;
    delta: number;
    belief: string;
    insight: string;
};

export default function InsightsPage() {
    const { data: session } = useAuth();
    const [insights, setInsights] = useState<Insight[]>([]);

    useEffect(() => {
        if (session) {
            api.get("/api/insights").then(async (res) => {
                if (res.ok) {
                    const data = await res.json();
                    setInsights(data);
                }
            });
        }
    }, [session]);

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-3">
                        <Lightbulb className="w-8 h-8 text-purple-400" />
                        Insights Log
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        The learning journal of the "Scientist".
                    </p>
                </div>
            </div>

            <div className="space-y-8 relative before:absolute before:left-8 before:top-4 before:bottom-0 before:w-0.5 before:bg-white/10">
                {insights.map((insight) => (
                    <motion.div
                        key={insight.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="pl-20 relative"
                    >
                        {/* Timeline Dot */}
                        <div className="absolute left-6 top-6 w-5 h-5 rounded-full bg-[#0F172A] border-4 border-purple-500/50 shadow-[0_0_10px_rgba(168,85,247,0.5)] z-10" />

                        <div className="glass p-6 rounded-3xl border border-white/5 space-y-4">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-muted-foreground font-mono">{insight.date}</span>
                                <span className="font-bold text-accent uppercase tracking-wider text-xs bg-accent/10 px-2 py-1 rounded-md">
                                    Trigger: {insight.trigger}
                                </span>
                            </div>

                            <div className="flex gap-6 items-center">
                                <div className={`flex flex-col items-center justify-center w-16 h-16 rounded-2xl border ${insight.delta > 0
                                    ? "bg-green-500/10 border-green-500/30 text-green-400"
                                    : "bg-red-500/10 border-red-500/30 text-red-400"
                                    }`}>
                                    {insight.delta > 0 ? <TrendingUp className="w-6 h-6" /> : <TrendingDown className="w-6 h-6" />}
                                    <span className="font-bold text-lg">{insight.delta > 0 ? '+' : ''}{insight.delta}%</span>
                                </div>

                                <div className="space-y-1">
                                    <div className="text-sm text-muted-foreground uppercase font-bold tracking-wider">
                                        Belief Update: <span className="text-white">{insight.belief}</span>
                                    </div>
                                    <p className="text-lg leading-relaxed">
                                        "{insight.insight}"
                                    </p>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
