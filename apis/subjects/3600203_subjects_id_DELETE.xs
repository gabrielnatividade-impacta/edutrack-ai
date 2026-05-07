// Delete a subject only if the authenticated user owns it.
query "subjects/{id}" verb=DELETE {
  api_group = "F-5n_QXm"
  auth = "user"

  input {
    uuid id
  }

  stack {
    db.get subjects {
      field = "id"
      value = $input.id
      output = ["id", "user_id"]
    } as $subject

    if ($subject.user_id != $auth.id) {
      error("accessdenied", "You do not have permission to delete this subject.")
    }

    db.delete subjects {
      field = "id"
      value = $input.id
    } as $deleted_subject
  }

  response = {deleted: $deleted_subject}
  tags = ["xano:quick-start"]
}
