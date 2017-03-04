from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, User, Artist, Album, Track
 
engine = create_engine('postgresql+psycopg2://catalog:udacity@localhost/mitunes')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

# User

user1 = User(name='User', id=1, email='david.sheard@hotmail.com')
session.add(user1)
session.commit()

# Artists

artist1 = Artist(name = 'The Afterparty', id = 1, user_id =  1, image =  'https://scontent-lhr3-1.xx.fbcdn.net/v/t1.0-9/10455424_10152853315166825_602796555442209128_n.jpg?oh=7cca7e89359c64fe8288d97822c36654&oe=591E0E14')
session.add(artist1)
session.commit()

artist2 = Artist(name = 'Manchester Orchestra', id = 2, user_id =  1, image =  'http://www.billboard.com/files/styles/article_main_image/public/media/manchester-orchestra-andrewthomaslee-650-430.jpg')
session.add(artist2)
session.commit()

artist3 = Artist(name = 'Brand New', id = 3, user_id =  1, image =  'http://www.dreamast.com/wp-content/uploads/2016/01/1868x1500.jpg')
session.add(artist3)
session.commit()

artist4 = Artist(name = 'letlive.', id = 4, user_id =  1, image =  'http://epitaph.com/media/artists/letlive_MegaImage_kZWFHtn.jpg.600x375_q90.jpg')
session.add(artist4)
session.commit()


# Albums

album1 = Album(user_id = 1, name = 'Distances', id = 1, artist = 'The Afterparty', year = '2014', artist_id = 1, artwork = 'http://www.hitthefloor.com/wp-content/uploads/2014/03/PDGIQ4FT.jpeg')
session.add(album1)
session.commit()

album2 = Album(user_id = 1, name = 'Hope', id = 2, artist = 'Manchester Orchestra', year = '2014', artist_id = 2, artwork = 'https://upload.wikimedia.org/wikipedia/en/b/bf/Manchester_Orchestra_Hope.png')
session.add(album2)
session.commit()

album3 = Album(user_id = 1, name = 'Cope', id = 3, artist = 'Manchester Orchestra', year = '2014', artist_id = 2, artwork = 'http://cdn4.pitchfork.com/albums/20352/homepage_large.cc98c6af.jpg')
session.add(album3)
session.commit()

album4 = Album(user_id = 1, name = 'Daisy', id = 4, artist = 'Brand New', year = '2009', artist_id = 3, artwork = 'https://s3.amazonaws.com/rapgenius/brandnew.jpg')
session.add(album4)
session.commit()

album5 = Album(user_id = 1, name = 'The Devil and God Are Raging Inside Me', id = 5, artist = 'Brand New', year = '2006', artist_id = 3, artwork = 'https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/Thedevilandgodareraginginsideme.jpg/220px-Thedevilandgodareraginginsideme.jpg')
session.add(album5)
session.commit()

album6 = Album(user_id = 1, name = "If I'm The Devil", id = 6, artist = 'letlive.', year = '2016', artist_id = 4, artwork = 'http://epitaph.com/media/releases/0045778739264.png')
session.add(album6)
session.commit()

album7 = Album(user_id = 1, name = 'Deja Entendu', id = 7, artist = 'Brand New', year = '2003', artist_id = 3, artwork = 'https://upload.wikimedia.org/wikipedia/en/7/7b/Brand_New_Deja_Entendu.jpg')
session.add(album7)
session.commit()

# Tracks

track1 = Track(user_id = 1, name = 'Lost Cause', id = 1, artist = 'The Afterparty', album = 'Distances', num = 1, artist_id = 1, album_id = 1)
session.add(track1)
session.commit()

track2 = Track(user_id = 1, name = 'Cover Up', id = 2, artist = 'The Afterparty', album = 'Distances', num = 2, artist_id = 1, album_id = 1)
session.add(track2)
session.commit()

