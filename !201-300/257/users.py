def get_users(passwd: str) -> dict:
    """Split password output by newline,
      extract user and name (1st and 5th columns),
      strip trailing commas from name,
      replace multiple commas in name with a single space
      return dict of keys = user, values = name.
    """
    res = {}
    for line in passwd.splitlines(keepends=False):
        if line and len(line) > 0:
            parts = line.split(':')
            user, name = parts[0], parts[4] or 'unknown'
            res[user] = ' '.join([s for s in (name.strip(',').replace(',', ' ')).split(' ') if len(s) > 0])
    return res
