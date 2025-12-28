
"use client";

import { useOnboardingStore } from "@/lib/store/onboarding";
import { Check, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";

const ROLES = ["Software Engineer", "Data Scientist", "Product Manager", "Designer", "DevRel"];
const TYPES = [
    { id: "internship", label: "Internship" },
    { id: "fulltime", label: "Full-time" },
    { id: "both", label: "Open to Both" },
];

export function StepClarification() {
    const { preferences, updatePreferences, setStep } = useOnboardingStore();

    const handleGenerate = async () => {
        setStep('reveal');
        try {
            await api.post("/api/onboarding/clarify", preferences);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
            {/* ... Input Fields ... */}
            <div className="text-center space-y-2">
                <h2 className="text-2xl font-bold">Calibration</h2>
                <p className="text-muted-foreground">Calibrating experiment parameters.</p>
            </div>

            <div className="space-y-6">
                {/* Role Selection */}
                <div className="space-y-3">
                    <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Target Role</label>
                    <div className="flex flex-wrap gap-2">
                        {ROLES.map((role) => (
                            <button
                                key={role}
                                onClick={() => updatePreferences({ role })}
                                className={cn(
                                    "px-4 py-2 rounded-full text-sm font-medium border transition-all",
                                    preferences.role === role
                                        ? "bg-primary text-primary-foreground border-primary"
                                        : "bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20"
                                )}
                            >
                                {role}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Type Selection */}
                <div className="space-y-3">
                    <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Experiment Type</label>
                    <div className="grid grid-cols-3 gap-2">
                        {TYPES.map((type) => (
                            <button
                                key={type.id}
                                // @ts-ignore
                                onClick={() => updatePreferences({ type: type.id })}
                                className={cn(
                                    "py-3 rounded-xl text-sm font-medium border transition-all",
                                    preferences.type === type.id
                                        ? "bg-primary/20 text-primary border-primary/50"
                                        : "bg-white/5 border-white/10 hover:bg-white/10"
                                )}
                            >
                                {type.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Location */}
                <div className="space-y-2">
                    <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Location Constraints</label>
                    <input
                        type="text"
                        value={preferences.location}
                        onChange={(e) => updatePreferences({ location: e.target.value })}
                        className="w-full bg-black/20 border border-white/10 rounded-xl py-3 px-4 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all"
                        placeholder="e.g. Remote, San Francisco, London"
                    />
                </div>

                {/* Hackathon Toggle */}
                <div
                    onClick={() => updatePreferences({ hackathons: !preferences.hackathons })}
                    className={cn(
                        "flex items-center gap-3 p-4 rounded-xl border cursor-pointer transition-all",
                        preferences.hackathons
                            ? "bg-purple-500/10 border-purple-500/50"
                            : "bg-white/5 border-white/10"
                    )}
                >
                    <div className={cn(
                        "w-6 h-6 rounded-full border flex items-center justify-center transition-colors",
                        preferences.hackathons ? "bg-purple-500 border-purple-500" : "border-white/20"
                    )}>
                        {preferences.hackathons && <Check className="w-4 h-4 text-white" />}
                    </div>
                    <span className="font-medium text-sm">Include Hackathons as valid experiments?</span>
                </div>
            </div>

            <button
                onClick={handleGenerate}
                className="w-full py-4 bg-primary text-primary-foreground rounded-xl font-bold shadow-lg shadow-primary/20 hover:bg-primary/90 transition-all active:scale-[0.98] flex items-center justify-center gap-2"
            >
                Generate Passport <ArrowRight className="w-5 h-5" />
            </button>
        </div>
    );
}
