         
table academic_tasks {
  auth = false

  schema {
    uuid id

    timestamp created_at?=now {
      visibility = "private"
    }

    timestamp updated_at?=now {
      visibility = "private"
    }

    // Task title
    text title filters=trim

    // Task description
    text description? filters=trim

    // Due date
    date due_date?

    // Task status
    text status?="pending"

    // Related subject
    uuid subject_id?

    // Owner user
    uuid user_id?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["xano:quick-start"]
}