track3 = Track(user_id = 1, name = 'Open Road', id = 3, artist = 'The Afterparty', album = 'Distances', num = 3, artist_id = 1, album_id = 1)
session.add(track3)
session.commit()

track4 = Track(user_id = 1, name = 'Liar Liar', id = 4, artist = 'The Afterparty', album = 'Distances', num = 4, artist_id = 1, album_id = 1)
session.add(track4)
session.commit()

track5 = Track(user_id = 1, name = 'When The Lights Go Out', id = 5, artist = 'The Afterparty', album = 'Distances', num = 5, artist_id = 1, album_id = 1)
session.add(track5)
session.commit()

track6 = Track(user_id = 1, name = 'Within The Looking Glass', id = 6, artist = 'The Afterparty', album = 'Distances', num = 6, artist_id = 1, album_id = 1)
session.add(track6)
session.commit()



track7 = Track(user_id = 1, name = 'Top Notch', id = 7, artist = 'Manchester Orchestra', album = 'Hope', num = 1, artist_id = 2, album_id = 2)
session.add(track7)
session.commit()

track8 = Track(user_id = 1, name = 'Choose You', id = 8, artist = 'Manchester Orchestra', album = 'Hope', num = 2, artist_id = 2, album_id = 2)
session.add(track8)
session.commit()

track9 = Track(user_id = 1, name = 'Girl Harbor', id = 9, artist = 'Manchester Orchestra', album = 'Hope', num = 3, artist_id = 2, album_id = 2)
session.add(track9)
session.commit()

track10 = Track(user_id = 1, name = 'The Mansion', id = 10, artist = 'Manchester Orchestra', album = 'Hope', num = 4, artist_id = 2, album_id = 2)
session.add(track10)
session.commit()

track11 = Track(user_id = 1, name = 'The Ocean', id = 11, artist = 'Manchester Orchestra', album = 'Hope', num = 5, artist_id = 2, album_id = 2)
session.add(track11)
session.commit()

track12 = Track(user_id = 1, name = 'Every Stone', id = 12, artist = 'Manchester Orchestra', album = 'Hope', num = 6, artist_id = 2, album_id = 2)
session.add(track12)
session.commit()

track13 = Track(user_id = 1, name = 'All That I Really Wanted', id = 13, artist = 'Manchester Orchestra', album = 'Hope', num = 7, artist_id = 2, album_id = 2)
session.add(track13)
session.commit()

track14 = Track(user_id = 1, name = 'Trees', id = 14, artist = 'Manchester Orchestra', album = 'Hope', num = 8, artist_id = 2, album_id = 2)
session.add(track14)
session.commit()

track15 = Track(user_id = 1, name = 'Indentions', id = 15, artist = 'Manchester Orchestra', album = 'Hope', num = 9, artist_id = 2, album_id = 2)
session.add(track15)
session.commit()

track16 = Track(user_id = 1, name = 'See It Again', id = 16, artist = 'Manchester Orchestra', album = 'Hope', num = 10, artist_id = 2, album_id = 2)
session.add(track16)
session.commit()

track17 = Track(user_id = 1, name = 'Cope', id = 17, artist = 'Manchester Orchestra', album = 'Hope', num = 11, artist_id = 2, album_id = 2)
session.add(track17)
session.commit()



track18 = Track(user_id = 1, name = 'Top Notch', id = 18, artist = 'Manchester Orchestra', album = 'Cope', num = 1, artist_id = 2, album_id = 3)
session.add(track18)
session.commit()

track19 = Track(user_id = 1, name = 'Choose You', id = 19, artist = 'Manchester Orchestra', album = 'Cope', num = 2, artist_id = 2, album_id = 3)
session.add(track19)
session.commit()

track20 = Track(user_id = 1, name = 'Girl Harbor', id = 20, artist = 'Manchester Orchestra', album = 'Cope', num = 3, artist_id = 2, album_id = 3)
session.add(track20)
session.commit()

