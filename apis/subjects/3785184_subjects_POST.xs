// Create a new subject for the authenticated user
query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name
    text code?
    text description?
    enum status? {
      values = ["active", "archived"]
    }
  }

  stack {
    db.add subject {
      data = {
        name       : $input.name
        code       : $input.code
        description: $input.description
        status     : $input.status ? $input.status : "active"
        user_id    : $auth.id
        account_id : $auth.account_id
        created_at : "now"
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["xano:quick-start"]
}