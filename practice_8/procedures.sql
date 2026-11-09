DROP PROCEDURE IF EXISTS bulk_insert_contacts(VARCHAR[], VARCHAR[]);

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_first_names VARCHAR[],
    p_phones VARCHAR[],
    INOUT p_invalid TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    v_i INT; v_fname VARCHAR; v_phone VARCHAR;
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
            p_invalid := array_append(p_invalid, v_fname || ': ' || v_phone);
        END IF;
    END LOOP;
END;
$$;