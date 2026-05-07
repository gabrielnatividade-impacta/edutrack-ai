// Update a subject only if the authenticated user owns it.
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
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
    db.get "" {
      field_name = "id"
      field_value = $input.id
      output = ["id", "user_id"]
    } as $subject
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to update this subject."
    }
  
    util.get_all_input as $updates
    db.patch "" {
      field_name = "id"
      field_value = $input.id
      data = $updates|filter_empty_text:""
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["xano:quick-start"]
}