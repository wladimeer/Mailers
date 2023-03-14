from ..database import get_database

def create(address, subject, content):
  try:
    database, cursor = get_database()

    query = f'insert into email values(null, "{address}", "{subject}", "{content}")'
    cursor.execute(query)
    database.commit()

  except Exception:
    return False
  
  return True

def read():
  _, cursor = get_database()

  query = 'select * from email'
  cursor.execute(query)

  return cursor.fetchall()

def update(id, subject, content):
  database, cursor = get_database()

  query = f'select * from email where id = {id}'
  cursor.execute(query)

  if cursor:
    to_add = ''

    if subject is not None and len(to_add) == 0:
      query += f' subject =  "{subject}"'
    elif subject is not None and len(to_add) > 0:
      query += f', subject =  "{subject}"'

    if content is not None and len(to_add) == 0:
      query += f' content =  "{content}"'
    if content is not None and len(to_add) > 0:
      query += f', content =  "{content}"'

    query = f'update from email set {to_add} where id = {id}'
    cursor.execute(query)
    database.commit()

    return cursor.id
  
def delete(id):
  database, cursor = get_database()

  query = f'select * from email where id = {id}'
  cursor.execute(query)

  if cursor:
    email = cursor.fetchone()

    query = f'delete from email where id = {id}'
    cursor.execute(query)
    database.commit()

    return email

def find_by_content(content):
  _, cursor = get_database()

  query = f'select * from email where content like "%{content}%"'
  cursor.execute(query)

  return cursor.fetchall()