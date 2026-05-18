-- backend/schema.sql

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. User Emails Table (একজন ইউজারের একাধিক ইমেইল)
CREATE TABLE IF NOT EXISTS user_emails (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    email_address VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Emails Table (যে মেইলগুলো আসবে)
CREATE TABLE IF NOT EXISTS emails (
    id BIGSERIAL PRIMARY KEY,
    user_email_id BIGINT REFERENCES user_emails(id) ON DELETE CASCADE,
    from_email VARCHAR(255),
    from_name VARCHAR(255),
    subject TEXT,
    text_body TEXT,
    html_body TEXT,
    message_id VARCHAR(255),
    received_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster search
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_user_emails_address ON user_emails(email_address);
CREATE INDEX idx_emails_user_email_id ON emails(user_email_id);
