
GET_USER_BY_USERNAME_QUERY = """
    SELECT id, firstname, middle_name, lastname, username, email, email_verified, password, usertype, 
    phone_number, street, city, state, country, image_url, salt, accept_condition, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE username = :username;
"""


GET_USER_BY_EMAIL_QUERY = """
    SELECT id, firstname, middle_name, lastname, username, email, email_verified, password, usertype, 
    phone_number, street, city, state, country, image_url, salt, accept_condition, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE email = :email;
"""

UPDATE_EMAIL_VERIFIED = """
    UPDATE users
    SET email_verified = true
    WHERE email = :email;
"""