query "subjects" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text name?
    text code?
    text description?
    enum status? {
      values = ["active", "archived"]
    }
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to edit this subject."
    }

    db.edit subject {
      field_name = "id"
      field_value = $input.subject_id
      data = {
        name        : $input.name,
        code        : $input.code,
        description : $input.description,
        status      : $input.status,
        updated_at  : "now"
      }
    } as $updated_subject

    response = $updated_subject
  }

  tags = ["xano:quick-start"]
}