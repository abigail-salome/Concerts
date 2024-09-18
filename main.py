from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Band,
    Venue,
    Concert,
    Base,
)


db = "sqlite:///concerts.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def main():

    session.query(Concert).delete()
    session.query(Band).delete()
    session.query(Venue).delete()
    session.commit()


def delete_concert(concert_id):
    # Query for the concert with the given ID
    concert = session.query(Concert).filter_by(concertID=concert_id).first()

    if concert:
        # Remove the concert from the session
        session.delete(concert)
        # Commit the changes to the database
        session.commit()
        print(f"Concert with ID {concert_id} has been deleted.")
    else:
        print(f"No concert found with ID {concert_id}.")


if __name__ == "__main__":
    main()


# Example usage: delete the concert with ID 2
delete_concert(2)
session.commit()

# Creates a Band instance
band1 = Band(name="The Rolling Stones", hometown="London")
session.add(band1)

# Creates a Venue instance
venue1 = Venue(title="O2 Arena", city="London")
session.add(venue1)

# Creates a Concert instance
concert1 = band1.play_in_venue(venue1, "2024-12-15")

# Queries the band to see if the data was inserted correctly
first_band = session.query(Band).first()
print(f"Band: {first_band.name}, Hometown: {first_band.hometown}")

# Queries the venue to see if the data was inserted correctly
first_venue = session.query(Venue).first()
print(f"Venue: {first_venue.title}, City: {first_venue.city}")

# Gets the concert introductions for the band
introductions = first_band.all_introductions()
print("\nBand Introductions")

# introductions for the band
introductions = band1.all_introductions()
print("\nBand Introductions:")
for intro in introductions:
    print(intro)

# Finds the band with the most performances
top_band = Band.most_performances(session)
print(f"The band with the most performances is: {top_band.name}")

# Find sthe most frequent band at the venue
most_frequent_band = venue1.most_frequent_band()
if most_frequent_band:
    print(f"The most frequent band at {venue1.title} is {most_frequent_band.name}.")
else:
    print(f"No bands have played at {venue1.title}.")
