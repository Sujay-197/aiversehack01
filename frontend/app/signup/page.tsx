"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Atom, Lock, Mail, User } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

export default function SignupPage() {
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const res = await api.post("/auth/register", {
                email,
                password,
                full_name: fullName
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Registration failed");
            }

            toast.success("Identity Initialized. Please login.");
            router.push("/login");
        } catch (error: any) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-[80vh]">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="w-full max-w-md glass p-8 rounded-3xl border border-white/10"
            >
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-accent/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md">
                        <Atom className="w-8 h-8 text-accent" />
                    </div>
                    <h1 className="text-2xl font-bold">Initialize Identity</h1>
                    <p className="text-muted-foreground text-sm mt-2">Create a new subject profile for experimentation.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Full Name</label>
                        <div className="relative">
                            <User className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                className="w-full bg-black/20 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-all text-sm"
                                placeholder="Dr. Jane Doe"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Email</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-black/20 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-all text-sm"
                                placeholder="researcher@lab.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Password</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-black/20 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-all text-sm"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-accent hover:bg-accent/90 text-white font-bold py-3 rounded-xl shadow-lg shadow-accent/20 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed mt-4"
                    >
                        {loading ? "Initializing..." : "Create Identity"}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-muted-foreground">
                    Already have an identity?{" "}
                    <Link href="/login" className="text-accent hover:underline font-medium">
                        Access Lab
                    </Link>
                </div>
            </motion.div>
        </div>
    );
}
