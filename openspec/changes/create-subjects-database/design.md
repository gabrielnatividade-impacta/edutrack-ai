# Design: Subjects Database

This document outlines the technical design for implementing the subjects database table and connecting it to the API.

## Table Schema

A new table named `subject` will be created with the following schema:

- `id`: (int, primary key)
- `created_at`: (timestamp)
- `name`: (text)
- `code`: (text, optional)
- `description`: (text, optional)
- `status`: (enum: "active", "archived")
- `user_id`: (int, foreign key to `user` table)
- `account_id`: (int, foreign key to `account` table)

The table definition will be in `tables/753301_subject.xs`.

## API Modifications

The existing `subjects` API endpoints will be modified to use the new `subject` table.

- **`POST /subjects`**: The `db.add ""` command will be changed to `db.add "subject"`.
- **`GET /subjects/{subject_id}`**: The `db.query ""` command will be changed to `db.query "subject"`.
- **`GET /subjects` and `PATCH /subjects`**: These endpoints already correctly reference the `subject` table and require no changes.
