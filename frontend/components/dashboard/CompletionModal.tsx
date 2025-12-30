"use client";

import { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { CheckCircle2, XCircle, Ghost, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface CompletionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onComplete: (result: string, feedback: string) => Promise<void>;
    experimentTitle: string;
}

export function CompletionModal({ isOpen, onClose, onComplete, experimentTitle }: CompletionModalProps) {
    const [result, setResult] = useState<string | null>(null);
    const [feedback, setFeedback] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async () => {
        if (!result) return;
        setSubmitting(true);
        try {
            await onComplete(result, feedback);
            onClose();
        } finally {
            setSubmitting(false);
            setResult(null);
            setFeedback("");
        }
    };

    const options = [
        { id: "Offer", label: "Success / Offer", icon: CheckCircle2, color: "text-green-400", bg: "bg-green-400/10 border-green-400/20" },
        { id: "Rejected", label: "Rejection", icon: XCircle, color: "text-red-400", bg: "bg-red-400/10 border-red-400/20" },
        { id: "Ghosted", label: "No Reply / Ghosted", icon: Ghost, color: "text-gray-400", bg: "bg-white/5 border-white/10" },
        { id: "Iterate", label: "Need More Time", icon: AlertTriangle, color: "text-amber-400", bg: "bg-amber-400/10 border-amber-400/20" },
    ];

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={`Complete Experiment: ${experimentTitle}`}>
            <div className="space-y-6">
                <div>
                    <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground mb-3 block">What happened?</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {options.map((opt) => (
                            <button
                                key={opt.id}
                                onClick={() => setResult(opt.id)}
                                className={cn(
                                    "flex items-center gap-3 p-4 rounded-xl border text-left transition-all",
                                    result === opt.id
                                        ? "ring-2 ring-primary border-transparent bg-white/10"
                                        : "hover:bg-white/5 border-white/10",
                                    opt.color
                                )}
                            >
                                <opt.icon className="w-5 h-5 flex-shrink-0" />
                                <span className={cn("font-medium", opt.id === result ? "text-white" : "")}>{opt.label}</span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Reflection & Feedback</label>
                    <textarea
                        className="w-full bg-black/20 border border-white/10 rounded-xl p-4 min-h-[120px] focus:outline-none focus:ring-1 focus:ring-primary/50 text-sm placeholder:text-muted-foreground/50 resize-none"
                        placeholder="Paste rejection email used, interview notes, or describe what you learned..."
                        value={feedback}
                        onChange={(e) => setFeedback(e.target.value)}
                    />
                </div>

                <div className="flex gap-3 pt-4">
                    <button
                        onClick={onClose}
                        className="flex-1 py-3 rounded-xl border border-white/10 hover:bg-white/5 font-medium transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSubmit}
                        disabled={!result || submitting}
                        className="flex-1 py-3 bg-primary text-primary-foreground rounded-xl font-bold shadow-lg shadow-primary/20 hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        {submitting ? "Updating Beliefs..." : "Confirm Outcome"}
                    </button>
                </div>
            </div>
        </Modal>
    );
}
