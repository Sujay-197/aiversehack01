"use client";

import { usePathname } from "next/navigation";
import { Sidebar } from "@/components/layout/Sidebar";
import { AuthProvider } from "@/context/AuthContext";
import { Guidebot } from "@/components/layout/Guidebot";

export function ClientLayout({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();
    const isAuthPage = pathname === "/" || pathname === "/login" || pathname === "/signup";

    return (
        <AuthProvider>
            {!isAuthPage && <Sidebar />}
            <main className={`flex-1 overflow-y-auto ${!isAuthPage ? "p-8" : ""} relative`}>
                <div className={!isAuthPage ? "max-w-7xl mx-auto" : "h-full"}>
                    {children}
                </div>
                {!isAuthPage && <Guidebot />}

                {/* Subtle background glow - Only show on dashboard/inner pages */}
                {!isAuthPage && (
                    <>
                        <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-primary/5 blur-[120px] rounded-full pointer-events-none -mr-48 -mt-48" />
                        <div className="fixed bottom-0 left-0 w-[400px] h-[400px] bg-accent/5 blur-[100px] rounded-full pointer-events-none -ml-32 -mb-32" />
                    </>
                )}
            </main>
        </AuthProvider>
    );
}
