-- PostgreSQL Query Examples for FastAPI Database
-- Run these queries using PostgreSQL Extension in VS Code

-- 1. View all users
SELECT * FROM users;

-- 2. View table structure
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'users';

-- 3. Count users by role
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role 
ORDER BY count DESC;

-- 4. Find specific user by email
SELECT * FROM users 
WHERE email LIKE '%example.com%';

-- 5. Insert new user (example)
-- INSERT INTO users (name, email, role) 
-- VALUES ('New User', 'newuser@example.com', 'user');

-- 6. Update user role
-- UPDATE users 
-- SET role = 'admin' 
-- WHERE email = 'user@example.com';

-- 7. Delete user (be careful!)
-- DELETE FROM users 
-- WHERE id = 1;

-- 8. View recent users
SELECT * FROM users 
ORDER BY id DESC 
LIMIT 5;

-- 9. Check for duplicate emails
SELECT email, COUNT(*) as count 
FROM users 
GROUP BY email 
HAVING COUNT(*) > 1;

-- 10. Get database statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables 
WHERE tablename = 'users';
