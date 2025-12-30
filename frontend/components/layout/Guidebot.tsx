
"use client";

import { useAuth } from "@/context/AuthContext";
import { useState } from "react";
import { MessageSquare, X, Send, Bot } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import { api } from "@/lib/api";

export function Guidebot() {
    const { data: session } = useAuth();
    const user = session?.user;
    const [isOpen, setIsOpen] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [messages, setMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([
        { role: 'bot', text: "I've analyzed your Passport. Try asking: 'Is my Python strong enough for Series A startups?'" }
    ]);
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);

    if (!user) return null;

    const handleSend = async () => {
        if (!input.trim() || isTyping) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setInput("");
        setIsTyping(true);

        try {
            const res = await api.post("/api/guidebot/chat", { message: userMsg });
            if (res.ok) {
                const data = await res.json();
                setMessages(prev => [...prev, { role: 'bot', text: data.reply }]);
            } else {
                setMessages(prev => [...prev, { role: 'bot', text: "Protocol link interrupted. Please try again." }]);
            }
        } catch (e) {
            console.error(e);
            setMessages(prev => [...prev, { role: 'bot', text: "Connection to Brain lost." }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="fixed bottom-8 right-8 z-50">
            <AnimatePresence>
                {!isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.9 }}
                        className="w-80 h-20 glass rounded-2xl border border-white/10 flex items-center shadow-2xl cursor-pointer"
                        onClick={() => { setIsOpen(true); setIsExpanded(false); }}
                    >
                        <div className="flex items-center gap-3 px-6 py-4 w-full">
                            <Bot className="w-6 h-6 text-primary" />
                            <span className="font-bold text-lg">Protocol Guide</span>
                            <span className="ml-auto text-muted-foreground text-sm">Chat with your agent</span>
                        </div>
                    </motion.div>
                )}
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: isExpanded ? 1 : 0.98 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className={isExpanded ? "fixed inset-0 z-50 bg-black/80 flex items-center justify-center" : "absolute bottom-16 right-0 w-80 md:w-96 h-[500px] glass rounded-3xl border border-white/10 flex flex-col shadow-2xl overflow-hidden"}
                    >
                        <div className={isExpanded ? "w-full max-w-2xl h-[80vh] bg-[#18181b] rounded-3xl flex flex-col overflow-hidden" : "flex flex-col h-full"}>
                            {/* Header */}
                            <div className="p-4 border-b border-white/5 bg-white/5 flex justify-between items-center">
                                <div className="flex items-center gap-2">
                                    <Bot className="w-5 h-5 text-primary" />
                                    <span className="font-bold">Protocol Guide</span>
                                </div>
                                <div className="flex gap-2">
                                    <button onClick={() => setIsExpanded(!isExpanded)} className="text-muted-foreground hover:text-white">
                                        {isExpanded ? <X className="w-4 h-4" /> : <MessageSquare className="w-4 h-4" />}
                                    </button>
                                    <button onClick={() => { setIsOpen(false); setIsExpanded(false); }} className="text-muted-foreground hover:text-white">
                                        <X className="w-4 h-4" />
                                    </button>
                                </div>
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
                                {isTyping && (
                                    <div className="flex justify-start">
                                        <div className="bg-white/10 p-3 rounded-2xl rounded-bl-sm flex gap-1 items-center">
                                            <div className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce" />
                                            <div className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce [animation-delay:0.2s]" />
                                            <div className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce [animation-delay:0.4s]" />
                                        </div>
                                    </div>
                                )}
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
                                        onFocus={() => setIsExpanded(true)}
                                    />
                                    <button
                                        onClick={handleSend}
                                        className="absolute right-2 top-2 p-1.5 bg-primary rounded-lg text-white hover:bg-primary/90 transition-colors"
                                    >
                                        <Send className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
