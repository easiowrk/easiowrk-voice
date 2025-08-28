create extension if not exists vector;

-- agents: stores AI agent configurations
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    stt_provider TEXT NOT NULL,
    llm_provider TEXT NOT NULL,
    tts_provider TEXT NOT NULL,
    tools JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- calls: inbound & outbound call logs
CREATE TABLE calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    customer_number TEXT NOT NULL,
    direction TEXT CHECK (direction IN ('inbound', 'outbound')),
    status TEXT CHECK (status IN ('active', 'completed', 'failed')) DEFAULT 'active',
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

-- messages: transcripts & embeddings for memory
CREATE TABLE messages ( 
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_id UUID REFERENCES calls(id) ON DELETE CASCADE,
    sender TEXT CHECK (sender IN ('agent', 'customer', 'supervisor')) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

-- escalations: when AI hands off to human
CREATE TABLE escalations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_id UUID REFERENCES calls(id) ON DELETE CASCADE,
    issue TEXT NOT NULL,
    status TEXT CHECK (status IN ('pending', 'resolved')) DEFAULT 'pending',
    supervisor_response TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

-- customers: optional, store repeat callers
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number TEXT UNIQUE NOT NULL,
    name TEXT,
    email TEXT,
    last_contact TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
