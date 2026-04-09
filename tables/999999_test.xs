table test {
  auth = false

  schema {
    int id
    text name
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}