"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    LayoutDashboard,
    UserCircle,
    FlaskConical,
    Lightbulb,
    Settings,
    Menu
} from "lucide-react";
import { useState } from "react";

const navItems = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Failure Passport", href: "/passport", icon: UserCircle },
    { name: "Experiments", href: "/experiments", icon: FlaskConical },
    { name: "Insights Log", href: "/insights", icon: Lightbulb },
];

export function Sidebar() {
    const pathname = usePathname();
    const [isOpen, setIsOpen] = useState(true);

    return (
        <aside className={cn(
            "h-screen glass border-r border-white/10 transition-all duration-300 z-10 sticky top-0",
            isOpen ? "w-64" : "w-20"
        )}>
            <div className="p-6 flex items-center justify-between">
                {isOpen && (
                    <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent italic">
                        Career Scientist
                    </h1>
                )}
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                >
                    <Menu className="w-5 h-5" />
                </button>
            </div>

            <nav className="mt-6 px-4 space-y-2">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-4 px-3 py-3 rounded-xl transition-all group",
                                isActive
                                    ? "bg-primary/20 text-primary border border-primary/20 shadow-lg shadow-primary/10"
                                    : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
                            )}
                        >
                            <item.icon className={cn(
                                "w-5 h-5 transition-transform group-hover:scale-110",
                                isActive ? "text-primary" : "text-muted-foreground"
                            )} />
                            {isOpen && <span className="font-medium">{item.name}</span>}
                        </Link>
                    );
                })}
            </nav>

            <div className="absolute bottom-6 left-4 right-4">
                <button className={cn(
                    "flex items-center gap-4 px-3 py-3 w-full rounded-xl text-muted-foreground hover:bg-white/5 hover:text-foreground transition-all group"
                )}>
                    <Settings className="w-5 h-5 group-hover:rotate-45 transition-transform" />
                    {isOpen && <span className="font-medium">Settings</span>}
                </button>
            </div>
        </aside>
    );
}
