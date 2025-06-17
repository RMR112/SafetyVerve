-- Drop tables if they exist
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS divisions;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS incident_types;
DROP TABLE IF EXISTS severity_levels;

-- Companies
CREATE TABLE companies (
    company_id    INTEGER PRIMARY KEY,
    name          TEXT NOT NULL
);

-- Projects (linked to company)
CREATE TABLE projects (
    project_id    INTEGER PRIMARY KEY,
    company_id    INTEGER NOT NULL,
    project_name  TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Divisions (linked to company)
CREATE TABLE divisions (
    division_id    INTEGER PRIMARY KEY,
    company_id     INTEGER NOT NULL,
    division_name  TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Employees (linked to company)
CREATE TABLE employees (
    employee_id   INTEGER PRIMARY KEY,
    company_id    INTEGER NOT NULL,
    name          TEXT NOT NULL,
    designation   TEXT,
    age           INTEGER,
    gender        TEXT,
    department    TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Incident Types
CREATE TABLE incident_types (
    type_id     INTEGER PRIMARY KEY,
    type_name   TEXT NOT NULL
);

-- Severity Levels
CREATE TABLE severity_levels (
    severity_id   INTEGER PRIMARY KEY,
    label         TEXT NOT NULL
);

-- Incidents (linked to company, project, division, employee)
CREATE TABLE incidents (
    incident_id        INTEGER PRIMARY KEY,
    company_id         INTEGER NOT NULL,
    project_id         INTEGER NOT NULL,
    division_id        INTEGER NOT NULL,
    employee_id        INTEGER NOT NULL,
    incident_type_id   INTEGER NOT NULL,
    severity_id        INTEGER NOT NULL,
    incident_datetime  TEXT,
    location           TEXT,
    reported_by        TEXT,
    description        TEXT,
    report_datetime    TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (division_id) REFERENCES divisions(division_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (incident_type_id) REFERENCES incident_types(type_id),
    FOREIGN KEY (severity_id) REFERENCES severity_levels(severity_id)
);

-- Seed Companies
INSERT INTO companies (company_id, name) VALUES
(1, 'Active Inferno'),
(2, 'American Gear');

-- Seed Projects
INSERT INTO projects (project_id, company_id, project_name) VALUES
(1, 1, 'Offshore Rig Alpha'),
(2, 1, 'Refinery West'),
(3, 2, 'Mine 21'),
(4, 2, 'Gear Plant South');

-- Seed Divisions
INSERT INTO divisions (division_id, company_id, division_name) VALUES
(1, 1, 'Drilling Ops'),
(2, 1, 'Maintenance'),
(3, 2, 'Assembly Line'),
(4, 2, 'Site Safety');

-- Seed Incident Types
INSERT INTO incident_types (type_id, type_name) VALUES
(1, 'Fall'),
(2, 'Equipment Failure'),
(3, 'Fire'),
(4, 'Electrical Shock'),
(5, 'Chemical Exposure');

-- Seed Severity Levels
INSERT INTO severity_levels (severity_id, label) VALUES
(1, 'Minor'),
(2, 'Major'),
(3, 'Fatal');
