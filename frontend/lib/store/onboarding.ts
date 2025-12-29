

import { create } from 'zustand';

export type OnboardingStep = 'ingestion' | 'clarification' | 'reveal';

interface OnboardingState {
    step: OnboardingStep;
    resumeFile: File | null;
    githubUrl: string;
    linkedInEnabled: boolean;
    preferences: {
        role: string;
        type: 'internship' | 'fulltime' | 'both';
        location: string;
        hackathons: boolean;
    };
    isIngesting: boolean;

    // Actions
    setStep: (step: OnboardingStep) => void;
    setResume: (file: File | null) => void;
    setGithubUrl: (url: string) => void;
    toggleLinkedIn: () => void;
    updatePreferences: (prefs: Partial<OnboardingState['preferences']>) => void;
    startIngestion: () => void;
    stopIngestion: () => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
    step: 'ingestion',
    resumeFile: null,
    githubUrl: '',
    linkedInEnabled: false,
    preferences: {
        role: '',
        type: 'internship',
        location: '',
        hackathons: true,
    },
    isIngesting: false,

    setStep: (step) => set({ step }),
    setResume: (file) => set({ resumeFile: file }),
    setGithubUrl: (url) => set({ githubUrl: url }),
    toggleLinkedIn: () => set((state) => ({ linkedInEnabled: !state.linkedInEnabled })),
    updatePreferences: (prefs) => set((state) => ({ preferences: { ...state.preferences, ...prefs } })),
    startIngestion: () => set({ isIngesting: true }),
    stopIngestion: () => set({ isIngesting: false }),
}));
