-- =====================================================================
-- TSIS 1: PhoneBook - extended schema
-- Safe to run several times (idempotent) and safe for the existing
-- Practice 7-8 table contacts(first_name, phone).
-- Run in pgAdmin: Query Tool -> open this file -> Execute (F5).
-- =====================================================================

-- 0. Base table (only created if Practice 7 table does not exist yet)
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    phone      VARCHAR(20)
);

-- If the old table has no id column, add one (needed for foreign keys)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'contacts' AND column_name = 'id'
    ) THEN
        ALTER TABLE contacts ADD COLUMN id SERIAL UNIQUE;
    END IF;
END $$;

-- The main phone now lives in the phones table, so the old column
-- must not be mandatory any more (it is kept for Practice 8 compatibility).
ALTER TABLE contacts ALTER COLUMN phone DROP NOT NULL;

-- 1. Groups (categories)
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- 2. New columns in contacts: email, birthday, group, date added
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email      VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday   DATE,
    ADD COLUMN IF NOT EXISTS group_id   INTEGER REFERENCES groups(id),
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- Contacts without a group go to "Other"
UPDATE contacts
SET group_id = (SELECT id FROM groups WHERE name = 'Other')
WHERE group_id IS NULL;

-- 3. Phones: 1-to-many (one contact -> many phone numbers)
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- 4. Move old single phones (Practice 7-8) into the phones table
INSERT INTO phones (contact_id, phone, type)
SELECT c.id, c.phone, 'mobile'
FROM contacts c
WHERE c.phone IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM phones p
      WHERE p.contact_id = c.id AND p.phone = c.phone
  );

-- 5. Indexes to speed up searching
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts (email);
CREATE INDEX IF NOT EXISTS idx_phones_contact ON phones (contact_id);
