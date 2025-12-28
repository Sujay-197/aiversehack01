
"use client";

import { useAuth } from "@/context/AuthContext";
import { FlaskConical, ExternalLink, Ghost, XCircle, CheckCircle, Clock } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Experiment = {
    id: number;
    role: string;
    company: string;
    status: string;
    date: string;
    hypothesis_id: number;
};

export default function ExperimentsPage() {
    const { data: session } = useAuth();
    const [experiments, setExperiments] = useState<Experiment[]>([]);

    useEffect(() => {
        if (session) {
            api.get("/api/experiments").then(async (res) => {
                if (res.ok) {
                    const data = await res.json();
                    setExperiments(data);
                }
            });
        }
    }, [session]);

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-3">
                        <FlaskConical className="w-8 h-8 text-blue-400" />
                        Lab Experiments
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Tracking applications and actions as data collection points.
                    </p>
                </div>
            </div>

            <div className="overflow-hidden rounded-3xl border border-white/10 glass">
                <table className="w-full text-left">
                    <thead className="bg-white/5 text-xs uppercase font-bold text-muted-foreground tracking-wider">
                        <tr>
                            <th className="px-6 py-4">Experiment (Role)</th>
                            <th className="px-6 py-4">Company</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Date</th>
                            <th className="px-6 py-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {experiments.map((exp) => (
                            <tr key={exp.id} className="hover:bg-white/5 transition-colors group">
                                <td className="px-6 py-4 font-medium">{exp.role}</td>
                                <td className="px-6 py-4 text-muted-foreground">{exp.company}</td>
                                <td className="px-6 py-4">
                                    <div className={cn(
                                        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide",
                                        {
                                            "bg-white/10 text-slate-400": exp.status === "Ghosted",
                                            "bg-red-500/10 text-red-400": exp.status === "Rejected",
                                            "bg-green-500/10 text-green-400": exp.status === "Accepted",
                                            "bg-blue-500/10 text-blue-400": exp.status === "Pending",
                                        }
                                    )}>
                                        {exp.status === "Ghosted" && <Ghost className="w-3 h-3" />}
                                        {exp.status === "Rejected" && <XCircle className="w-3 h-3" />}
                                        {exp.status === "Accepted" && <CheckCircle className="w-3 h-3" />}
                                        {exp.status === "Pending" && <Clock className="w-3 h-3" />}
                                        {exp.status}
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm text-muted-foreground">{exp.date}</td>
                                <td className="px-6 py-4 text-right">
                                    <button className="p-2 hover:bg-white/10 rounded-lg text-muted-foreground hover:text-white transition-colors">
                                        <ExternalLink className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
