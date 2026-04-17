-- SQL Schema for Team Resource Board (Supabase)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Boards Table
CREATE TABLE IF NOT EXISTS boards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_by UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
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
    tags TEXT,
    created_by UUID REFERENCES auth.users(id) DEFAULT auth.uid(),
    storage_path TEXT
);

-- Backfill schema changes for existing projects where `resources` was created earlier.
ALTER TABLE IF EXISTS resources
    ADD COLUMN IF NOT EXISTS storage_path TEXT;

ALTER TABLE IF EXISTS resources
    ADD COLUMN IF NOT EXISTS tags TEXT;

ALTER TABLE IF EXISTS boards ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS resources ENABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS idx_resources_board_id ON resources(board_id);
CREATE INDEX IF NOT EXISTS idx_resources_storage_path ON resources(storage_path);
CREATE INDEX IF NOT EXISTS idx_resources_tags ON resources(tags);

-- Remove old policy names if this script is re-run
DROP POLICY IF EXISTS "Public boards are viewable by everyone" ON boards;
DROP POLICY IF EXISTS "Users can create their own boards" ON boards;
DROP POLICY IF EXISTS "Resources are viewable by board access" ON resources;

-- Remove latest policies if this script is re-run
DROP POLICY IF EXISTS boards_select_public_or_owner ON boards;
DROP POLICY IF EXISTS boards_insert_authenticated ON boards;
DROP POLICY IF EXISTS boards_update_owner ON boards;
DROP POLICY IF EXISTS boards_delete_owner ON boards;

DROP POLICY IF EXISTS resources_select_by_board_access ON resources;
DROP POLICY IF EXISTS resources_insert_by_board_owner ON resources;
DROP POLICY IF EXISTS resources_update_owner_or_board_owner ON resources;
DROP POLICY IF EXISTS resources_delete_owner_or_board_owner ON resources;

-- 3. RLS Policies (Security as a Service)
CREATE POLICY boards_select_public_or_owner ON boards
    FOR SELECT
    USING (is_public = true OR created_by = auth.uid());

CREATE POLICY boards_insert_authenticated ON boards
    FOR INSERT
    TO authenticated
    WITH CHECK (created_by = auth.uid());

CREATE POLICY boards_update_owner ON boards
    FOR UPDATE
    TO authenticated
    USING (created_by = auth.uid())
    WITH CHECK (created_by = auth.uid());

CREATE POLICY boards_delete_owner ON boards
    FOR DELETE
    TO authenticated
    USING (created_by = auth.uid());

CREATE POLICY resources_select_by_board_access ON resources
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1
            FROM boards
            WHERE boards.id = resources.board_id
              AND (boards.is_public = true OR boards.created_by = auth.uid())
        )
    );

CREATE POLICY resources_insert_by_board_owner ON resources
    FOR INSERT
    TO authenticated
    WITH CHECK (
        created_by = auth.uid()
        AND EXISTS (
            SELECT 1
            FROM boards
            WHERE boards.id = resources.board_id
              AND boards.created_by = auth.uid()
        )
    );

CREATE POLICY resources_update_owner_or_board_owner ON resources
    FOR UPDATE
    TO authenticated
    USING (
        created_by = auth.uid()
        OR EXISTS (
            SELECT 1
            FROM boards
            WHERE boards.id = resources.board_id
              AND boards.created_by = auth.uid()
        )
    )
    WITH CHECK (
        created_by = auth.uid()
        OR EXISTS (
            SELECT 1
            FROM boards
            WHERE boards.id = resources.board_id
              AND boards.created_by = auth.uid()
        )
    );

CREATE POLICY resources_delete_owner_or_board_owner ON resources
    FOR DELETE
    TO authenticated
    USING (
        created_by = auth.uid()
        OR EXISTS (
            SELECT 1
            FROM boards
            WHERE boards.id = resources.board_id
              AND boards.created_by = auth.uid()
        )
    );

-- 4. Storage bucket and object policies
INSERT INTO storage.buckets (id, name, public)
VALUES ('resource-files', 'resource-files', false)
ON CONFLICT (id) DO NOTHING;

-- In some environments this script may run as a role that is not owner of storage.objects.
-- Wrap storage policy DDL to avoid aborting the whole migration with SQLSTATE 42501.
DO $storage_policy_setup$
BEGIN
    EXECUTE 'ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY';

    EXECUTE 'DROP POLICY IF EXISTS storage_select_resource_files ON storage.objects';
    EXECUTE 'DROP POLICY IF EXISTS storage_insert_resource_files ON storage.objects';
    EXECUTE 'DROP POLICY IF EXISTS storage_update_resource_files ON storage.objects';
    EXECUTE 'DROP POLICY IF EXISTS storage_delete_resource_files ON storage.objects';

    EXECUTE $policy_select$
        CREATE POLICY storage_select_resource_files ON storage.objects
            FOR SELECT
            TO authenticated
            USING (
                bucket_id = 'resource-files'
                AND EXISTS (
                    SELECT 1
                    FROM resources r
                    JOIN boards b ON b.id = r.board_id
                    WHERE r.storage_path = storage.objects.name
                      AND (b.is_public = true OR b.created_by = auth.uid() OR r.created_by = auth.uid())
                )
            )
    $policy_select$;

    EXECUTE $policy_insert$
        CREATE POLICY storage_insert_resource_files ON storage.objects
            FOR INSERT
            TO authenticated
            WITH CHECK (
                bucket_id = 'resource-files'
                AND owner = auth.uid()
            )
    $policy_insert$;

    EXECUTE $policy_update$
        CREATE POLICY storage_update_resource_files ON storage.objects
            FOR UPDATE
            TO authenticated
            USING (
                bucket_id = 'resource-files'
                AND owner = auth.uid()
            )
            WITH CHECK (
                bucket_id = 'resource-files'
                AND owner = auth.uid()
            )
    $policy_update$;

    EXECUTE $policy_delete$
        CREATE POLICY storage_delete_resource_files ON storage.objects
            FOR DELETE
            TO authenticated
            USING (
                bucket_id = 'resource-files'
                AND owner = auth.uid()
            )
    $policy_delete$;
EXCEPTION
    WHEN insufficient_privilege THEN
        RAISE NOTICE 'Skipping storage.objects policy setup: current role is not table owner (SQLSTATE 42501). Configure storage policies in Supabase Dashboard as owner/admin role.';
END
$storage_policy_setup$;
