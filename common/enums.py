import enum

class Category(enum.Enum):
   GAMES = 'GAMES'
   SPORTS = 'SPORTS'
   CLOTHING = 'CLOTHING'
   ELECTRONICS = 'ELECTRONICS'

class Role(enum.Enum):
   ADMIN = 'ADMIN'
   USER = 'USER'