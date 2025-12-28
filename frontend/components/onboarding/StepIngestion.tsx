
"use client";

import { useOnboardingStore } from "@/lib/store/onboarding";
import { Upload, Github, FileText, Linkedin } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export function StepIngestion() {
    const {
        resumeFile, setResume,
        githubUrl, setGithubUrl,
        linkedInEnabled, toggleLinkedIn,
        setStep
    } = useOnboardingStore();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setResume(e.target.files[0]);
        }
    };

    const handleProceed = async () => {
        // Prepare upload
        const formData = new FormData();
        if (resumeFile) formData.append("file", resumeFile);
        if (githubUrl) formData.append("github_url", githubUrl);
        if (linkedInEnabled) formData.append("linkedin", "true");

        setStep('clarification'); // Move to next step immediately for UX (optimistic)

        try {
            // In real app, call API here. 
            // For now we just move next.
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center space-y-2">
                <h2 className="text-2xl font-bold">Evidence Gathering</h2>
                <p className="text-muted-foreground">We’re collecting evidence, not judging you.</p>
            </div>

            <div className="space-y-6">
                {/* Resume Upload */}
                <div className="p-6 rounded-2xl border border-dashed border-white/20 bg-white/5 hover:bg-white/10 transition-colors text-center cursor-pointer relative group">
                    <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />
                    <div className="flex flex-col items-center gap-3 py-4">
                        <div className={cn(
                            "w-12 h-12 rounded-full flex items-center justify-center transition-colors",
                            resumeFile ? "bg-green-500/20 text-green-400" : "bg-white/10 text-white"
                        )}>
                            {resumeFile ? <FileText className="w-6 h-6" /> : <Upload className="w-6 h-6" />}
                        </div>
                        <div className="space-y-1">
                            <p className="font-medium text-lg">
                                {resumeFile ? resumeFile.name : "Upload Resume (PDF)"}
                            </p>
                            <p className="text-xs text-muted-foreground">Drag & drop or click to browse</p>
                        </div>
                    </div>
                </div>

                {/* GitHub URL */}
                <div className="space-y-2">
                    <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">GitHub Profile</label>
                    <div className="relative">
                        <Github className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                        <input
                            type="text"
                            value={githubUrl}
                            onChange={(e) => setGithubUrl(e.target.value)}
                            className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-10 pr-4 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all"
                            placeholder="https://github.com/username"
                        />
                    </div>
                </div>

                {/* LinkedIn Toggle (Optional) */}
                <div
                    onClick={toggleLinkedIn}
                    className={cn(
                        "flex items-center justify-between p-4 rounded-xl border cursor-pointer transition-all",
                        linkedInEnabled
                            ? "bg-blue-500/10 border-blue-500/50"
                            : "bg-white/5 border-white/10 hover:border-white/20"
                    )}
                >
                    <div className="flex items-center gap-3">
                        <div className={cn(
                            "w-8 h-8 rounded-lg flex items-center justify-center",
                            linkedInEnabled ? "bg-blue-500 text-white" : "bg-white/10 text-muted-foreground"
                        )}>
                            <Linkedin className="w-5 h-5" />
                        </div>
                        <div className="text-sm font-medium">Include LinkedIn Evidence</div>
                    </div>
                    <div className={cn(
                        "w-10 h-6 rounded-full relative transition-colors",
                        linkedInEnabled ? "bg-blue-500" : "bg-white/20"
                    )}>
                        <div className={cn(
                            "absolute top-1 left-1 w-4 h-4 rounded-full bg-white transition-transform",
                            linkedInEnabled ? "translate-x-4" : "translate-x-0"
                        )} />
                    </div>
                </div>
            </div>

            <button
                onClick={handleProceed}
                disabled={!resumeFile && !githubUrl}
                className="w-full py-4 bg-primary text-primary-foreground rounded-xl font-bold shadow-lg shadow-primary/20 hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
            >
                Proceed to Synthesis
            </button>
        </div>
    );
}
