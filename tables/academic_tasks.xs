table academic_tasks {
id = uuid {
primary_key = true
}
title = text {
description = "Title of the task"
}
description = text {
description = "Description of the task"
}
due_date = date {
description = "Due date"
}
status = text {
description = "Status of the task"
default = "pending"
}
subject_id = uuid {
references = subjects.id
description = "Reference to subject"
}
user_id = uuid {
references = users.id
description = "User who owns the task"
}
created_at = timestamp {
default = now()
}
updated_at = timestamp {
default = now()
}
}