CREATE_TABLE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS caregivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        caregiver_type TEXT NOT NULL,
        gender TEXT,
        photo_url TEXT,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        hourly_rate REAL NOT NULL CHECK (hourly_rate > 0),
        bio TEXT,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """.strip(),
    """
    CREATE TABLE IF NOT EXISTS family_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT,
        care_recipient_info TEXT,
        house_rules TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """.strip(),
    """
    CREATE TABLE IF NOT EXISTS job_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        caregiver_type TEXT NOT NULL,
        city TEXT NOT NULL,
        care_recipient_age INTEGER,
        description TEXT,
        preferred_time_slots TEXT,
        frequency TEXT,
        requirements TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (family_id) REFERENCES family_members(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """.strip(),
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_family_id INTEGER,
        sender_caregiver_id INTEGER,
        receiver_family_id INTEGER,
        receiver_caregiver_id INTEGER,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_family_id) REFERENCES family_members(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        FOREIGN KEY (sender_caregiver_id) REFERENCES caregivers(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        FOREIGN KEY (receiver_family_id) REFERENCES family_members(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
        FOREIGN KEY (receiver_caregiver_id) REFERENCES caregivers(id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
    );
    """.strip(),
    """
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        caregiver_id INTEGER NOT NULL,
        family_id INTEGER NOT NULL,
        appointment_date DATE NOT NULL,
        start_time TIME NOT NULL,
        duration_hours REAL NOT NULL CHECK (duration_hours > 0),
        status TEXT NOT NULL DEFAULT 'pending',
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (caregiver_id) REFERENCES caregivers(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (family_id) REFERENCES family_members(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """.strip(),
    """
    CREATE TABLE IF NOT EXISTS job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_post_id INTEGER NOT NULL,
        caregiver_id INTEGER NOT NULL,
        cover_message TEXT,
        status TEXT NOT NULL DEFAULT 'applied',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_post_id) REFERENCES job_posts(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (caregiver_id) REFERENCES caregivers(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """.strip()
]