"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { FlaskConical } from "lucide-react";

export function GlobalLoader() {
    const pathname = usePathname();
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        // Trigger loading on route change
        setIsLoading(true);
        const timer = setTimeout(() => setIsLoading(false), 800); // Artificial delay for smooth effect
        return () => clearTimeout(timer);
    }, [pathname]);

    return (
        <AnimatePresence mode="wait">
            {isLoading && (
                <motion.div
                    key="loader"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-xl"
                >
                    <div className="flex flex-col items-center gap-4">
                        <motion.div
                            animate={{
                                rotate: [0, 45, -45, 0],
                                scale: [1, 1.1, 1.1, 1]
                            }}
                            transition={{
                                duration: 2,
                                ease: "easeInOut",
                                repeat: Infinity
                            }}
                            className="relative"
                        >
                            <FlaskConical className="w-12 h-12 text-primary" />
                            <motion.div
                                className="absolute inset-0 bg-primary/20 blur-xl rounded-full"
                                animate={{ scale: [1, 1.5, 1] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                            />
                        </motion.div>

                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: 100 }}
                            className="h-1 bg-white/10 rounded-full overflow-hidden w-24"
                        >
                            <motion.div
                                className="h-full bg-primary"
                                animate={{ x: [-100, 100] }}
                                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            />
                        </motion.div>

                        <p className="text-xs font-mono text-muted-foreground uppercase tracking-widest animate-pulse">
                            Calibrating Instruments...
                        </p>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