track21 = Track(user_id = 1, name = 'The Mansion', id = 21, artist = 'Manchester Orchestra', album = 'HCpe', num = 4, artist_id = 2, album_id = 3)
session.add(track21)
session.commit()

track22 = Track(user_id = 1, name = 'The Ocean', id = 22, artist = 'Manchester Orchestra', album = 'Cope', num = 5, artist_id = 2, album_id = 3)
session.add(track22)
session.commit()

track23 = Track(user_id = 1, name = 'Every Stone', id = 23, artist = 'Manchester Orchestra', album = 'Cope', num = 6, artist_id = 2, album_id = 3)
session.add(track23)
session.commit()

track24 = Track(user_id = 1, name = 'All That I Really Wanted', id = 24, artist = 'Manchester Orchestra', album = 'Cope', num = 7, artist_id = 2, album_id = 3)
session.add(track24)
session.commit()

track25 = Track(user_id = 1, name = 'Trees', id = 25, artist = 'Manchester Orchestra', album = 'Cope', num = 8, artist_id = 2, album_id = 3)
session.add(track25)
session.commit()

track26 = Track(user_id = 1, name = 'Indentions', id = 26, artist = 'Manchester Orchestra', album = 'Cope', num = 9, artist_id = 2, album_id = 3)
session.add(track26)
session.commit()

track27 = Track(user_id = 1, name = 'See It Again', id = 27, artist = 'Manchester Orchestra', album = 'Cope', num = 10, artist_id = 2, album_id = 3)
session.add(track27)
session.commit()

track28 = Track(user_id = 1, name = 'Cope', id = 28, artist = 'Manchester Orchestra', album = 'Cope', num = 11, artist_id = 2, album_id = 3)
session.add(track28)
session.commit()



track29 = Track(user_id = 1, name = 'Vices', id = 29, artist = 'Brand New', album = 'Daisy', num = 1, artist_id = 3, album_id = 4)
session.add(track29)
session.commit()

track30 = Track(user_id = 1, name = 'Bed', id = 30, artist = 'Brand New', album = 'Daisy', num = 2, artist_id = 3, album_id = 4)
session.add(track30)
session.commit()

track31 = Track(user_id = 1, name = 'At The Bottom', id = 31, artist = 'Brand New', album = 'Daisy', num = 3, artist_id = 3, album_id = 4)
session.add(track31)
session.commit()

track32 = Track(user_id = 1, name = 'Gasoline', id = 32, artist = 'Brand New', album = 'Daisy', num = 4, artist_id = 3, album_id = 4)
session.add(track32)
session.commit()

track33 = Track(user_id = 1, name = 'You Stole', id = 33, artist = 'Brand New', album = 'Daisy', num = 5, artist_id = 3, album_id = 4)
session.add(track33)
session.commit()

track34 = Track(user_id = 1, name = 'Be Gone', id = 34, artist = 'Brand New', album = 'Daisy', num = 6, artist_id = 3, album_id = 4)
session.add(track34)
session.commit()

track35 = Track(user_id = 1, name = 'Sink', id = 35, artist = 'Brand New', album = 'Daisy', num = 7, artist_id = 3, album_id = 4)
session.add(track35)
session.commit()

track36 = Track(user_id = 1, name = 'Bought A Bride', id = 36, artist = 'Brand New', album = 'Daisy', num = 8, artist_id = 3, album_id = 4)
session.add(track36)
session.commit()

track37 = Track(user_id = 1, name = 'Daisy', id = 37, artist = 'Brand New', album = 'Daisy', num = 9, artist_id = 3, album_id = 4)
session.add(track37)
session.commit()

track38 = Track(user_id = 1, name = 'In A Jar', id = 38, artist = 'Brand New', album = 'Daisy', num = 10, artist_id = 3, album_id = 4)
session.add(track38)
session.commit()

