CREATE DATABASE employee_attendance_db;
USE employee_attendance_db;
CREATE TABLE employees 
(
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    joining_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE attendance 
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
CREATE TABLE tasks 
(
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    task_date DATE NOT NULL,
    tasks_completed INT NOT NULL DEFAULT 0,
    task_status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
SHOW TABLES;
DESCRIBE employees;
DESCRIBE attendance;
DESCRIBE tasks;
INSERT INTO employees(employee_name, department, email, joining_date) VALUES
('Arun Kumar', 'IT', 'arun@company.com', '2025-01-10'),
('Priya Sharma', 'HR', 'priya@company.com', '2025-02-15'),
('Karthik Raj', 'IT', 'karthik@company.com', '2025-03-01'),
('Divya S', 'Finance', 'divya@company.com', '2025-04-12'),
('Rahul M', 'HR', 'rahul@company.com', '2025-05-20');
INSERT INTO attendance(employee_id, attendance_date, clock_in, clock_out, status) VALUES
(1, '2026-10-12', '2026-10-12 09:00:00','2026-10-12 17:00:00', 'Present'),
(2, '2026-10-12', '2026-10-12 09:30:00','2026-10-12 17:00:00', 'Present'),
(3, '2026-10-12', NULL, NULL, 'Absent'),
(4, '2026-10-12', '2026-10-12 08:55:00','2026-10-12 17:10:00', 'Present'),
(5, '2026-10-12', '2026-10-12 09:05:00','2026-10-12 17:00:00', 'Present');
INSERT INTO tasks(employee_id, task_name, task_date,tasks_completed, task_status)VALUES
(1, 'SQL reporting', '2026-10-12', 4, 'Completed'),
(2, 'Employee records update', '2026-10-12', 3, 'Completed'),
(3, 'Database testing', '2026-10-12', 0, 'Pending'),
(4, 'Monthly report', '2026-10-12', 5, 'Completed'),
(5, 'Data validation', '2026-10-12', 2, 'In Progress');
INSERT INTO employees (employee_name, department, email, joining_date) VALUES
('Manoj Kumar', 'IT', 'manoj@company.com', '2026-01-15');
SELECT employee_id, employee_name, email FROM employees WHERE department = 'IT';
SELECT e.employee_name, e.department, a.attendance_date, a.clock_in, a.clock_out, a.status
FROM employees e INNER JOIN attendance a ON e.employee_id = a.employee_id;
UPDATE attendance SET clock_out = '2026-10-12 17:30:00' WHERE employee_id = 1 AND attendance_date = '2026-10-12';
DELETE FROM tasks WHERE task_id = 5;
SELECT * FROM attendance WHERE employee_id = 1 AND attendance_date = CURDATE();
UPDATE attendance SET clock_in = NOW(), status = 'Present' WHERE employee_id = 1 AND attendance_date = CURDATE() AND clock_in IS NULL;
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
CALL CalculateWorkingHours();
