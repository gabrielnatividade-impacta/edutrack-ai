// Create a new subject for the authenticated user.
query subjects verb=POST {
  api_group = "F-5n_QXm"
  auth = "user"

  input {
    // Name of the subject
    text name
  
    // Optional subject code
    text? code
  
    // Subject description
    text? description
  
    // Subject status
    text? status
  }

  stack {
    db.add subjects {
      data = {
        name       : $input.name
        code       : $input.code
        description: $input.description
        status     : $input.status
        user_id    : $auth.id
      }
    } as $subject
  }

  response = $subject
  tags = ["xano:quick-start"]
}