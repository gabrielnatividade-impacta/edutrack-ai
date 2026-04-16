table subjects {
  schema {
    uuid id
    text name
    text? code
    text? description
    text status?="active"
    uuid user_id {
      table = "user"
    }
    uuid? account_id {
      table = "account"
    }
    timestamp created_at?=now
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
}