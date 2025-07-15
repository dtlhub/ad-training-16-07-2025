from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum, literal_column, func, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

db = SQLAlchemy()

class UserType:
    MAGIC = 'Magic'
    MELEE = 'Melee'
    TYPES = (MAGIC, MELEE)


class User(db.Model):
    __tablename__ = 'users'

    id:            Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username:      Mapped[str]             = mapped_column(String(100), unique=True)
    password:      Mapped[str]             = mapped_column(String(100))
    secret_answer: Mapped[str]             = mapped_column(String, nullable=True)
    created_at:    Mapped[DateTime]        = mapped_column(DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return f'<User {self.username}>'
        
class Character(db.Model):
    __tablename__ = 'characters'
    id:         Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id:   Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    name:       Mapped[str]         = mapped_column(String(100))
    spells:     Mapped[list[int]]   = mapped_column(ARRAY(Integer), nullable=True, default=list, server_default='{}')
    xp:         Mapped[int]         = mapped_column(Integer)
    type:       Mapped[str]         = mapped_column(Enum(*UserType.TYPES, name='user_type'))
    inventory:  Mapped[list[int]]   = mapped_column(ARRAY(Integer), nullable=True, default=list, server_default='{}')
    wins:       Mapped[int]         = mapped_column(Integer, nullable=True)
    loses:      Mapped[int]         = mapped_column(Integer, nullable=True)
    image_url:  Mapped[str]         = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return f'<Character {self.name}>\n XP:  {self.xp}\n HP:  {self.hp}\n OID: {self.owner_id}\n'
    
    def filter_chars(column='wins', order='desc'):
        if not column or column == '':
            column = 'wins'
        if order == 'asc':
            return db.session.query(Character).order_by(literal_column(column)).all()
        else:
            return db.session.query(Character).order_by(literal_column(column).desc()).all()
    
    def create_character(owner_id, name, xp, char_type, inventory=[], image_url=None, spells=[]):
        if inventory is None:
            inventory = []

        character = Character(
            owner_id=owner_id,
            name=name,
            xp=xp,
            type=char_type,
            inventory=inventory,
            image_url=image_url,
            spells=spells,
            wins=0,
            loses=0
            
        )
        db.session.add(character)
        db.session.commit()
        return character