// Get one subject by ID, ensuring ownership
query "subjects/{subject_id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
  }

  stack {
    db.query subject {
      where = $db.subject.id == $input.subject_id && $db.subject.user_id == $auth.id
      return = {type: "single"}
    } as $subject
  }

  response = $subject
  tags = ["xano:quick-start"]
}