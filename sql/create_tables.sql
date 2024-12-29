CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_id INTEGER UNIQUE NOT NULL,
    locale TEXT DEFAULT 'en' NOT NULL
);

-- Citizens table
CREATE TABLE citizens (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    balance FLOAT DEFAULT 1000.0,
    home_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
    insurance_company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL
);

-- Companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    balance FLOAT DEFAULT 0.0,
    company_type VARCHAR(50) NOT NULL,
    provides_insurance BOOLEAN DEFAULT FALSE
);

-- Insurance offers table
CREATE TABLE insurance_offers (
    id SERIAL PRIMARY KEY,
    citizen_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    monthly_fee FLOAT,
    status VARCHAR(50) DEFAULT 'pending'
);

-- Properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    rent_fee FLOAT,
    is_available BOOLEAN DEFAULT TRUE
);

-- Jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    employer_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    salary FLOAT NOT NULL,
    terms TEXT NOT NULL,
    is_open BOOLEAN DEFAULT TRUE
);

-- Loans table
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    lender_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    borrower_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    interest_rate FLOAT NOT NULL,
    repayment_term INTEGER NOT NULL,
    remaining_balance FLOAT NOT NULL
);

-- Regions table
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES citizens(id) ON DELETE SET NULL,
    prosperity FLOAT DEFAULT 50.0,
    pollution FLOAT DEFAULT 0.0
);

-- Resources table
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region_id INTEGER REFERENCES regions(id) ON DELETE CASCADE,
    quantity FLOAT NOT NULL,
    extraction_rate FLOAT NOT NULL
);

-- Roads table
CREATE TABLE roads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id INTEGER REFERENCES citizens(id) ON DELETE CASCADE,
    access_fee FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Trade routes table
CREATE TABLE trade_routes (
    id SERIAL PRIMARY KEY,
    region_a_id INTEGER REFERENCES regions(id) ON DELETE CASCADE,
    region_b_id INTEGER REFERENCES regions(id) ON DELETE CASCADE,
    trade_volume FLOAT DEFAULT 0.0,
    tariff_rate FLOAT DEFAULT 0.0
);

-- Public projects table
CREATE TABLE public_projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cost FLOAT NOT NULL,
    funds_raised FLOAT DEFAULT 0.0,
    is_completed BOOLEAN DEFAULT FALSE
);
