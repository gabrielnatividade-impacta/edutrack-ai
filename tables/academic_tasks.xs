table academic_tasks {
  schema {
    uuid id
    text title
    text description
    date due_date
    text status?="pending"
    uuid subject_id {
      table = "subjects"
    }
    uuid user_id {
      table = "user"
    }
    timestamp created_at?=now
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]
}