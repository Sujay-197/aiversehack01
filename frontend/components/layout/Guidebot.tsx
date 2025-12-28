
"use client";

import { useAuth } from "@/context/AuthContext";
import { useState } from "react";
import { MessageSquare, X, Send, Bot } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function Guidebot() {
    const { data: session } = useAuth();
    const user = session?.user;
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([
        { role: 'bot', text: "I've analyzed your Passport. Try asking: 'Is my Python strong enough for Series A startups?'" }
    ]);
    const [input, setInput] = useState("");

    if (!user) return null;

    const handleSend = () => {
        if (!input.trim()) return;
        setMessages(prev => [...prev, { role: 'user', text: input }]);
        // Mock response for now
        setTimeout(() => {
            setMessages(prev => [...prev, {
                role: 'bot',
                text: `Based on your Passport (Python Confidence: 0.72), you are strong enough technically. However, we have 0 evidence of System Design skills in your GitHub. I recommend running an experiment to build a microservice.`
            }]);
        }, 1000);
        setInput("");
    };

    return (
        <div className="fixed bottom-8 right-8 z-50">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                        className="absolute bottom-16 right-0 w-80 md:w-96 h-[500px] glass rounded-3xl border border-white/10 flex flex-col shadow-2xl overflow-hidden"
                    >
                        {/* Header */}
                        <div className="p-4 border-b border-white/5 bg-white/5 flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <Bot className="w-5 h-5 text-primary" />
                                <span className="font-bold">Protocol Guide</span>
                            </div>
                            <button onClick={() => setIsOpen(false)} className="text-muted-foreground hover:text-white">
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4">
                            {messages.map((msg, i) => (
                                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                                        ? 'bg-primary text-white rounded-br-sm'
                                        : 'bg-white/10 text-slate-200 rounded-bl-sm'
                                        }`}>
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Input */}
                        <div className="p-4 border-t border-white/5 bg-white/5">
                            <div className="relative">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                    placeholder="Ask grounded in your belief state..."
                                    className="w-full bg-black/20 border border-white/10 rounded-xl py-3 pl-4 pr-10 focus:outline-none focus:border-primary/50 text-sm"
                                />
                                <button
                                    onClick={handleSend}
                                    className="absolute right-2 top-2 p-1.5 bg-primary rounded-lg text-white hover:bg-primary/90 transition-colors"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-14 h-14 rounded-full bg-primary text-white shadow-lg shadow-primary/30 hover:scale-110 active:scale-95 transition-all flex items-center justify-center"
            >
                <div className="relative">
                    <MessageSquare className="w-6 h-6" />
                    <div className="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#0F172A]" />
                </div>
            </button>
        </div>
    );
}
