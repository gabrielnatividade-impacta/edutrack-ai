# Proposal: Create Subjects Database

This change introduces a new database table for `subjects` to allow users to manage their academic disciplines.

## Motivation

The application needs a way to store and manage subjects for each user. This is a foundational feature for tracking academic progress.

## Goals

- Create a `subject` table in the database.
- Ensure subjects are owned by users.
- Connect the existing `subjects` API endpoints to this new table.

## Non-goals

- This change does not include a user interface for managing subjects.
