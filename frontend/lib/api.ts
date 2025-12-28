const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

import { getSession } from "next-auth/react";

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    const session = await getSession();
    const token = session?.user?.email;

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(token && { "X-User-Email": token }),
        ...(options.headers as Record<string, string>),
    };

    // If Content-Type is explicitly set to empty string, remove it (for FormData)
    if (headers["Content-Type"] === "") {
        delete headers["Content-Type"];
    }

    return fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });
}

export const api = {
    get: (endpoint: string) => fetchWithAuth(endpoint),
    post: (endpoint: string, body: any) =>
        fetchWithAuth(endpoint, {
            method: "POST",
            body: JSON.stringify(body),
        }),
    postFormData: (endpoint: string, body: FormData) =>
        fetchWithAuth(endpoint, {
            method: "POST",
            body: body,
            headers: {
                // Remove default Content-Type to let browser set it with boundary
                "Content-Type": "",
            },
        }),
};
