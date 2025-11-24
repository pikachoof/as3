"""
SQL statements supporting reporting and data maintenance tasks for the caregivers
platform. Statements are listed in assignment order (Task X.Y) so they can be run
sequentially as needed.
"""

TASK_STATEMENTS = {
    "Task 2.1": """
    INSERT INTO caregivers (
        id, first_name, last_name, caregiver_type, gender, photo_url,
        email, phone, city, hourly_rate, bio, password_hash
    ) VALUES
        (1, 'Arman', 'Armanov', 'Babysitter', 'Male', NULL,
         'arman@example.com', '+77771234567', 'Astana', 9.5,
         'Certified babysitter with early childhood CPR training',
         'hashed_pw_arman'),
        (2, 'Dana', 'Zhan', 'Elderly Care', 'Female', NULL,
         'dana@example.com', '+77772345678', 'Astana', 12.0,
         'Experienced nurse specialized in elder care',
         'hashed_pw_dana'),
        (3, 'Timur', 'Bekov', 'Babysitter', 'Male', NULL,
         'timur@example.com', '+77773456789', 'Astana', 11.0,
         'STEM tutor and bilingual babysitter',
         'hashed_pw_timur'),
        (4, 'Madina', 'Sadyk', 'Special Needs', 'Female', NULL,
         'madina@example.com', '+77774567890', 'Astana', 16.0,
         'Special education assistant with ten years of experience',
         'hashed_pw_madina');
    """.strip(),
    "Task 2.2": """
    INSERT INTO family_members (
        id, first_name, last_name, email, phone, password_hash, city,
        address, care_recipient_info, house_rules
    ) VALUES
        (1, 'Amina', 'Aminova', 'amina@example.com', '+77770000001',
         'hashed_pw_amina', 'Astana', '45 Kabanbay Batyr Street',
         'Daughter, 4 years old', 'No pets, quiet after 21:00'),
        (2, 'Bolat', 'Bolatov', 'bolat@example.com', '+77770000002',
         'hashed_pw_bolat', 'Astana', '12 Dostyk Avenue',
         'Father, 72 years old', 'No pets.'),
        (3, 'Kamila', 'Sultanova', 'kamila@example.com', '+77770000003',
         'hashed_pw_kamila', 'Astana', '78 Turan Avenue',
         'Son, 3 years old', 'No smoking indoors'),
        (4, 'Yerbol', 'Nurtay', 'yerbol@example.com', '+77770000004',
         'hashed_pw_yerbol', 'Astana', '23 Mangilik El Avenue',
         'Mother, 80 years old', 'Quiet hours after 22:00');
    """.strip(),
    "Task 2.3": """
    INSERT INTO job_posts (
        id, family_id, title, caregiver_type, city, care_recipient_age,
        description, preferred_time_slots, frequency, requirements
    ) VALUES
        (1, 1, 'Evening Babysitter', 'Babysitter', 'Astana', 4,
         'Need help with evening routine for preschooler',
         '["Weekdays 18:00-21:00"]', 'Weekdays',
         'Energetic, soft-spoken, patient'),
        (2, 2, 'Companion for Elderly Parent', 'Elderly Care', 'Astana', 72,
         'Provide companionship and light exercise support',
         '["Daily 09:00-12:00"]', 'Daily',
         'Must be soft-spoken and punctual'),
        (3, 3, 'Weekend Babysitter', 'Babysitter', 'Astana', 3,
         'Focus on creative play and meal prep for toddler',
         '["Weekends 10:00-16:00"]', 'Weekends',
         'Comfortable with toddlers; creative play'),
        (4, 4, 'Overnight Elderly Care', 'Elderly Care', 'Astana', 80,
         'Overnight supervision and medication reminders',
         '["Weekdays 22:00-06:00"]', 'Weeknights',
         'Experienced with medication schedules');
    """.strip(),
    "Task 2.4": """
    INSERT INTO job_applications (
        id, job_post_id, caregiver_id, cover_message, status
    ) VALUES
        (1, 2, 2, 'I have eight years supporting elders with dementia.', 'accepted'),
        (2, 3, 1, 'Weekend availability and Montessori training.', 'accepted'),
        (3, 3, 3, 'STEM tutor offering creative activities.', 'applied'),
        (4, 4, 2, 'Comfortable with overnight schedules and medication.', 'applied'),
        (5, 2, 1, 'Bilingual support and light cooking.', 'applied'),
        (6, 3, 4, 'Experienced in special needs childcare.', 'applied');
    """.strip(),
    "Task 2.5": """
    INSERT INTO appointments (
        id, caregiver_id, family_id, appointment_date, start_time,
        duration_hours, status, notes
    ) VALUES
        (1, 2, 2, '2025-11-01', '09:00', 4.0, 'accepted', 'Morning companionship session'),
        (2, 1, 3, '2025-11-02', '10:00', 5.0, 'accepted', 'Weekend creative activities'),
        (3, 3, 3, '2025-11-03', '12:00', 3.0, 'accepted', 'Afternoon tutoring and play'),
        (4, 2, 4, '2025-11-05', '22:00', 8.0, 'accepted', 'Overnight supervision and medication'),
        (5, 4, 4, '2025-11-06', '22:00', 6.0, 'pending', 'Trial overnight shift');
    """.strip(),
    "Task 2.6": """
    INSERT INTO messages (
        id, sender_family_id, sender_caregiver_id, receiver_family_id,
        receiver_caregiver_id, content
    ) VALUES
        (1, 2, NULL, NULL, 2, 'We appreciate your support with our father.'),
        (2, NULL, 1, 3, NULL, 'Looking forward to the weekend appointment.');
    """.strip(),
    "Task 3.1": """
        UPDATE caregivers
        SET phone = '+77773414141'
        WHERE first_name = 'Arman' AND last_name = 'Armanov';
    """.strip(),
    "Task 3.2": """
        UPDATE caregivers
        SET hourly_rate = ROUND(
            CASE
                WHEN hourly_rate < 10 THEN hourly_rate + 0.3
                ELSE hourly_rate * 1.10
            END,
            2
        );
    """.strip(),
    "Task 4.1": """
        DELETE FROM job_posts
        WHERE family_id = (
            SELECT id
            FROM family_members
            WHERE first_name = 'Amina' AND last_name = 'Aminova'
        );
    """.strip(),
    "Task 4.2": """
        DELETE FROM family_members
        WHERE LOWER(address) LIKE '%kabanbay batyr%';
    """.strip(),
    "Task 5.1": """
        SELECT
            c.first_name || ' ' || c.last_name AS caregiver_name,
            f.first_name || ' ' || f.last_name AS family_member_name,
            a.appointment_date,
            a.start_time,
            a.duration_hours
        FROM appointments AS a
        INNER JOIN caregivers AS c ON c.id = a.caregiver_id
        INNER JOIN family_members AS f ON f.id = a.family_id
        WHERE a.status = 'accepted'
        ORDER BY a.appointment_date, caregiver_name;
    """.strip(),
    "Task 5.2": """
        SELECT id AS job_id
        FROM job_posts
        WHERE LOWER(requirements) LIKE '%soft-spoken%'
        ORDER BY id;
    """.strip(),
    "Task 5.3": """
        SELECT
            id AS job_id,
            title,
            preferred_time_slots AS work_hours
        FROM job_posts
        WHERE caregiver_type = 'Babysitter'
        ORDER BY id;
    """.strip(),
    "Task 5.4": """
        SELECT DISTINCT
            f.id,
            f.first_name,
            f.last_name,
            f.city
        FROM family_members AS f
        INNER JOIN job_posts AS jp ON jp.family_id = f.id
        WHERE jp.caregiver_type = 'Elderly Care'
          AND jp.city = 'Astana'
          AND f.house_rules LIKE '%No pets.%'
        ORDER BY f.last_name;
    """.strip(),
    "Task 6.1": """
        SELECT
            fm.first_name || ' ' || fm.last_name AS member_name,
            jp.id AS job_id,
            COUNT(ja.id) AS applicant_count
        FROM family_members AS fm
        INNER JOIN job_posts AS jp ON jp.family_id = fm.id
        LEFT JOIN job_applications AS ja ON ja.job_post_id = jp.id
        GROUP BY fm.id, jp.id
        ORDER BY fm.last_name, jp.id;
    """.strip(),
    "Task 6.2": """
        SELECT
            c.first_name || ' ' || c.last_name AS caregiver_name,
            SUM(a.duration_hours) AS total_hours
        FROM caregivers AS c
        INNER JOIN appointments AS a ON a.caregiver_id = c.id
        WHERE a.status = 'accepted'
        GROUP BY c.id
        ORDER BY total_hours DESC;
    """.strip(),
    "Task 6.3": """
        SELECT
            c.first_name || ' ' || c.last_name AS caregiver_name,
            AVG(a.duration_hours * c.hourly_rate) AS average_pay
        FROM caregivers AS c
        INNER JOIN appointments AS a ON a.caregiver_id = c.id
        WHERE a.status = 'accepted'
        GROUP BY c.id
        ORDER BY average_pay DESC;
    """.strip(),
    "Task 6.4": """
        SELECT
            c.first_name || ' ' || c.last_name AS caregiver_name,
            SUM(a.duration_hours * c.hourly_rate) AS total_earnings
        FROM caregivers AS c
        INNER JOIN appointments AS a ON a.caregiver_id = c.id
        WHERE a.status = 'accepted'
        GROUP BY c.id
        HAVING SUM(a.duration_hours * c.hourly_rate) > (
            SELECT AVG(caregiver_earnings)
            FROM (
                SELECT
                    SUM(a2.duration_hours * c2.hourly_rate) AS caregiver_earnings
                FROM caregivers AS c2
                INNER JOIN appointments AS a2 ON a2.caregiver_id = c2.id
                WHERE a2.status = 'accepted'
                GROUP BY c2.id
            ) AS earnings_per_caregiver
        )
        ORDER BY total_earnings DESC;
    """.strip(),
    "Task 7.1": """
    SELECT
        c.id AS caregiver_id,
        c.first_name || ' ' || c.last_name AS caregiver_name,
        SUM(a.duration_hours) AS total_hours,
        c.hourly_rate AS current_hourly_rate,
        SUM(a.duration_hours * c.hourly_rate) AS total_cost
    FROM caregivers AS c
    INNER JOIN appointments AS a ON a.caregiver_id = c.id
    WHERE a.status = 'accepted'
    GROUP BY c.id
    ORDER BY total_cost DESC;
    """.strip(),
    "Task 8.1": """
    CREATE VIEW IF NOT EXISTS vw_job_applications AS
    SELECT
        ja.id AS application_id,
        jp.id AS job_post_id,
        jp.title AS job_title,
        fm.first_name || ' ' || fm.last_name AS family_member_name,
        c.first_name || ' ' || c.last_name AS caregiver_name,
        ja.status,
        ja.created_at
    FROM job_applications AS ja
    INNER JOIN job_posts AS jp ON jp.id = ja.job_post_id
    INNER JOIN family_members AS fm ON fm.id = jp.family_id
    INNER JOIN caregivers AS c ON c.id = ja.caregiver_id;
    """.strip()
}
