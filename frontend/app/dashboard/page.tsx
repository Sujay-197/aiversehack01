"use client";

import { motion } from "framer-motion";
import {
    FlaskConical,
    TrendingUp,
    AlertCircle,
    CheckCircle2,
    ArrowRight
} from "lucide-react";
import { cn, formatConfidence } from "@/lib/utils";
import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

import { StatCard } from "@/components/ui/StatCard";

const stats = [
    { name: "Active Experiments", value: "3", icon: FlaskConical, color: "text-blue-400" },
    { name: "Avg. Confidence", value: "62%", icon: TrendingUp, color: "text-verifying" },
    { name: "Lessons Learned", value: "12", icon: CheckCircle2, color: "text-purple-400" },
    { name: "Open Hypotheses", value: "5", icon: AlertCircle, color: "text-amber-400" },
];

const recentExperiments = [
    { id: 1, title: "Backend Series A Test", hypothesis: "Python fit for Series A", status: "Active", confidence: 0.65 },
    { id: 2, title: "Fintech Growth Leap", hypothesis: "React expertise matches Fintech", status: "Completed", outcome: "Failed", confidence: 0.42 },
    { id: 3, title: "DevRel Exploration", hypothesis: "Communication skills test", status: "Proposed", confidence: 0.20 },
];

export default function Dashboard() {
    const { user, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && !user) {
            router.push("/login");
        }
    }, [user, loading, router]);

    if (loading || !user) return null;

    return (
        <div className="space-y-10">
            <header>
                <motion.h2
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-3xl font-bold"
                >
                    Welcome Back, {user.full_name || "Researcher"}
                </motion.h2>
                <p className="text-muted-foreground mt-1 text-lg">
                    Your current <span className="text-foreground font-medium italic underline decoration-primary/50">Failure Passport</span> is 12% more refined this week.
                </p>
            </header>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <StatCard key={stat.name} {...stat} index={index} />
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Timeline Card */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 }}
                    className="lg:col-span-2 glass rounded-3xl p-8 space-y-6"
                >
                    <div className="flex items-center justify-between">
                        <h3 className="text-xl font-semibold flex items-center gap-2">
                            <FlaskConical className="w-5 h-5 text-primary" />
                            Recent Experiments
                        </h3>
                        <button className="text-sm text-primary font-medium hover:underline flex items-center gap-1">
                            View all <ArrowRight className="w-4 h-4" />
                        </button>
                    </div>

                    <div className="space-y-4">
                        {recentExperiments.map((exp) => (
                            <div key={exp.id} className="p-5 rounded-2xl bg-white/5 border border-white/5 flex items-center justify-between hover:bg-white/10 transition-colors">
                                <div className="space-y-1">
                                    <h4 className="font-semibold text-lg">{exp.title}</h4>
                                    <p className="text-sm text-muted-foreground italic">&ldquo;{exp.hypothesis}&rdquo;</p>
                                </div>
                                <div className="flex items-center gap-4">
                                    <div className="text-right">
                                        <div className="text-xs text-muted-foreground uppercase font-bold tracking-wider">Confidence</div>
                                        <div className={cn(
                                            "font-mono font-bold text-lg",
                                            exp.confidence > 0.5 ? "text-verifying" : "text-learning"
                                        )}>
                                            {formatConfidence(exp.confidence)}
                                        </div>
                                    </div>
                                    <div className={cn(
                                        "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-tight",
                                        exp.status === "Active" ? "bg-blue-500/20 text-blue-400 border border-blue-500/20" :
                                            exp.status === "Completed" ? "bg-green-500/20 text-green-400 border border-green-500/20" :
                                                "bg-muted text-muted-foreground border border-muted"
                                    )}>
                                        {exp.status}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Next Suggestion */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.5 }}
                    className="glass rounded-3xl p-8 bg-gradient-to-br from-primary/10 to-accent/5 border border-primary/20 space-y-6"
                >
                    <h3 className="text-xl font-semibold text-primary">Lab Suggestion</h3>
                    <p className="text-muted-foreground leading-relaxed">
                        Confidence in <span className="text-foreground font-bold italic">React Performance</span> is below testing threshold (0.3).
                    </p>
                    <div className="p-4 rounded-2xl bg-white/10 border border-white/10">
                        <p className="text-sm font-medium">Proposed Experiment:</p>
                        <p className="mt-1 font-bold">Build a high-throughput visualization dashboard using Framer Motion.</p>
                    </div>
                    <button className="w-full py-4 bg-primary text-white rounded-2xl font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform flex items-center justify-center gap-2">
                        Start Experiment <FlaskConical className="w-5 h-5" />
                    </button>
                </motion.div>
            </div>
        </div>
    );
}
