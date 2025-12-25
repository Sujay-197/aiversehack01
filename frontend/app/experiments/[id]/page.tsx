"use client";

import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import {
    ArrowLeft,
    FlaskConical,
    Calendar,
    CheckCircle2,
    XCircle,
    Timer,
    GitCommit,
    FileText,
    MessageSquare,
    ExternalLink
} from "lucide-react";
import { cn, formatConfidence } from "@/lib/utils";
import Link from "next/link";
import { ConfidenceBar } from "@/components/ui/ConfidenceBar";

interface TimelineEvent {
    stage: string;
    date: string;
    status: string;
}

interface Evidence {
    type: string;
    name: string;
    impact: string;
}

interface Experiment {
    title: string;
    company: string;
    hypothesis: string;
    status: string;
    started: string;
    type: string;
    timeline: TimelineEvent[];
    evidence: Evidence[];
    outcome?: string;
    reason?: string;
}

// Mock data store - normally fetched via API
const experimentData: Record<number, Experiment> = {
    1: {
        title: "Backend Series A Test",
        company: "Scale AI",
        hypothesis: "If I apply to Backend roles, then my Python confidence will be validated at 0.8+.",
        status: "Active",
        started: "2025-12-23",
        type: "Verification",
        timeline: [
            { stage: "Hypothesis Formed", date: "Dec 23", status: "done" },
            { stage: "Resume Tailored", date: "Dec 23", status: "done" },
            { stage: "Application Sent", date: "Dec 24", status: "done" },
            { stage: "Screening Call", date: "Pending", status: "current" },
            { stage: "Technical Interview", date: "-", status: "upcoming" },
            { stage: "Offer/Reject", date: "-", status: "upcoming" }
        ],
        evidence: [
            { type: "Resume", name: "Backend_Engineer_v2.pdf", impact: "High" },
            { type: "Github", name: "ai-agent-framework", impact: "Medium" }
        ]
    },
    2: {
        title: "Fintech Growth Leap",
        company: "Stripe",
        hypothesis: "If I pass the technical screen, then my React expertise matches high-frequency trading latency needs.",
        status: "Completed",
        outcome: "Failed",
        reason: "Lacked deep understanding of Concurrent React rendering patterns.",
        started: "2025-12-15",
        type: "Learning",
        timeline: [
            { stage: "Hypothesis Formed", date: "Dec 15", status: "done" },
            { stage: "Application Sent", date: "Dec 16", status: "done" },
            { stage: "Screening Call", date: "Dec 18", status: "done" },
            { stage: "Technical Interview", date: "Dec 20", status: "failed" },
        ],
        evidence: [
            { type: "Resume", name: "FullStack_Lead.pdf", impact: "High" }
        ]
    }
};

export default function ExperimentDetail() {
    const params = useParams();
    const id = Number(params.id);
    const data = experimentData[id as keyof typeof experimentData];

    if (!data) return <div className="p-10 text-center">Experiment not found</div>;

    return (
        <div className="space-y-8 pb-20">
            <Link href="/experiments" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <ArrowLeft className="w-4 h-4" /> Back to Log
            </Link>

            {/* Header */}
            <div className="glass p-8 rounded-[40px] space-y-6 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                    <FlaskConical className="w-64 h-64 rotate-12" />
                </div>

                <div className="relative z-10 space-y-4">
                    <div className="flex items-start justify-between">
                        <div className="space-y-1">
                            <h1 className="text-4xl font-black italic tracking-wide uppercase">{data.title}</h1>
                            <p className="text-xl text-muted-foreground font-mono">@ {data.company}</p>
                        </div>
                        <div className={cn(
                            "px-4 py-2 rounded-xl font-bold uppercase tracking-widest border",
                            data.status === "Active" ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                                data.status === "Completed" ? (data.outcome === "Success" ? "bg-verifying/10 text-verifying border-verifying/20" : "bg-learning/10 text-learning border-learning/20") :
                                    "bg-muted text-muted-foreground"
                        )}>
                            {data.status === "Completed" ? data.outcome : data.status}
                        </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-white/5 border border-white/5 backdrop-blur-md max-w-2xl">
                        <p className="text-xs font-bold uppercase text-muted-foreground mb-2 flex items-center gap-2">
                            <FlaskConical className="w-3 h-3" /> Scientific Hypothesis
                        </p>
                        <p className="text-lg font-medium italic leading-relaxed">"{data.hypothesis}"</p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Timeline Column */}
                <div className="lg:col-span-2 glass rounded-3xl p-8 space-y-8">
                    <h3 className="text-xl font-bold flex items-center gap-2">
                        <Calendar className="w-5 h-5 text-primary" /> Progress Timeline
                    </h3>

                    <div className="relative border-l-2 border-white/10 ml-3 space-y-8 pl-8 py-2">
                        {data.timeline.map((event, index) => (
                            <div key={index} className="relative">
                                <div className={cn(
                                    "absolute -left-[41px] top-1 w-6 h-6 rounded-full border-4 transition-colors bg-background",
                                    event.status === "done" ? "border-verifying" :
                                        event.status === "current" ? "border-primary animate-pulse" :
                                            event.status === "failed" ? "border-learning" :
                                                "border-white/10"
                                )} />
                                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                                    <div>
                                        <p className={cn(
                                            "font-bold text-lg",
                                            event.status === "upcoming" && "text-muted-foreground"
                                        )}>{event.stage}</p>
                                        {event.status === "failed" && (
                                            <p className="text-sm text-learning font-bold mt-1">Experiment Terminated</p>
                                        )}
                                    </div>
                                    <span className="font-mono text-sm text-muted-foreground bg-white/5 px-2 py-1 rounded-md">
                                        {event.date}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Sidebar Column */}
                <div className="space-y-6">
                    {/* Outcome Box */}
                    {data.status === "Completed" && (
                        <div className={cn(
                            "p-6 rounded-3xl border space-y-4",
                            data.outcome === "Failed" ? "bg-learning/5 border-learning/20" : "bg-verifying/5 border-verifying/20"
                        )}>
                            <div className="flex items-center gap-2 font-bold uppercase tracking-widest text-xs">
                                {data.outcome === "Failed" ? <XCircle className="w-4 h-4 text-learning" /> : <CheckCircle2 className="w-4 h-4 text-verifying" />}
                                <span className={data.outcome === "Failed" ? "text-learning" : "text-verifying"}>
                                    Result Analysis
                                </span>
                            </div>
                            <p className="text-sm font-medium leading-relaxed">
                                {data.reason}
                            </p>
                        </div>
                    )}

                    {/* Evidence List */}
                    <div className="glass rounded-3xl p-6 space-y-4">
                        <h3 className="font-bold flex items-center gap-2 text-sm uppercase tracking-widest text-muted-foreground">
                            <GitCommit className="w-4 h-4" /> Attached Evidence
                        </h3>
                        <div className="space-y-3">
                            {data.evidence.map((item, i) => (
                                <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
                                    <FileText className="w-4 h-4 text-primary" />
                                    <div className="flex-1 overflow-hidden">
                                        <p className="font-bold text-sm truncate">{item.name}</p>
                                        <p className="text-xs text-muted-foreground capitalize">{item.type}</p>
                                    </div>
                                    <span className="text-[10px] uppercase font-bold bg-white/10 px-1.5 py-0.5 rounded">
                                        {item.impact} Imapct
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
