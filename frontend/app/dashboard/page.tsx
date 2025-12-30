"use client";

import { motion } from "framer-motion";
import {
    FlaskConical,
    TrendingUp,
    CheckCircle2,
    AlertCircle,
    Play,
    CheckSquare
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { StatCard } from "@/components/ui/StatCard";
import { Guidebot } from "@/components/dashboard/Guidebot";
import { CompletionModal } from "@/components/dashboard/CompletionModal";
import { ActiveExperimentView } from "@/components/dashboard/ActiveExperimentView";
import { api } from "@/lib/api";

const stats = [
    { name: "Active Experiments", value: "0", icon: FlaskConical, color: "text-blue-400" },
    { name: "Avg. Confidence", value: "0%", icon: TrendingUp, color: "text-verifying" },
    { name: "Lessons Learned", value: "0", icon: CheckCircle2, color: "text-purple-400" },
    { name: "Open Hypotheses", value: "0", icon: AlertCircle, color: "text-amber-400" },
];

export default function Dashboard() {
    const { data: session, status } = useAuth();
    const router = useRouter();
    const loading = status === "loading";
    const user = session?.user;

    const [realStats, setRealStats] = useState(stats);
    const [experiments, setExperiments] = useState<any[]>([]);
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [pageLoading, setPageLoading] = useState(true);

    // Modal State
    const [selectedExpForCompletion, setSelectedExpForCompletion] = useState<any>(null);

    // Derived State for "Focus Mode"
    const activeExperiment = experiments.find(e => e.status === 'active' || e.status === 'applying');

    const fetchData = async () => {
        try {
            const [exps, hyps] = await Promise.all([
                api.get("/api/experiments").then(res => res.json()),
                api.get("/api/hypotheses").then(res => res.json())
            ]);

            const expsArray = Array.isArray(exps) ? exps : [];
            const hypsArray = Array.isArray(hyps) ? hyps : [];

            setExperiments(expsArray);
            setSuggestions(hypsArray);

            const updatedStats = [...stats];
            updatedStats[0].value = expsArray.filter((e: any) => e.status === 'active' || e.status === 'applying').length.toString();
            updatedStats[2].value = expsArray.filter((e: any) => e.status === 'completed').length.toString();
            updatedStats[3].value = hypsArray.length.toString();
            setRealStats(updatedStats);

        } catch (err) {
            console.error("Failed to fetch dashboard data", err);
            toast.error("Failed to load lab data.");
        } finally {
            setPageLoading(false);
        }
    };

    useEffect(() => {
        if (status === "unauthenticated") {
            router.push("/");
        }
        if (session) {
            fetchData();
        }
    }, [status, router, session]);

    const handleStartExperiment = async (suggestion: any) => {
        toast.promise(
            api.post("/api/experiments", suggestion),
            {
                loading: 'Initializing experiment protocols...',
                success: (data) => {
                    fetchData();
                    return 'Experiment Active. Focus Mode Engaged.';
                },
                error: 'Failed to start experiment'
            }
        );
    };

    const handleCompleteExperiment = async (result: string, feedback: string) => {
        const expId = selectedExpForCompletion?.id || activeExperiment?.id;
        if (!expId) return;

        await api.post(`/api/experiments/${expId}/outcome`, {
            result,
            feedback
        });

        toast.success("Reflection recorded. Updating Belief State...");
        setSelectedExpForCompletion(null); // Close modal
        fetchData(); // Refresh everything
    };

    const handleAbandonExperiment = async () => {
        // Could impl api call to cancel, for now just UI switch by refreshing or setting state
        // Ideally should update status to 'abandoned'
        toast.info("Returning to Planning Mode...");
        fetchData();
    };

    if (loading || pageLoading || !user) return (
        <div className="flex h-[50vh] items-center justify-center text-muted-foreground flex-col gap-4">
            <div className="relative w-16 h-16">
                <div className="absolute inset-0 border-4 border-white/10 rounded-full" />
                <div className="absolute inset-0 border-4 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
            <p className="animate-pulse">Accessing Lab Database...</p>
        </div>
    );

    return (
        <div className="space-y-10 pb-20">
            {/* Header only shows in Planning Mode or simplified in Focus Mode */}
            {!activeExperiment && (
                <header>
                    <motion.h2
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-3xl font-bold"
                    >
                        Welcome Back, {user.name || "Researcher"}
                    </motion.h2>
                    <p className="text-muted-foreground mt-1 text-lg">
                        Check your <span className="text-foreground font-medium italic underline decoration-primary/50">Failure Passport</span> to see how your beliefs are evolving.
                    </p>
                </header>
            )}

            {/* Stats Grid - Always visible but maybe smaller in focus mode? Keeping same for now */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {realStats.map((stat, index) => (
                    <StatCard key={stat.name} {...stat} index={index} />
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">

                {/* Left Column: Two Modes Switch */}
                <div className="lg:col-span-2 space-y-8">

                    {activeExperiment ? (
                        // MODE 2: Constrained Development Mode (Focus Checklists)
                        <ActiveExperimentView
                            experiment={activeExperiment}
                            requestCompletion={() => setSelectedExpForCompletion(activeExperiment)}
                            onAbandon={handleAbandonExperiment}
                            onComplete={handleCompleteExperiment}
                        />
                    ) : (
                        // MODE 1: Planning Mode (Suggestions + History)
                        <>
                            {/* Main Timeline Card */}
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.4 }}
                                className="glass rounded-3xl p-8 space-y-6"
                            >
                                <div className="flex items-center justify-between">
                                    <h3 className="text-xl font-semibold flex items-center gap-2">
                                        <FlaskConical className="w-5 h-5 text-primary" />
                                        Experiment History
                                    </h3>
                                </div>

                                <div className="space-y-4">
                                    {experiments.length > 0 ? (
                                        experiments.slice(0, 5).map((exp: any) => (
                                            <div key={exp.id} className="p-5 rounded-2xl bg-white/5 border border-white/5 flex flex-col md:flex-row md:items-center justify-between hover:bg-white/10 transition-colors gap-4">
                                                <div className="space-y-1">
                                                    <div className="flex items-center gap-2">
                                                        <h4 className="font-semibold text-lg">{exp.title}</h4>
                                                        {exp.company && <span className="text-xs px-2 py-0.5 rounded bg-white/10 text-muted-foreground">{exp.company}</span>}
                                                    </div>
                                                    <p className="text-sm text-muted-foreground italic">&ldquo;{exp.hypothesis}&rdquo;</p>
                                                </div>

                                                <div className="flex items-center gap-4 self-end md:self-auto">
                                                    <div className={cn(
                                                        "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-tight",
                                                        exp.status === "completed" ? "bg-green-500/20 text-green-400 border border-green-500/20" :
                                                            "bg-muted text-muted-foreground border border-muted"
                                                    )}>
                                                        {exp.status}
                                                    </div>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="p-8 text-center text-muted-foreground border border-dashed border-white/10 rounded-2xl">
                                            No history yet. Start your first experiment below!
                                        </div>
                                    )}
                                </div>
                            </motion.div>

                            {/* Suggestions Stack */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-semibold text-muted-foreground uppercase tracking-wider pl-1">Lab Suggestions</h3>
                                {suggestions.length > 0 ? (
                                    suggestions.map((sugg: any, idx) => (
                                        <motion.div
                                            key={sugg.id}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: 0.5 + (idx * 0.1) }}
                                            className="glass rounded-3xl p-8 bg-gradient-to-br from-primary/5 to-accent/5 border border-primary/20 space-y-6"
                                        >
                                            <div className="flex items-start justify-between">
                                                <div>
                                                    <h3 className="text-xl font-semibold text-primary">Hypothesis #{idx + 1}</h3>
                                                    <p className="text-muted-foreground leading-relaxed mt-2">
                                                        <span className="text-foreground font-bold italic">{sugg.belief}</span> belief needs verification.
                                                    </p>
                                                </div>
                                                {sugg.risk === 'Low' && <span className="px-2 py-1 rounded bg-green-500/20 text-green-400 text-xs font-bold">Safe Bet</span>}
                                            </div>

                                            <div className="p-4 rounded-2xl bg-white/10 border border-white/10">
                                                <p className="text-sm font-medium opacity-70">Experiment:</p>
                                                <p className="mt-1 font-bold text-lg">{sugg.statement}</p>
                                                <p className="mt-2 text-xs text-muted-foreground">{sugg.reasoning}</p>
                                            </div>
                                            <button
                                                onClick={() => handleStartExperiment(sugg)}
                                                className="w-full py-4 bg-primary text-white rounded-2xl font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform flex items-center justify-center gap-2 group"
                                            >
                                                Start Experiment
                                                <Play className="w-5 h-5 fill-current group-hover:translate-x-1 transition-transform" />
                                            </button>
                                        </motion.div>
                                    ))
                                ) : (
                                    <div className="glass rounded-3xl p-8 text-center text-muted-foreground">
                                        All hypotheses cleared. You are a career master (or the API is down).
                                    </div>
                                )}
                            </div>
                        </>
                    )}
                </div>

                {/* Right Column: Guidebot (Always visible) */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                    className="lg:col-span-1 sticky top-8"
                >
                    <Guidebot />
                </motion.div>

            </div>

            {/* Outcome Modal */}
            {selectedExpForCompletion && (
                <CompletionModal
                    isOpen={!!selectedExpForCompletion}
                    onClose={() => setSelectedExpForCompletion(null)}
                    experimentTitle={selectedExpForCompletion.title}
                    onComplete={handleCompleteExperiment}
                />
            )}
        </div>
    );
}
