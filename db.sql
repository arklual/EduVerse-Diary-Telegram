

CREATE TABLE users
(
    id serial NOT NULL,
    user_id character varying(255) NOT NULL,
    subscription_status boolean NOT NULL DEFAULT true,
    leaved_review boolean NOT NULL DEFAULT false,
    join_date timestamptz NOT NULL DEFAULT NOW(),
    get_emails boolean NOT NULL DEFAULT true,
    school character varying(255),
    locality character varying(255),
    login_text character varying(255),
    password_text character varying(255),
    CONSTRAINT users_pkey PRIMARY KEY (id)
)
ALTER TABLE users ADD CONSTRAINT unique_login_text UNIQUE(login_text)

