# feature-notas-atividades Specification

## Purpose
Define the database structure and API endpoints for managing activity grades in EduTrack AI, allowing professors to assign grades to students for specific activities with proper access controls.

## ADDED Requirements

### Requirement: Store activity grades
The system SHALL store grades assigned by professors to students for specific activities.

#### Scenario: Professor assigns grade
- **WHEN** professor assigns a grade to a student for an activity
- **THEN** system stores the grade with activity, student, and professor references

### Requirement: Associate grades with activities and users
The system SHALL associate each grade with an activity and a student user.

#### Scenario: Grade linked to activity and student
- **WHEN** grade is created
- **THEN** it references valid activity and student IDs

### Requirement: Control access for grade management
The system SHALL allow only the professor who owns the activity's subject to create, edit, or view grades for that activity.

#### Scenario: Unauthorized access blocked
- **WHEN** user tries to manage grades for activity they don't own
- **THEN** system denies access with error

### Requirement: Allow students to view their grades
The system SHALL allow students to view their own grades for activities.

#### Scenario: Student views own grades
- **WHEN** student requests their grades
- **THEN** system returns only grades for that student