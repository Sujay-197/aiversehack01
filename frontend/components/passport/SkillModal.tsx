"use client";

import { Modal } from "@/components/ui/Modal";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { FlaskConical, History, FileText } from "lucide-react";

interface SkillModalProps {
    isOpen: boolean;
    onClose: () => void;
    skill: {
        name: string;
        category: string;
        confidence: number;
        basis: string;
        experience: number;
    } | null;
}

const mockHistory = [
    { date: "Dec 1", value: 0.2 },
    { date: "Dec 5", value: 0.25 },
    { date: "Dec 10", value: 0.45 },
    { date: "Dec 15", value: 0.42 },
    { date: "Dec 20", value: 0.60 },
    { date: "Today", value: 0.68 },
];

export function SkillModal({ isOpen, onClose, skill }: SkillModalProps) {
    if (!skill) return null;

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={`Analysis: ${skill.name}`}>
            <div className="space-y-8">

                {/* Confidence Graph */}
                <div className="space-y-2">
                    <h4 className="text-sm font-bold uppercase tracking-widest text-muted-foreground flex items-center gap-2">
                        <History className="w-4 h-4" /> Confidence Trajectory
                    </h4>
                    <div className="h-64 w-full bg-white/5 rounded-2xl p-4 border border-white/5">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={mockHistory}>
                                <defs>
                                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis hide domain={[0, 1]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                                    itemStyle={{ color: '#f1f5f9' }}
                                    formatter={(value: any) => [`${(value || 0) * 100}%`, "Confidence"]}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="value"
                                    stroke="#3b82f6"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorValue)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Evidence Chain */}
                <div className="space-y-4">
                    <h4 className="text-sm font-bold uppercase tracking-widest text-muted-foreground flex items-center gap-2">
                        <FileText className="w-4 h-4" /> Supporting Evidence
                    </h4>
                    <div className="space-y-3">
                        <div className="p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer border border-white/5 flex items-start gap-3">
                            <FlaskConical className="w-5 h-5 text-learning mt-1" />
                            <div>
                                <p className="font-bold text-sm">Failed React Experiment</p>
                                <p className="text-xs text-muted-foreground mt-1">"Demonstrated lack of deep effect knowledge."</p>
                            </div>
                            <span className="ml-auto text-xs font-mono text-learning">-15%</span>
                        </div>
                        <div className="p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer border border-white/5 flex items-start gap-3">
                            <FileText className="w-5 h-5 text-verifying mt-1" />
                            <div>
                                <p className="font-bold text-sm">Resume Analysis v3</p>
                                <p className="text-xs text-muted-foreground mt-1">"Strong keyword density for 'Hooks' and 'Context'."</p>
                            </div>
                            <span className="ml-auto text-xs font-mono text-verifying">+20%</span>
                        </div>
                    </div>
                </div>

            </div>
        </Modal>
    );
}
