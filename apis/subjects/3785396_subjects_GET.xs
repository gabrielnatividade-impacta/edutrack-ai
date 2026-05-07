query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    enum status? {
      values = ["active", "archived"]
    }
  }

  stack {
    db.query subject {
      where = `user_id == $auth.id` == true
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  tags = ["xano:quick-start"]
}