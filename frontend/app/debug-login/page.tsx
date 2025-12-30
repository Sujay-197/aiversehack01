"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { FlaskConical, Bug } from "lucide-react";

export default function DebugLoginPage() {
    const [email, setEmail] = useState("debug@test.com");
    const [loading, setLoading] = useState(false);

    const handleDebugLogin = async () => {
        setLoading(true);
        await signIn("credentials", {
            email: email,
            callbackUrl: "/dashboard"
        });
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-black text-white p-4">
            <div className="max-w-md w-full space-y-8 p-8 glass rounded-3xl border border-dashed border-yellow-500/30">
                <div className="text-center space-y-2">
                    <div className="mx-auto w-16 h-16 bg-yellow-500/10 rounded-2xl flex items-center justify-center border border-yellow-500/20">
                        <Bug className="w-8 h-8 text-yellow-500" />
                    </div>
                    <h1 className="text-2xl font-bold text-yellow-500">Debug Access</h1>
                    <p className="text-muted-foreground text-sm">
                        Bypassing GitHub OAuth for testing purposes.
                        <br />
                        <span className="text-xs opacity-50">Only use this in development/testing.</span>
                    </p>
                </div>

                <div className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-xs uppercase tracking-wider text-muted-foreground ml-1">Mock Email</label>
                        <input
                            type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-yellow-500/50 transition-all"
                        />
                    </div>

                    <button
                        onClick={handleDebugLogin}
                        disabled={loading}
                        className="w-full py-4 bg-yellow-500 text-black font-bold rounded-xl hover:bg-yellow-400 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                        {loading ? "Authenticating..." : "Enter Lab (Debug Mode)"}
                    </button>

                    <div className="pt-4 border-t border-white/5 text-center">
                        <a href="/" className="text-sm text-muted-foreground hover:text-white transition-colors">
                            ← Return to Main Entrance
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}
