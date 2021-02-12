from datetime import datetime
from users.models import User




now = datetime.now()
current = User.objects.get(username='admin')
diff = now - current.modified_at

print(diff)