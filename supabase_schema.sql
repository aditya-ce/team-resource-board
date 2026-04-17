-- SQL Schema for Team Resource Board (Supabase)

-- Enable Row Level Security (RLS)
ALTER TABLE IF EXISTS boards ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS resources ENABLE ROW LEVEL SECURITY;

-- 1. Boards Table
CREATE TABLE IF NOT EXISTS boards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_by UUID REFERENCES auth.users(id),
    is_public BOOLEAN DEFAULT false
);

-- 2. Resources Table
CREATE TABLE IF NOT EXISTS resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    type TEXT CHECK (type IN ('link', 'file', 'image', 'video')) DEFAULT 'link',
    created_by UUID REFERENCES auth.users(id)
);

-- 3. RLS Policies (Security as a Service)
-- Policy: Anyone can view public boards
CREATE POLICY "Public boards are viewable by everyone" ON boards
    FOR SELECT USING (is_public = true);

-- Policy: Authenticated users can create boards
CREATE POLICY "Users can create their own boards" ON boards
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Policy: Users can see resources of boards they have access to
CREATE POLICY "Resources are viewable by board access" ON resources
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM boards WHERE boards.id = resources.board_id AND (boards.is_public = true OR boards.created_by = auth.uid())
        )
    );
