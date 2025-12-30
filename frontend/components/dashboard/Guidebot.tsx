"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Sparkles, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface Message {
    role: "user" | "assistant";
    content: string;
    id: number;
}

export function Guidebot() {
    const [messages, setMessages] = useState<Message[]>([
        { id: 0, role: "assistant", content: "Hello! I'm your Career Guidebot. I have access to your belief state and experiment results. How can I help you strategize today?" }
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg: Message = { role: "user", content: input, id: Date.now() };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setIsLoading(true);

        try {
            const res = await api.post("/guidebot/chat", { message: userMsg.content });
            if (!res.ok) throw new Error("Failed to correct guidebot");

            const data = await res.json();
            setMessages(prev => [...prev, { role: "assistant", content: data.reply, id: Date.now() + 1 }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: "assistant", content: "I'm having trouble connecting to the lab database. Please try again.", id: Date.now() + 1 }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="glass flex flex-col h-[600px] rounded-3xl border border-white/10 overflow-hidden relative">
            <div className="p-4 border-b border-white/10 bg-white/5 backdrop-blur-md flex items-center gap-3 relative z-10">
                <div className="bg-primary/20 p-2 rounded-xl text-primary border border-primary/20 shadow-[0_0_15px_-3px_var(--color-primary)]">
                    <Bot size={24} />
                </div>
                <div>
                    <h3 className="font-bold text-lg flex items-center gap-2">
                        Career Guidebot
                        <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                    </h3>
                    <p className="text-xs text-muted-foreground">Powered by your Evidence & Belief State</p>
                </div>
            </div>

            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent"
            >
                {messages.map((msg) => (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        key={msg.id}
                        className={cn(
                            "flex gap-4 max-w-[90%]",
                            msg.role === "user" ? "ml-auto flex-row-reverse" : ""
                        )}
                    >
                        <div className={cn(
                            "h-8 w-8 rounded-full flex items-center justify-center shrink-0 border",
                            msg.role === "assistant"
                                ? "bg-primary/10 text-primary border-primary/20"
                                : "bg-muted text-muted-foreground border-white/10"
                        )}>
                            {msg.role === "assistant" ? <Bot size={16} /> : <User size={16} />}
                        </div>

                        <div className={cn(
                            "p-4 rounded-2xl text-sm leading-relaxed shadow-sm",
                            msg.role === "assistant"
                                ? "bg-white/5 border border-white/5 text-foreground rounded-tl-none"
                                : "bg-primary text-primary-foreground rounded-tr-none"
                        )}>
                            {msg.content.split('\n').map((line, i) => (
                                <p key={i} className="mb-1 last:mb-0">{line}</p>
                            ))}
                        </div>
                    </motion.div>
                ))}

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex gap-4 max-w-[80%]"
                    >
                        <div className="h-8 w-8 rounded-full bg-primary/10 text-primary border border-primary/20 flex items-center justify-center shrink-0">
                            <Sparkles size={16} className="animate-spin" />
                        </div>
                        <div className="bg-white/5 border border-white/5 text-muted-foreground p-4 rounded-2xl rounded-tl-none text-sm flex items-center gap-2">
                            Thinking...
                        </div>
                    </motion.div>
                )}
            </div>

            <div className="p-4 bg-white/5 border-t border-white/10 mt-auto">
                <form
                    onSubmit={(e) => { e.preventDefault(); handleSend(); }}
                    className="relative flex items-center gap-2"
                >
                    <input
                        className="flex-1 bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all placeholder:text-muted-foreground/50"
                        placeholder="Ask about your next career move..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="bg-primary hover:bg-primary/90 text-primary-foreground p-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-primary/20"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
}
