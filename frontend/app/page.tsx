"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { FlaskConical, Atom, ArrowRight, UserPlus } from "lucide-react";
import { useState } from "react";

export default function LandingPage() {
  const [hoveredZone, setHoveredZone] = useState<"left" | "right" | null>(null);

  return (
    <div className="flex h-[calc(100vh-theme(spacing.8))] w-full gap-4 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 bg-background z-0" />

      {/* Left Zone: Existing User */}
      <Link href="/login" className="contents">
        <motion.div
          onHoverStart={() => setHoveredZone("left")}
          onHoverEnd={() => setHoveredZone(null)}
          animate={{
            flex: hoveredZone === "left" ? 2 : hoveredZone === "right" ? 1 : 1.5,
            opacity: hoveredZone === "right" ? 0.6 : 1
          }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
          className="relative z-10 glass rounded-3xl cursor-pointer flex flex-col items-center justify-center border border-white/5 hover:border-primary/50 group overflow-hidden"
        >
          {/* Decorative Loader Rings */}
          <div className="absolute inset-0 flex items-center justify-center opacity-10 group-hover:opacity-20 transition-opacity">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-[400px] h-[400px] border border-dashed border-primary rounded-full"
            />
            <motion.div
              animate={{ rotate: -360 }}
              transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
              className="absolute w-[300px] h-[300px] border border-dotted border-primary rounded-full"
            />
          </div>

          <div className="relative z-20 text-center space-y-4 p-8">
            <motion.div
              animate={{ scale: hoveredZone === "left" ? 1.1 : 1 }}
              className="w-20 h-20 bg-primary/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md"
            >
              <FlaskConical className="w-10 h-10 text-primary" />
            </motion.div>
            <h2 className="text-4xl font-bold tracking-tight">Return to Lab</h2>
            <p className="text-muted-foreground text-lg max-w-sm">
              Continue your experiments. Your failure passport awaits update.
            </p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: hoveredZone === "left" ? 1 : 0, y: hoveredZone === "left" ? 0 : 10 }}
              className="flex items-center gap-2 text-primary font-bold mt-4"
            >
              Access Dashboard <ArrowRight className="w-5 h-5" />
            </motion.div>
          </div>
        </motion.div>
      </Link>

      {/* Right Zone: New User */}
      <Link href="/signup" className="contents">
        <motion.div
          onHoverStart={() => setHoveredZone("right")}
          onHoverEnd={() => setHoveredZone(null)}
          animate={{
            flex: hoveredZone === "right" ? 2 : hoveredZone === "left" ? 1 : 1.5,
            opacity: hoveredZone === "left" ? 0.6 : 1
          }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
          className="relative z-10 glass rounded-3xl cursor-pointer flex flex-col items-center justify-center border border-white/5 hover:border-accent/50 group overflow-hidden"
        >
          {/* Decorative Grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:40px_40px] opacity-20 group-hover:opacity-40 transition-opacity" />

          <div className="relative z-20 text-center space-y-4 p-8">
            <motion.div
              animate={{ scale: hoveredZone === "right" ? 1.1 : 1 }}
              className="w-20 h-20 bg-accent/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md"
            >
              <Atom className="w-10 h-10 text-accent" />
            </motion.div>
            <h2 className="text-4xl font-bold tracking-tight">New Protocol</h2>
            <p className="text-muted-foreground text-lg max-w-sm">
              Initialize a new research subject. Begin your journey of discovery.
            </p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: hoveredZone === "right" ? 1 : 0, y: hoveredZone === "right" ? 0 : 10 }}
              className="flex items-center gap-2 text-accent font-bold mt-4"
            >
              Initialize Subject <UserPlus className="w-5 h-5" />
            </motion.div>
          </div>
        </motion.div>
      </Link>
    </div>
  );
}