track39 = Track(user_id = 1, name = 'Noro', id = 39, artist = 'Brand New', album = 'Daisy', num = 11, artist_id = 3, album_id = 4)
session.add(track39)
session.commit()

track40 = Track(user_id = 1, name = 'Bed (Live In Studio)', id = 40, artist = 'Brand New', album = 'Daisy', num = 12, artist_id = 3, album_id = 4)
session.add(track40)
session.commit()




track41 = Track(user_id = 1, name = 'Sowing Season', id = 41, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 1, artist_id = 3, album_id = 5)
session.add(track41)
session.commit()

track42 = Track(user_id = 1, name = 'Millstone', id = 42, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 2, artist_id = 3, album_id = 5)
session.add(track42)
session.commit()

track43 = Track(user_id = 1, name = 'Jesus', id = 43, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 3, artist_id = 3, album_id = 5)
session.add(track43)
session.commit()

track44 = Track(user_id = 1, name = 'Degausser', id = 44, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 4, artist_id = 3, album_id = 5)
session.add(track44)
session.commit()

track45 = Track(user_id = 1, name = 'Limousine', id = 45, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 5, artist_id = 3, album_id = 5)
session.add(track45)
session.commit()

track46 = Track(user_id = 1, name = "You Won't Know", id = 46, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 6, artist_id = 3, album_id = 5)
session.add(track46)
session.commit()

track47 = Track(user_id = 1, name = 'Welcome To Bangkok', id = 47, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 7, artist_id = 3, album_id = 5)
session.add(track47)
session.commit()

track48 = Track(user_id = 1, name = 'Not The Sun', id = 48, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 8, artist_id = 3, album_id = 5)
session.add(track48)
session.commit()

track49 = Track(user_id = 1, name = 'Untitled', id = 49, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 9, artist_id = 3, album_id = 5)
session.add(track49)
session.commit()

track50 = Track(user_id = 1, name = 'Luca', id = 50, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 10, artist_id = 3, album_id = 5)
session.add(track50)
session.commit()

track51 = Track(user_id = 1, name = "The Archer's Bows Have Broken", id = 51, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 11, artist_id = 3, album_id = 5)
session.add(track51)
session.commit()

track52 = Track(user_id = 1, name = 'Handcuffs', id = 52, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 12, artist_id = 3, album_id = 5)
session.add(track52)
session.commit()

track53 = Track(user_id = 1, name = 'Luca (reprise)', id = 53, artist = 'Brand New', album = 'The Devil and God Are Raging Inside Me', num = 13, artist_id = 3, album_id = 5)
session.add(track53)
session.commit()



track54 = Track(user_id = 1, name = "I've Learned To Love Myself", id = 54, artist = 'letlive.', album = "If I'm The Devil", num = 1, artist_id = 4, album_id = 6)
session.add(track54)
session.commit()

track55 = Track(user_id = 1, name = 'Nu Romantics', id = 55, artist = 'letlive.', album = "If I'm The Devil", num = 2, artist_id = 4, album_id = 6)
session.add(track55)
session.commit()

track56 = Track(user_id = 1, name = 'Good Mourning, America', id = 56, artist = 'letlive.', album = "If I'm The Devil", num = 3, artist_id = 4, album_id = 6)
session.add(track56)
session.commit()

track57 = Track(user_id = 1, name = 'Who You Are Not', id = 57, artist = 'letlive.', album = "If I'm The Devil", num = 4, artist_id = 4, album_id = 6)
session.add(track57)
session.commit()

track58 = Track(user_id = 1, name = 'A Weak Ago', id = 58, artist = 'letlive.', album = "If I'm The Devil", num = 5, artist_id = 4, album_id = 6)
session.add(track58)
session.commit()

track59 = Track(user_id = 1, name = "Foreign Cab Rides", id = 59, artist = 'letlive.', album = "If I'm The Devil", num = 6, artist_id = 4, album_id = 6)
session.add(track59)
session.commit()

