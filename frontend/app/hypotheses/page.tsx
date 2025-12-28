"use client";

import { useAuth } from "@/context/AuthContext";
import { Lightbulb, ThumbsUp, HelpCircle, AlertTriangle, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Hypothesis = {
    id: number;
    statement: string;
    risk: string;
    belief: string;
    reasoning: string;
    status: 'active' | 'proposed';
};

export default function HypothesesPage() {
    const { data: session } = useAuth();
    const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (session) {
            api.get("/api/hypotheses")
                .then(async (res) => {
                    if (res.ok) {
                        const data = await res.json();
                        setHypotheses(data);
                    }
                })
                .finally(() => setLoading(false));
        }
    }, [session]);

    if (loading) return (
        <div className="flex h-[50vh] items-center justify-center text-muted-foreground">
            <Loader2 className="w-8 h-8 animate-spin" />
        </div>
    );

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-3">
                        <Lightbulb className="w-8 h-8 text-amber-400" />
                        Active Hypotheses
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Scientific predictions about your career market fit.
                    </p>
                </div>
            </div>

            <div className="space-y-4">
                {hypotheses.map((hyp) => (
                    <motion.div
                        key={hyp.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass p-6 rounded-3xl border border-white/5 space-y-4 relative overflow-hidden group hover:border-white/10"
                    >
                        {/* Status Stripe */}
                        <div className={cn(
                            "absolute left-0 top-0 bottom-0 w-1",
                            hyp.status === 'active' ? "bg-amber-400" : "bg-white/10"
                        )} />

                        <div className="flex justify-between items-start pl-4">
                            <div className="space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className={cn(
                                        "text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md",
                                        {
                                            "bg-green-500/20 text-green-400": hyp.risk === "Low",
                                            "bg-amber-500/20 text-amber-400": hyp.risk === "Medium",
                                            "bg-red-500/20 text-red-400": hyp.risk === "High",
                                        }
                                    )}>
                                        {hyp.risk} Risk
                                    </span>
                                    {hyp.status === 'active' && (
                                        <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md bg-blue-500/20 text-blue-400 animate-pulse">
                                            Testing Now
                                        </span>
                                    )}
                                </div>
                                <h3 className="text-lg font-medium leading-relaxed">
                                    &ldquo;{hyp.statement}&rdquo;
                                </h3>
                            </div>

                            {hyp.status === 'proposed' && (
                                <div className="flex gap-2">
                                    <button className="p-2 rounded-full hover:bg-white/10 text-muted-foreground hover:text-white transition-colors" title="Why this?">
                                        <HelpCircle className="w-5 h-5" />
                                    </button>
                                    <button className="p-2 rounded-full hover:bg-green-500/20 text-muted-foreground hover:text-green-400 transition-colors" title="Approve">
                                        <ThumbsUp className="w-5 h-5" />
                                    </button>
                                </div>
                            )}
                        </div>

                        <div className="pl-4 flex items-center gap-6 text-sm text-muted-foreground">
                            <div className="flex items-center gap-2">
                                <AlertTriangle className="w-4 h-4" />
                                <span>Testing: <span className="text-foreground font-medium">{hyp.belief}</span></span>
                            </div>
                            <div className="hidden md:block w-1 h-1 rounded-full bg-white/20" />
                            <div className="hidden md:block italic opacity-70">
                                Reasoning: {hyp.reasoning}
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}
