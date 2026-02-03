from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()



favorite_characters = Table(
    "favorite_characters",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorite_locations = Table(
    "favorite_locations",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True),
)



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    character_like: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorite_characters,
        back_populates="users"
    )

    location_like: Mapped[list["Location"]] = relationship(
        "Location",
        secondary=favorite_locations,
        back_populates="users"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,}
    
    def serialize_favorite(self):
            return{
            "favorite_characters": [character.serialize() for character in self.character_like],
            "favorite_locations": [location.serialize() for location in self.location_like]
                 
            }
    

        



class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    quote: Mapped[str] = mapped_column(String(180))

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_characters,
        back_populates="character_like"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "quote": self.quote
        }



class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    use: Mapped[str] = mapped_column(String(180) )
    image: Mapped[str] = mapped_column(String(250), nullable=False)
    town: Mapped[str] = mapped_column(String(180), nullable=False)

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_locations,
        back_populates="location_like"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "town": self.town
        }
