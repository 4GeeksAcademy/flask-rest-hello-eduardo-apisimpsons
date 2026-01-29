from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites = Table(
    "favorites_table",
    db.metadata,
    Column("location_id", ForeignKey("location.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"),primary_key=True),
    Column("user_id", ForeignKey("user.id"),primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    character_like:Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorites,
        back_populates="character_"
        
    )
    location_like:Mapped[list["Location"]] = relationship(
        "Location",
        secondary=favorites,
        back_populates="location_"
        
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(180), unique=True, nullable=False)
    use: Mapped[str]= mapped_column(String(180), nullable=False)
    image: Mapped[str]= mapped_column(String(250), nullable=False)
    town: Mapped[str]= mapped_column(String(180), nullable=False)
    location_:Mapped[list[User]]=relationship(
        "User",
        secondary=favorites,
        back_populates= "location_like"
    )

    def serialize(self):
        return{
        }
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    quote: Mapped[str]= mapped_column(String(180), nullable=False)
    image: Mapped[str]= mapped_column(String(250), nullable=False)
    name: Mapped[str]= mapped_column(String(250), nullable=False)
    character_: Mapped[list[User]]=relationship(
        "User",
        secondary=favorites,
        back_populates="character_like"     
    )
    def serialize(self):
        return{
        }