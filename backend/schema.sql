-- Database Schema for Aiversehack01: Belief Testing System

-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    github_username TEXT,
    linkedin_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Evidence Table (Raw data artifacts)
CREATE TABLE evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    type TEXT NOT NULL, -- 'resume', 'github_repo', 'linkedin_profile'
    content_raw TEXT, -- Text extracted from PDF or raw JSON from API
    source_url TEXT,
    captured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. BeliefState Table (The Failure Passport)
CREATE TABLE belief_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    version INTEGER NOT NULL,
    -- assumptions is a JSONB array: 
    -- [{"attribute": "Python Proficiency", "basis": "Github Repo X", "confidence": 0.62, "last_updated": "..."}]
    assumptions JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Experiments Table (Actions taken to test beliefs)
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    belief_state_id UUID REFERENCES belief_state(id),
    type TEXT NOT NULL, -- 'application', 'hackathon_submission', 'portfolio_update'
    hypothesis TEXT NOT NULL, -- e.g. "Applying to Backend roles tests Python belief"
    meta_data JSONB, -- Job details, submission links
    status TEXT DEFAULT 'pending', -- 'pending', 'active', 'completed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Outcomes Table (Results of experiments)
CREATE TABLE outcomes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID REFERENCES experiments(id),
    type TEXT NOT NULL, -- 'rejection', 'ghosting', 'invite', 'win'
    raw_response TEXT, -- e.g. Email body
    belief_impact JSONB, -- How this specific outcome shifted confidence (calculated by Reflection Agent)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
