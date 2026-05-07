// Update a subject only if the authenticated user owns it.
query "subjects/{id}" verb=PATCH {
  api_group = "F-5n_QXm"
  auth = "user"

  input {
    // Subject ID
    uuid id
  
    // Updated subject name
    text? name
  
    // Updated subject code
    text? code
  
    // Updated subject description
    text? description
  
    // Updated subject status
    text? status
  }

  stack {
    db.get subjects {
      field = "id"
      value = $input.id
      output = ["id", "user_id"]
    } as $subject
  
    if ($subject.user_id != $auth.id) {
      error("accessdenied", "You do not have permission to update this subject.")
    }
  
    util.get_all_input as $updates
    db.patch subjects {
      field = "id"
      value = $input.id
      data = $updates
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["xano:quick-start"]
}