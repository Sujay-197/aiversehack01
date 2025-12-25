const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    const token = localStorage.getItem("token");
    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem("token");
        window.location.href = "/login";
        return response;
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
