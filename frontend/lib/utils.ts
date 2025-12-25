import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function formatConfidence(value: number): string {
    return `${Math.round(value * 100)}%`;
}

export function getConfidenceColor(value: number): string {
    if (value < 0.3) return "text-learning";
    if (value < 0.7) return "text-testing";
    return "text-verifying";
}

export function getConfidenceBg(value: number): string {
    if (value < 0.3) return "bg-learning";
    if (value < 0.7) return "bg-testing";
    return "bg-verifying";
}
