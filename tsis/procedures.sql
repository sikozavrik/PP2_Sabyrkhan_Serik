-- =====================================================================
-- TSIS 1: PhoneBook - new server-side objects (PL/pgSQL)
-- Run AFTER schema.sql. Practice 8 procedures are NOT duplicated here.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. add_phone: add a new phone number to an existing contact
--    CALL add_phone('Aigerim', '+77015556677', 'work');
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type "%". Use home, work or mobile.', p_type;
    END IF;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    IF EXISTS (
        SELECT 1 FROM phones
        WHERE contact_id = v_contact_id AND phone = p_phone
    ) THEN
        RAISE EXCEPTION 'Contact "%" already has the number %.', p_contact_name, p_phone;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

-- ---------------------------------------------------------------------
-- 2. move_to_group: move a contact to another group
--    (the group is created automatically if it does not exist)
--    CALL move_to_group('Nurlan', 'Work');
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    SELECT id INTO v_group_id
    FROM groups
    WHERE LOWER(name) = LOWER(p_group_name);

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;

-- ---------------------------------------------------------------------
-- 3. search_contacts: search by name, email AND every phone number
--    SELECT * FROM search_contacts('gmail');
--    SELECT * FROM search_contacts('+7701');
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id   INTEGER,
    contact_name VARCHAR,
    email        VARCHAR,
    birthday     DATE,
    group_name   VARCHAR,
    phones       TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name::VARCHAR,
        c.email,
        c.birthday,
        g.name,
        COALESCE(string_agg(p.type || ': ' || p.phone, ', ' ORDER BY p.id), '')
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR EXISTS (
            SELECT 1 FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || p_query || '%'
       )
    GROUP BY c.id, c.first_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
END;
$$;

-- ---------------------------------------------------------------------
-- OPTIONAL: only if you do NOT have the Practice 8 pagination function
-- (or it has a different name), uncomment this block and set the same
-- name in config.py -> PAGINATION_FUNCTION.
-- ---------------------------------------------------------------------
-- CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
-- RETURNS TABLE (id INTEGER, first_name VARCHAR, email VARCHAR, phone VARCHAR)
-- LANGUAGE sql AS $$
--     SELECT c.id, c.first_name::VARCHAR, c.email, c.phone::VARCHAR
--     FROM contacts c
--     ORDER BY c.first_name
--     LIMIT p_limit OFFSET p_offset;
-- $$;
