"use client";

import { motion } from "framer-motion";
import { BeliefCard } from "@/components/passport/BeliefCard";
import {
    Users,
    Search,
    Filter,
    PlusCircle,
    Info,
    ShieldAlert
} from "lucide-react";
import { useState } from "react";
import { SkillModal } from "@/components/passport/SkillModal";

const mockBeliefs = [
    { name: "Python", category: "Language", confidence: 0.85, basis: "Built complex agents, handled 15+ library integrations", experience: 4.5 },
    { name: "React", category: "Framework", confidence: 0.52, basis: "Moderate dashboard experience, pending testing on complex state", experience: 2.0 },
    { name: "PostgreSQL", category: "Database", confidence: 0.68, basis: "Designed 5+ schemas, but limited experience with scaling/sharding", experience: 3.0 },
    { name: "Node.js", category: "Runtime", confidence: 0.28, basis: "Only handled simple express servers, prone to async bugs", experience: 1.0 },
    { name: "System Design", category: "Theory", confidence: 0.15, basis: "Understands basics, but no production experience with large scale", experience: 0.5 },
    { name: "TypeScript", category: "Language", confidence: 0.45, basis: "Uses basic types, struggles with complex generics", experience: 1.5 },
];

export default function Passport() {
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedSkill, setSelectedSkill] = useState<typeof mockBeliefs[0] | null>(null);

    const filteredBeliefs = mockBeliefs.filter(b =>
        b.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-10">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div className="space-y-2">
                    <motion.h2
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-4xl font-black italic tracking-tight"
                    >
                        THE FAILURE PASSPORT
                    </motion.h2>
                    <div className="flex items-center gap-2 text-muted-foreground p-2 rounded-lg bg-orange-500/10 border border-orange-500/20 max-w-fit">
                        <ShieldAlert className="w-4 h-4 text-orange-400" />
                        <span className="text-xs font-bold uppercase tracking-widest text-orange-400 uppercase">Warning: Scientist at Work</span>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <input
                            type="text"
                            placeholder="Search beliefs..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-primary/50 outline-none w-64 transition-all"
                        />
                    </div>
                    <button className="p-2 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
                        <Filter className="w-5 h-5" />
                    </button>
                    <button className="flex items-center gap-2 px-6 py-2 bg-primary text-white font-bold rounded-xl hover:scale-105 transition-transform">
                        <PlusCircle className="w-5 h-5" /> Add Belief
                    </button>
                </div>
            </header>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-20">
                {filteredBeliefs.map((belief, index) => (
                    <div key={belief.name} onClick={() => setSelectedSkill(belief)} className="cursor-pointer">
                        <BeliefCard
                            {...belief}
                            index={index}
                        />
                    </div>
                ))}

                {filteredBeliefs.length === 0 && (
                    <div className="col-span-full py-20 text-center glass rounded-3xl space-y-4">
                        <Info className="w-12 h-12 text-muted-foreground mx-auto" />
                        <p className="text-xl text-muted-foreground italic">&ldquo;No existing records found for this attribute.&rdquo;</p>
                    </div>
                )}
            </div>

            <footer className="fixed bottom-0 left-64 right-0 p-6 bg-gradient-to-t from-background to-transparent pointer-events-none">
                <div className="max-w-7xl mx-auto flex justify-center">
                    <div className="glass px-8 py-4 rounded-full border-primary/20 pointer-events-auto shadow-2xl shadow-primary/20 flex items-center gap-8">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-learning" />
                            <span className="text-xs font-bold text-muted-foreground uppercase">Learning</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-testing" />
                            <span className="text-xs font-bold text-muted-foreground uppercase">Testing</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-verifying" />
                            <span className="text-xs font-bold text-muted-foreground uppercase">Verifying</span>
                        </div>
                    </div>
                </div>
            </footer>

            <SkillModal
                isOpen={!!selectedSkill}
                onClose={() => setSelectedSkill(null)}
                skill={selectedSkill}
            />
        </div>
    );
}
