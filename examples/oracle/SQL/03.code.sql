rem DESCRIPTION
rem    1. Creates a statement level trigger on the EMPLOYEES table
rem       to allow DML during business hours.
rem    2. Creates a row level trigger on the EMPLOYEES table,
rem       after UPDATES on the department_id or job_id columns.
rem    3. Creates a stored procedure to insert a row into the
rem       JOB_HISTORY table.  
rem    4. The defined row level trigger calls the stored procedure. 

SET FEEDBACK 1
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL ON
SET TAB OFF
SET PAGESIZE 100
SET ECHO OFF

REM **************************************************************************

REM procedure and statement trigger to allow dmls during business hours:
CREATE OR REPLACE PROCEDURE secure_dml
IS
BEGIN
  IF TO_CHAR (SYSDATE, 'HH24:MI') NOT BETWEEN '08:00' AND '18:00'
        OR TO_CHAR (SYSDATE, 'DY') IN ('SAT', 'SUN') THEN
	RAISE_APPLICATION_ERROR (-20205, 
		'You may only make changes during normal office hours');
  END IF;
END secure_dml;
/

CREATE OR REPLACE TRIGGER secure_employees
  BEFORE INSERT OR UPDATE OR DELETE ON employees
BEGIN
  secure_dml;
END secure_employees;
/

ALTER TRIGGER secure_employees DISABLE;

REM **************************************************************************
REM procedure to add a row to the JOB_HISTORY table and row trigger 
REM to call the procedure when data is updated in the job_id or 
REM department_id columns in the EMPLOYEES table:

CREATE OR REPLACE PROCEDURE add_job_history
  (  p_emp_id          job_history.employee_id%type
   , p_start_date      job_history.start_date%type
   , p_end_date        job_history.end_date%type
   , p_job_id          job_history.job_id%type
   , p_department_id   job_history.department_id%type 
   )
IS
BEGIN
  INSERT INTO job_history (employee_id, start_date, end_date, 
                           job_id, department_id)
    VALUES(p_emp_id, p_start_date, p_end_date, p_job_id, p_department_id);
END add_job_history;
/

CREATE OR REPLACE TRIGGER update_job_history
  AFTER UPDATE OF job_id, department_id ON employees
  FOR EACH ROW
BEGIN
  add_job_history(:old.employee_id, :old.hire_date, sysdate, 
                  :old.job_id, :old.department_id);
END;
/

COMMIT;

CREATE OR REPLACE FUNCTION get_employee_name (p_employee_id IN employees.employee_id%type)
  RETURN VARCHAR2
IS
  v_employee_name VARCHAR2(100);
BEGIN
  SELECT first_name || ' ' || last_name
    INTO v_employee_name
    FROM employees
    WHERE employee_id = p_employee_id;
  RETURN v_employee_name;
END get_employee_name;
/

COMMIT;

CREATE OR REPLACE TYPE temp_list AS TABLE OF VARCHAR2(100);
/

COMMIT;

CREATE OR REPLACE PACKAGE employee_pkg AS
  FUNCTION get_employee_name (p_employee_id IN employees.employee_id%type)
    RETURN VARCHAR2;
  FUNCTION get_employee_names (p_department_id IN employees.department_id%type)
    RETURN temp_list;
END employee_pkg;
/

CREATE OR REPLACE PACKAGE BODY employee_pkg AS
  FUNCTION get_employee_name (p_employee_id IN employees.employee_id%type)
    RETURN VARCHAR2
  IS
    v_employee_name VARCHAR2(100);
  BEGIN
    SELECT first_name || ' ' || last_name
      INTO v_employee_name
      FROM employees
      WHERE employee_id = p_employee_id;
    RETURN v_employee_name;
  END get_employee_name;

  FUNCTION get_employee_names (p_department_id IN employees.department_id%type)
    RETURN temp_list
  IS
    v_employee_names temp_list;
  BEGIN
    SELECT first_name || ' ' || last_name
      BULK COLLECT INTO v_employee_names
      FROM employees
      WHERE department_id = p_department_id;
    RETURN v_employee_names;
  END get_employee_names;
END employee_pkg;
/

COMMIT;