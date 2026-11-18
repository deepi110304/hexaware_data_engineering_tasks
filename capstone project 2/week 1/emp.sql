-- 1. CREATE DATABASE
CREATE DATABASE IF NOT EXISTS employee_attendance_db;
USE employee_attendance_db;
-- 2. CREATE EMPLOYEES TABLE
CREATE TABLE IF NOT EXISTS employees 
(
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    joining_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);
-- 3. CREATE ATTENDANCE TABLE
CREATE TABLE IF NOT EXISTS attendance 
(
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    clock_in DATETIME,
    clock_out DATETIME,
    status VARCHAR(20) NOT NULL DEFAULT 'Present',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id), 
    UNIQUE (employee_id, attendance_date)
);
-- 4. CREATE TASKS TABLE
CREATE TABLE IF NOT EXISTS tasks 
(
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    task_date DATE NOT NULL,
    tasks_completed INT NOT NULL DEFAULT 0,
    task_status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);
-- 5. VERIFY TABLES
SHOW TABLES;
DESCRIBE employees;
DESCRIBE attendance;
DESCRIBE tasks;
-- 6. INSERT SAMPLE EMPLOYEES
INSERT INTO employees VALUES
('Arun Kumar', 'IT', 'arun@company.com', '2025-01-10'),
('Priya Sharma', 'HR', 'priya@company.com', '2025-02-15'),
('Karthik Raj', 'IT', 'karthik@company.com', '2025-03-01'),
('Divya S', 'Finance', 'divya@company.com', '2025-04-12'),
('Rahul M', 'HR', 'rahul@company.com', '2025-05-20'),
('Manoj Kumar', 'IT', 'manoj@company.com', '2026-01-15');
-- 7. INSERT VALUES FOR ATTENDANCE
INSERT INTO attendance VALUES
(1, '2026-10-12', '2026-10-12 09:00:00','2026-10-12 17:00:00', 'Present'),
(2, '2026-10-12', '2026-10-12 09:30:00','2026-10-12 17:00:00', 'Present'),
(3, '2026-10-12', NULL, NULL, 'Absent'),
(4, '2026-10-12', '2026-10-12 08:55:00','2026-10-12 17:10:00', 'Present'),
(5, '2026-10-12', '2026-10-12 09:05:00','2026-10-12 17:00:00', 'Present');
-- 8. INSERT VALUES FOR TASKS
INSERT INTO tasks VALUES
(1, 'SQL reporting', '2026-10-12', 4, 'Completed'),
(2, 'Employee records update', '2026-10-12', 3, 'Completed'),
(3, 'Database testing', '2026-10-12', 0, 'Pending'),
(4, 'Monthly report', '2026-10-12', 5, 'Completed'),
(5, 'Data validation', '2026-10-12', 2, 'In Progress');
-- 9. READ: DISPLAY ALL EMPLOYEES
SELECT * FROM employees;
-- 10. READ: EMPLOYEES IN THE IT DEPARTMENT
SELECT employee_id, employee_name, email FROM employees WHERE department = 'IT';
-- 11. READ: ATTENDANCE WITH EMPLOYEE DETAILS
SELECT e.employee_id, e.employee_name, e.department, a.attendance_date, a.clock_in, a.clock_out, a.status
FROM employees e INNER JOIN attendance a ON e.employee_id = a.employee_id;
-- 12. CREATE: ADD AN EMPLOYEE
INSERT INTO employees (employee_name, department, email, joining_date) VALUES
('Varun Verma', 'IT', 'varunv@company.com', '2026-10-13');
-- 13. UPDATE: CHANGE AN EMPLOYEE'S DEPARTMENT
UPDATE employees SET department = 'Finance' WHERE employee_id = 6;
-- 14. UPDATE: CORRECT A CLOCK-OUT TIME
UPDATE attendance SET clock_out = '2026-10-12 17:30:00' WHERE employee_id = 1 AND attendance_date = '2026-10-12';
-- 15. DELETE: REMOVE A TEST TASK
DELETE FROM tasks WHERE task_id = 2;
-- 16. CHECK AN EMPLOYEE'S ATTENDANCE
SELECT * FROM attendance WHERE employee_id = 1 AND attendance_date = '2026-10-12';
-- 17. CLOCK-IN LOGIC
UPDATE attendance SET clock_in = NOW(), status = 'Present' WHERE employee_id = 1 AND attendance_date = CURDATE() AND clock_in IS NULL;
-- Run the INSERT below only when no record exists for employee 1 today.
INSERT INTO attendance (employee_id, attendance_date, clock_in, status)
SELECT 1, CURDATE(), NOW(), 'Present' WHERE NOT EXISTS (SELECT 1 FROM attendance WHERE employee_id = 1 AND attendance_date = CURDATE());
-- 18. CLOCK-OUT LOGIC
UPDATE attendance SET clock_out = NOW() WHERE employee_id = 1 AND attendance_date = CURDATE() AND clock_in IS NOT NULL AND clock_out IS NULL;
-- 19. STORED PROCEDURE: TOTAL WORKING HOURS
DROP PROCEDURE IF EXISTS CalculateWorkingHours;
DELIMITER $$
CREATE PROCEDURE CalculateWorkingHours()
BEGIN
    SELECT
        e.employee_id,
        e.employee_name,
        COALESCE(
            ROUND(
                SUM(
                    TIMESTAMPDIFF(
                        MINUTE,
                        a.clock_in,
                        a.clock_out
                    )
                ) / 60,
                2
            ),
            0
        ) AS total_working_hours
    FROM employees e
    LEFT JOIN attendance a
        ON e.employee_id = a.employee_id
    GROUP BY
        e.employee_id,
        e.employee_name
    ORDER BY e.employee_id;
