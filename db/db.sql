CREATE TABLE prospects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Source
    source VARCHAR(50) NOT NULL,
    source_url TEXT,

    -- Type de prospect
    entity_type VARCHAR(50), -- association, creator, saas, ecommerce, freelancer

    -- Infos principales
    name TEXT NOT NULL,
    short_description TEXT,
    long_description TEXT,

    -- Contact
    email TEXT,
    phone TEXT,
    website TEXT,

    -- Réseaux sociaux
    instagram TEXT,
    linkedin TEXT,
    tiktok TEXT,
    youtube TEXT,

    -- Localisation
    address TEXT,
    city TEXT,
    zipcode TEXT,
    country TEXT,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    -- Assets
    logo_url TEXT,
    banner_url TEXT,

    -- Tracking
    first_seen_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_contacted_at TIMESTAMP,

    unsubscribed BOOLEAN DEFAULT FALSE,

    -- Données additionnelles
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE campaign (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT,
    template TEXT,
    subject TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prospect_id UUID REFERENCES prospects(id) ON DELETE CASCADE,
    campaign_id UUID REFERENCES campaign(id) ON DELETE CASCADE,

    to_addr TEXT,
    from_addr TEXT,
    sent_at TIMESTAMP,

    subject TEXT,
    content TEXT,

    brevo_id TEXT
);

CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    prospect_id UUID REFERENCES prospects(id) ON DELETE CASCADE,
    email_id UUID REFERENCES emails(id) ON DELETE CASCADE,

    event_type TEXT, -- opened, clicked, bounced

    received_at TIMESTAMP DEFAULT NOW(),

    metadata JSONB DEFAULT '{}'::jsonb
);