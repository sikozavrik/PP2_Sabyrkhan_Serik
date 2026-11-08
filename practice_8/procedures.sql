DROP PROCEDURE IF EXISTS upsert_contact(VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE upsert_contact(p_first_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_first_name) THEN
        UPDATE contacts SET phone = p_phone WHERE first_name = p_first_name;
    ELSE
        INSERT INTO contacts(first_name, phone) VALUES(p_first_name, p_phone);
    END IF;
END;
$$;

DROP PROCEDURE IF EXISTS bulk_insert_contacts(VARCHAR[], VARCHAR[]);

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_first_names VARCHAR[], 
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    v_i INT;
    v_fname VARCHAR;
    v_phone VARCHAR;
BEGIN
    FOR v_i IN 1..array_length(p_first_names, 1) LOOP
        v_fname := p_first_names[v_i];
        v_phone := p_phones[v_i];
        
        IF v_phone ~ '^\+?[0-9\-\s]{5,15}$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE first_name = v_fname) THEN
                UPDATE contacts SET phone = v_phone WHERE first_name = v_fname;
            ELSE
                INSERT INTO contacts(first_name, phone) VALUES(v_fname, v_phone);
            END IF;
        ELSE
            RAISE NOTICE 'Invalid phone format for contact: % (%)', v_fname, v_phone;
        END IF;
    END LOOP;
END;
$$;

DROP PROCEDURE IF EXISTS delete_contact(VARCHAR);

CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE first_name = p_identifier OR phone = p_identifier;
END;
$$;