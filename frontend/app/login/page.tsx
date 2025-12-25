"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { FlaskConical, Lock, Mail } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Setup form data for OAuth2
            const formData = new URLSearchParams();
            formData.append('username', email); // OAuth2 expects username
            formData.append('password', password);

            const res = await fetch("http://localhost:8000/auth/token", {
                method: "POST",
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (!res.ok) throw new Error("Invalid credentials");

            const data = await res.json();
            await login(data.access_token);
            toast.success("Access Granted. Welcome back.");
        } catch (error) {
            toast.error("Access Denied. Please check your credentials.");
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
                    <div className="w-16 h-16 bg-primary/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md">
                        <FlaskConical className="w-8 h-8 text-primary" />
                    </div>
                    <h1 className="text-2xl font-bold">Researcher Access</h1>
                    <p className="text-muted-foreground text-sm mt-2">Enter your credentials to access the lab.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">Email</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-black/20 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all text-sm"
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
                                className="w-full bg-black/20 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all text-sm"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary hover:bg-primary/90 text-white font-bold py-3 rounded-xl shadow-lg shadow-primary/20 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed mt-4"
                    >
                        {loading ? "Authenticating..." : "Authenticate"}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-muted-foreground">
                    New to the protocol?{" "}
                    <Link href="/signup" className="text-primary hover:underline font-medium">
                        Initialize ID
                    </Link>
                </div>
            </motion.div>
        </div>
    );
}
