from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections import Counter

Base = declarative_base()


class Band(Base):
    __tablename__ = "bands"
    bandID = Column(Integer, primary_key=True)
    name = Column(String)
    hometown = Column(String)

    # Relationship to Concert
    concerts = relationship("Concert", back_populates="band")

    def __init__(self, name, hometown):
        self.name = name
        self.hometown = hometown

    # Return a list of concerts that the band has played
    def concerts(self):
        return self.concerts

    # Return a list of distinct venues where the band has performed
    def venues(self):
        return list({concert.venue for concert in self.concerts})

    # Return a list of introductions for all the concerts the band has played
    def all_introductions(self):
        introductions = []
        for concert in self.concerts:
            intro = f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}"
            introductions.append(intro)
        return introductions

    # Class method to find the band with the most concerts
    @classmethod
    def most_performances(cls, session):
        bands = session.query(cls).all()
        return max(bands, key=lambda band: len(band.concerts))


class Venue(Base):
    __tablename__ = "venues"
    venueID = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    # Relationship to Concert
    concerts = relationship("Concert", back_populates="venue")

    def __init__(self, title, city):
        self.title = title
        self.city = city

    # Return a list of all he concerts for the venue
    def concerts(self):
        return self.concerts

    # Return a list of bands that have performed at the venue
    def bands(self):
        return [concert.band for concert in self.concerts]

    # Creates a new concert for the band in the specified venue on the given date
    def play_in_venue(self, venue, date):
        # Creates a new Concert instance
        concert = Concert(bandID=self.bandID, venueID=venue.venueID, date=date)

    # returns the first concert on the given date at this venue
    def concert_on(self, date):
        return next(
            (concert for concert in self.concerts if concert.date == date), None
        )

    # Finds the band that has played the most concerts at this venue
    def most_frequent_band(self):
        bands = [concert.band for concert in self.concerts]
        if bands:
            band_count = Counter(bands)
            most_frequent_band = band_count.most_common(1)[0][0]
            return most_frequent_band
        return None


class Concert(Base):
    __tablename__ = "concerts"
    concertID = Column(Integer, primary_key=True)
    bandID = Column(Integer, ForeignKey("bands.bandID"))
    venueID = Column(Integer, ForeignKey("venues.venueID"))
    date = Column(String)

    # Relationships to Band and Venue
    band = relationship("Band", back_populates="concerts")
    venue = relationship("Venue", back_populates="concerts")

    def __init__(self, date):
        self.date = date

    # band instance for this concert
    def band(self):
        return self.band

    # venue instance for this concert
    def venue(self):
        return self.venue

    # Check if the concert is in the band's hometown
    def hometown_show(self):
        return self.band.hometown == self.venue.city

    # Return the introduction string
    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
