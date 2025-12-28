"use client";

import { useAuth } from "@/context/AuthContext";
import { BeliefCard } from "@/components/passport/BeliefCard";
import { Shield, BrainCircuit, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { motion } from "framer-motion";

type Belief = {
    skill: string;
    confidence: number;
    status: 'learning' | 'testing' | 'verifying';
    evidence: { type: 'github' | 'resume' | 'manual'; count: number }[];
    trend?: number;
};

export default function PassportPage() {
    const { data: session } = useAuth();
    const user = session?.user;
    const [beliefs, setBeliefs] = useState<Belief[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (session) {
            api.get("/api/passport")
                .then(async (res) => {
                    if (res.ok) {
                        const data = await res.json();
                        setBeliefs(data.beliefs || []);
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
                        <Shield className="w-8 h-8 text-verifying" />
                        Career Passport
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Current probabilistic belief state of <span className="text-white font-medium">{user?.name || "Researcher"}</span>.
                    </p>
                </div>
                <div className="hidden md:flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/10">
                    <BrainCircuit className="w-4 h-4 text-accent" />
                    <span className="text-xs font-mono text-muted-foreground">VERSION: v0.4.2 (BETA)</span>
                </div>
            </div>

            {beliefs.length === 0 ? (
                <div className="p-12 text-center border border-dashed border-white/10 rounded-3xl">
                    <p className="text-muted-foreground">No beliefs established yet. Complete onboarding or add items manually.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {beliefs.map((belief) => (
                        <BeliefCard key={belief.skill} {...belief} />
                    ))}
                </div>
            )}

            <div className="p-4 rounded-xl border border-dashed border-white/20 text-center text-sm text-muted-foreground hover:bg-white/5 transition-colors cursor-pointer">
                + Add manual evidence source
            </div>
        </div>
    );
}