END $$
DELIMITER ;
-- 20. EXECUTE THE STORED PROCEDURE
CALL CalculateWorkingHours();
-- 21. VERIFY RECORD COUNTS
SELECT COUNT(*) AS employee_count FROM employees;
SELECT COUNT(*) AS attendance_count FROM attendance;
SELECT COUNT(*) AS task_count FROM tasks;
-- 22. EXPORT QUERY: ATTENDANCE DATA FOR PYTHON
SELECT e.employee_id, e.employee_name, e.department, a.attendance_date, a.clock_in, a.clock_out, a.status
FROM employees e LEFT JOIN attendance a ON e.employee_id = a.employee_id ORDER BY a.attendance_date, e.employee_id;
-- 23. EXPORT QUERY: TASK DATA FOR PYTHON
SELECT e.employee_id, e.employee_name, e.department, t.task_id, t.task_name, t.task_date, t.tasks_completed, t.task_status
FROM employees e LEFT JOIN tasks t ON e.employee_id = t.employee_id ORDER BY t.task_date, e.employee_id;
USE employee_attendance_db;
SELECT e.employee_id, e.employee_name, e.department, a.attendance_date, a.clock_in, a.clock_out, a.status
FROM employees e LEFT JOIN attendance a ON e.employee_id = a.employee_id ORDER BY e.employee_id, a.attendance_date;
SELECT e.employee_id, e.employee_name, e.department, t.task_id, t.task_name, t.task_date, t.tasks_completed, t.task_status
FROM employees e LEFT JOIN tasks t ON e.employee_id = t.employee_id ORDER BY e.employee_id, t.task_date;

USE employee_attendance_db;
SELECT *
FROM tasks
ORDER BY employee_id, task_date;
SELECT task_id, employee_id,task_name,task_date,tasks_completed,task_status FROM tasks
ORDER BY employee_id, task_date;
USE employee_attendance_db;
SELECT
    employee_id,
    employee_name,
    attendance_date,
    clock_in,
    clock_out,
    status,
    TIMESTAMPDIFF(SECOND, clock_in, clock_out) AS duration_seconds
FROM attendance
WHERE employee_id = 1
  AND attendance_date = '2026-10-13';
  
USE employee_attendance_db;

SELECT
    a.employee_id,
    e.employee_name,
    a.attendance_date,
    a.clock_in,
    a.clock_out,
    a.status,
    TIMESTAMPDIFF(
        SECOND,
        a.clock_in,
        a.clock_out
    ) AS duration_seconds
FROM attendance a
JOIN employees e
    ON a.employee_id = e.employee_id
WHERE a.employee_id = 1
  AND a.attendance_date = '2026-10-13';
SELECT *
FROM attendance
WHERE employee_id = 1
  AND attendance_date = '2026-10-13';
SELECT *
FROM attendance
WHERE employee_id = 1
ORDER BY attendance_date;
USE employee_attendance_db;

SELECT
    attendance_id,
    employee_id,
    attendance_date,
    clock_in,
    clock_out,
    TIMESTAMPDIFF(SECOND, clock_in, clock_out) AS duration_seconds
FROM attendance
WHERE employee_id = 1
ORDER BY attendance_date;
USE employee_attendance_db;

UPDATE attendance
SET clock_in = '2026-10-13 09:00:00',
    clock_out = '2026-10-13 17:30:00'
WHERE attendance_id = 7
  AND employee_id = 1
  AND attendance_date = '2026-10-13';
SELECT
    attendance_id,
    employee_id,
    attendance_date,
    clock_in,
    clock_out,
    TIMESTAMPDIFF(SECOND, clock_in, clock_out) AS duration_seconds
FROM attendance
WHERE attendance_id = 7;
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    a.attendance_date,
    a.clock_in,
    a.clock_out,
    a.status
FROM employees e
LEFT JOIN attendance a
    ON e.employee_id = a.employee_id
ORDER BY e.employee_id, a.attendance_date;