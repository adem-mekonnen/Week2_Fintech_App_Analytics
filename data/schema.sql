-- schema.sql
-- Database Schema for Fintech App Analytics

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

CREATE TABLE banks (
    bank_id VARCHAR(100) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id VARCHAR(100) NOT NULL,
    review_text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    identified_theme VARCHAR(100),
    source VARCHAR(50) DEFAULT 'Google Play',
    CONSTRAINT fk_bank FOREIGN KEY(bank_id) REFERENCES banks(bank_id)
);

CREATE INDEX idx_bank_id ON reviews(bank_id);
CREATE INDEX idx_sentiment ON reviews(sentiment_label);