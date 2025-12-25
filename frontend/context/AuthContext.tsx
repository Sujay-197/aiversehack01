"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

interface User {
    id: string;
    email: string;
    full_name?: string;
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (token: string) => void;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem("token");
            if (token) {
                try {
                    const res = await api.get("/auth/me");
                    if (res.ok) {
                        const userData = await res.json();
                        setUser(userData);
                    } else {
                        localStorage.removeItem("token");
                    }
                } catch (error) {
                    console.error("Auth check failed", error);
                    localStorage.removeItem("token");
                }
            }
            setLoading(false);
        };
        checkAuth();
    }, []);

    const login = async (token: string) => {
        localStorage.setItem("token", token);
        const res = await api.get("/auth/me");
        if (res.ok) {
            const userData = await res.json();
            setUser(userData);
            router.push("/dashboard");
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        router.push("/login");
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
