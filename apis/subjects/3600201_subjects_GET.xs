// List subjects owned by the authenticated user.
query subjects verb=GET {
  api_group = "F-5n_QXm"
  auth = "user"

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  tags = ["xano:quick-start"]
}