track60 = Track(user_id = 1, name = 'Reluctantly Dead', id = 60, artist = 'letlive.', album = "If I'm The Devil", num = 7, artist_id = 4, album_id = 6)
session.add(track60)
session.commit()

track61 = Track(user_id = 1, name = 'Elephant', id = 61, artist = 'letlive.', album = "If I'm The Devil", num = 8, artist_id = 4, album_id = 6)
session.add(track61)
session.commit()

track62 = Track(user_id = 1, name = 'Another Offensive Song', id = 62, artist = 'letlive.', album = "If I'm The Devil", num = 9, artist_id = 4, album_id = 6)
session.add(track62)
session.commit()

track63 = Track(user_id = 1, name = "If I'm The Devil...", id = 63, artist = 'letlive.', album = "If I'm The Devil", num = 10, artist_id = 4, album_id = 6)
session.add(track63)
session.commit()

track64 = Track(user_id = 1, name = "Copper Coloured Quiet", id = 64, artist = 'letlive.', album = "If I'm The Devil", num = 11, artist_id = 4, album_id = 6)
session.add(track64)
session.commit()




track65 = Track(user_id = 1, name = 'Tautou', id = 65, artist = 'Brand New', album = 'Deja Entendu', num = 1, artist_id = 3, album_id = 7)
session.add(track65)
session.commit()

track66 = Track(user_id = 1, name = 'Sic Transit Gloria... Glory Fades', id = 66, artist = 'Brand New', album = 'Deja Entendu', num = 2, artist_id = 3, album_id = 7)
session.add(track66)
session.commit()

track67 = Track(user_id = 1, name = 'I Will Play My Game Beneath The Spin Light', id = 67, artist = 'Brand New', album = 'Deja Entendu', num = 3, artist_id = 3, album_id = 7)
session.add(track67)
session.commit()

track68 = Track(user_id = 1, name = "Okay I Believe You, But My Tommy Gun Don't", id = 68, artist = 'Brand New', album = 'Deja Entendu', num = 4, artist_id = 3, album_id = 7)
session.add(track68)
session.commit()

track69 = Track(user_id = 1, name = 'The Quiet Things That No One Ever Knows', id = 69, artist = 'Brand New', album = 'Deja Entendu', num = 5, artist_id = 3, album_id = 7)
session.add(track69)
session.commit()

track70 = Track(user_id = 1, name = "The Boy Who Blocked His Own Shot", id = 70, artist = 'Brand New', album = 'Deja Entendu', num = 6, artist_id = 3, album_id = 7)
session.add(track70)
session.commit()

track71 = Track(user_id = 1, name = 'Jaws Theme Swimming', id = 71, artist = 'Brand New', album = 'Deja Entendu', num = 7, artist_id = 3, album_id = 7)
session.add(track71)
session.commit()

track72 = Track(user_id = 1, name = 'Me vs. Maradonna vs. Elvis', id = 72, artist = 'Brand New', album = 'Deja Entendu', num = 8, artist_id = 3, album_id = 7)
session.add(track72)
session.commit()

track73 = Track(user_id = 1, name = 'Guernica', id = 73, artist = 'Brand New', album = 'Deja Entendu', num = 9, artist_id = 3, album_id = 7)
session.add(track73)
session.commit()

track74 = Track(user_id = 1, name = 'Good To Know That If I Ever Need Attention, All I Have To Do Is Die', id = 74, artist = 'Brand New', album = 'Deja Entendu', num = 10, artist_id = 3, album_id = 7)
session.add(track74)
session.commit()

track75 = Track(user_id = 1, name = "Play Crack The Sky", id = 75, artist = 'Brand New', album = 'Deja Entendu', num = 11, artist_id = 3, album_id = 7)
session.add(track75)
session.commit()

print "Populated the db successfully"















