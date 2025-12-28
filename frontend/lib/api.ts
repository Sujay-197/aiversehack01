const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

import { getSession } from "next-auth/react";

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    const session = await getSession();
    const token = session?.user?.email; // For MVP, identifying by email

    const headers = {
        "Content-Type": "application/json",
        ...(token && { "X-User-Email": token }), // Backend will trust this for now
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Handle unauthorized
        // window.location.href = "/login"; // Optional: redirect
    }

    return response;
}

export const api = {
    get: (endpoint: string) => fetchWithAuth(endpoint),
    post: (endpoint: string, body: any) =>
        fetchWithAuth(endpoint, {
            method: "POST",
            body: JSON.stringify(body),
        }),
};
