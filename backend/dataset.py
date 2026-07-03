# D:\YASH\Movie_Recommendation_System\backend\dataset.py

MOVIES = [
    # --- SCI-FI / MIND-BENDING ---
    {
        "id": 1,
        "title": "Inception",
        "year": 2010,
        "genres": ["Sci-Fi", "Action", "Thriller"],
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "runtime": 148,
        "language": "English",
        "rating": 8.8,
        "vote_count": 25000,
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "moods": ["Mind-bending", "Action-packed", "Suspenseful"],
        "poster_path": "/oYuLEt3zSjqZJ6u8gi7r2iGtzK3.jpg"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "year": 2014,
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "director": "Christopher Nolan",
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "runtime": 169,
        "language": "English",
        "rating": 8.7,
        "vote_count": 22000,
        "overview": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        "moods": ["Mind-bending", "Emotional", "Inspirational"],
        "poster_path": "/gEU2QvHOm5fgvQZmc3VYpeJUv2e.jpg"
    },
    {
        "id": 3,
        "title": "The Matrix",
        "year": 1999,
        "genres": ["Sci-Fi", "Action"],
        "director": "Lana Wachowski",
        "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        "runtime": 136,
        "language": "English",
        "rating": 8.7,
        "vote_count": 24000,
        "overview": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
        "moods": ["Mind-bending", "Action-packed"],
        "poster_path": "/f89U3wL3mF79o2eam4h5ilPL6c6.jpg"
    },
    {
        "id": 4,
        "title": "Blade Runner 2049",
        "year": 2017,
        "genres": ["Sci-Fi", "Drama", "Mystery"],
        "director": "Denis Villeneuve",
        "cast": ["Ryan Gosling", "Harrison Ford", "Ana de Armas"],
        "runtime": 164,
        "language": "English",
        "rating": 8.0,
        "vote_count": 12000,
        "overview": "A new blade runner, LAPD Officer K, unearths a long-buried secret that has the potential to plunge what's left of society into chaos.",
        "moods": ["Mind-bending", "Relaxing", "Suspenseful"],
        "poster_path": "/gajva2L054k2TYrN6LIzT5i2UHG.jpg"
    },
    {
        "id": 5,
        "title": "Arrival",
        "year": 2016,
        "genres": ["Sci-Fi", "Drama", "Mystery"],
        "director": "Denis Villeneuve",
        "cast": ["Amy Adams", "Jeremy Renner", "Forest Whitaker"],
        "runtime": 116,
        "language": "English",
        "rating": 7.9,
        "vote_count": 16000,
        "overview": "A linguist is recruited by the military to assist in communicating with alien beings who have initiated first contact.",
        "moods": ["Mind-bending", "Emotional", "Suspenseful"],
        "poster_path": "/x2FiwSy46p444vj8S5n64V2661y.jpg"
    },
    {
        "id": 6,
        "title": "Coherence",
        "year": 2013,
        "genres": ["Sci-Fi", "Thriller", "Mystery"],
        "director": "James Ward Byrkit",
        "cast": ["Emily Baldoni", "Maury Sterling", "Nicholas Brendon"],
        "runtime": 89,
        "language": "English",
        "rating": 7.2,
        "vote_count": 1800,  # Hidden Gem candidate!
        "overview": "Strange things begin to happen when a group of friends gather for a dinner party on an evening when a comet is passing overhead.",
        "moods": ["Mind-bending", "Suspenseful"],
        "poster_path": "/l94W9G94fH59j90uI70EAu5Z82Z.jpg"
    },
    {
        "id": 7,
        "title": "Eternal Sunshine of the Spotless Mind",
        "year": 2004,
        "genres": ["Romance", "Sci-Fi", "Drama"],
        "director": "Michel Gondry",
        "cast": ["Jim Carrey", "Kate Winslet", "Kirsten Dunst"],
        "runtime": 108,
        "language": "English",
        "rating": 8.3,
        "vote_count": 13000,
        "overview": "When their relationship turns sour, a young couple undergoes a medical procedure to have each other erased from their memories.",
        "moods": ["Mind-bending", "Emotional", "Romantic"],
        "poster_path": "/54mZ51wBdR69SUJUrlSafeevrj0.jpg"
    },

    # --- ACTION / ADVENTURE ---
    {
        "id": 8,
        "title": "The Dark Knight",
        "year": 2008,
        "genres": ["Action", "Drama", "Thriller"],
        "director": "Christopher Nolan",
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "runtime": 152,
        "language": "English",
        "rating": 9.0,
        "vote_count": 28000,
        "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "moods": ["Action-packed", "Suspenseful"],
        "poster_path": "/qJ2tWGB2YiZ5YwIBQRs3gkSLJ27.jpg"
    },
    {
        "id": 9,
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "genres": ["Action", "Sci-Fi", "Adventure"],
        "director": "George Miller",
        "cast": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
        "runtime": 120,
        "language": "English",
        "rating": 8.1,
        "vote_count": 20000,
        "overview": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.",
        "moods": ["Action-packed"],
        "poster_path": "/8tZYrj3goj5k218ESGbFyIlM8rj.jpg"
    },
    {
        "id": 10,
        "title": "Gladiator",
        "year": 2000,
        "genres": ["Action", "Drama", "Adventure"],
        "director": "Ridley Scott",
        "cast": ["Russell Crowe", "Joaquin Phoenix", "Connie Nielsen"],
        "runtime": 155,
        "language": "English",
        "rating": 8.5,
        "vote_count": 16000,
        "overview": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "moods": ["Action-packed", "Emotional", "Inspirational"],
        "poster_path": "/ty87Lu1YmKMfxchqgQI6xh7GE06.jpg"
    },
    {
        "id": 11,
        "title": "John Wick",
        "year": 2014,
        "genres": ["Action", "Thriller"],
        "director": "Chad Stahelski",
        "cast": ["Keanu Reeves", "Michael Nyqvist", "Alfie Allen"],
        "runtime": 101,
        "language": "English",
        "rating": 7.4,
        "vote_count": 17000,
        "overview": "An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.",
        "moods": ["Action-packed"],
        "poster_path": "/fZPSwx93tMrv4egB3qncl30ge9c.jpg"
    },
    {
        "id": 12,
        "title": "Kill Bill: Vol. 1",
        "year": 2003,
        "genres": ["Action", "Thriller"],
        "director": "Quentin Tarantino",
        "cast": ["Uma Thurman", "Lucy Liu", "Vivica A. Geneca"],
        "runtime": 111,
        "language": "English",
        "rating": 8.2,
        "vote_count": 15000,
        "overview": "After awakening from a four-year coma, a former assassin wreaks vengeance on the team of assassins who betrayed her.",
        "moods": ["Action-packed", "Suspenseful"],
        "poster_path": "/v7TaX8kpaE1XSGw6yp8t648qV05.jpg"
    },

    # --- COMEDY / FEEL-GOOD ---
    {
        "id": 13,
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genres": ["Comedy", "Drama", "Adventure"],
        "director": "Wes Anderson",
        "cast": ["Ralph Fiennes", "F. Murray Abraham", "Mathieu Amalric"],
        "runtime": 99,
        "language": "English",
        "rating": 8.1,
        "vote_count": 13000,
        "overview": "A writer relates his adventures at a renowned European resort hotel between the first and second World Wars with a concierge who is wrongly framed for murder.",
        "moods": ["Funny", "Relaxing", "Inspirational"],
        "poster_path": "/e64sbj7v244r52z3nn3Cc4o8g44.jpg"
    },
    {
        "id": 14,
        "title": "Superbad",
        "year": 2007,
        "genres": ["Comedy"],
        "director": "Greg Mottola",
        "cast": ["Jonah Hill", "Michael Cera", "Christopher Mintz-Plasse"],
        "runtime": 113,
        "language": "English",
        "rating": 7.6,
        "vote_count": 10000,
        "overview": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
        "moods": ["Funny", "Relaxing"],
        "poster_path": "/ek8gzl3n75IFf6nh7kPldC75iZg.jpg"
    },
    {
        "id": 15,
        "title": "Groundhog Day",
        "year": 1993,
        "genres": ["Comedy", "Romance", "Fantasy"],
        "director": "Harold Ramis",
        "cast": ["Bill Murray", "Andie MacDowell", "Chris Elliott"],
        "runtime": 101,
        "language": "English",
        "rating": 8.1,
        "vote_count": 7000,
        "overview": "A narcissistic, self-centered weatherman finds himself inexplicably living the same day over and over again.",
        "moods": ["Funny", "Relaxing", "Inspirational"],
        "poster_path": "/g8a59449xT56v9F38e1G3aG11bU.jpg"
    },
    {
        "id": 16,
        "title": "Knives Out",
        "year": 2019,
        "genres": ["Comedy", "Mystery", "Thriller"],
        "director": "Rian Johnson",
        "cast": ["Daniel Craig", "Chris Evans", "Ana de Armas"],
        "runtime": 130,
        "language": "English",
        "rating": 7.9,
        "vote_count": 15000,
        "overview": "A detective investigates the death of the patriarch of an eccentric, combative family.",
        "moods": ["Funny", "Suspenseful"],
        "poster_path": "/pThyQrqv5Ed41J92Zrfa2Oh40jM.jpg"
    },
    {
        "id": 17,
        "title": "Shaun of the Dead",
        "year": 2004,
        "genres": ["Comedy", "Horror"],
        "director": "Edgar Wright",
        "cast": ["Simon Pegg", "Nick Frost", "Kate Ashfield"],
        "runtime": 99,
        "language": "English",
        "rating": 7.9,
        "vote_count": 8000,
        "overview": "A man's uneventful life is disrupted by the zombie apocalypse, forcing him to rise to the occasion and save his loved ones.",
        "moods": ["Funny", "Spooky"],
        "poster_path": "/x69j7rmO2u4Vlg4724yL1v47C5m.jpg"
    },

    # --- DRAMA / EMOTIONAL ---
    {
        "id": 18,
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genres": ["Drama"],
        "director": "Frank Darabont",
        "cast": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
        "runtime": 142,
        "language": "English",
        "rating": 9.3,
        "vote_count": 26000,
        "overview": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
        "moods": ["Emotional", "Inspirational"],
        "poster_path": "/9cqN025wZIMrW78fVg5ZmHgJ56V.jpg"
    },
    {
        "id": 19,
        "title": "Forrest Gump",
        "year": 1994,
        "genres": ["Drama", "Romance", "Comedy"],
        "director": "Robert Zemeckis",
        "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
        "runtime": 142,
        "language": "English",
        "rating": 8.8,
        "vote_count": 23000,
        "overview": "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.",
        "moods": ["Emotional", "Inspirational", "Funny", "Romantic"],
        "poster_path": "/arw2eeUpqqcWcvclrmAhURs2jXA.jpg"
    },
    {
        "id": 20,
        "title": "Fight Club",
        "year": 1999,
        "genres": ["Drama", "Thriller"],
        "director": "David Fincher",
        "cast": ["Brad Pitt", "Edward Norton", "Meat Loaf"],
        "runtime": 139,
        "language": "English",
        "rating": 8.8,
        "vote_count": 26000,
        "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "moods": ["Mind-bending", "Action-packed", "Suspenseful"],
        "poster_path": "/pB8Z4j2nBky8PQK53wV55u53tq7.jpg"
    },
    {
        "id": 21,
        "title": "Whiplash",
        "year": 2014,
        "genres": ["Drama", "Music"],
        "director": "Damien Chazelle",
        "cast": ["Miles Teller", "J.K. Simmons", "Paul Reiser"],
        "runtime": 106,
        "language": "English",
        "rating": 8.5,
        "vote_count": 14000,
        "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
        "moods": ["Inspirational", "Emotional", "Suspenseful"],
        "poster_path": "/7yyN12wlubrR6QQt4u0704XBr9o.jpg"
    },
    {
        "id": 22,
        "title": "The Godfather",
        "year": 1972,
        "genres": ["Drama", "Crime"],
        "director": "Francis Ford Coppola",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "runtime": 175,
        "language": "English",
        "rating": 9.2,
        "vote_count": 19000,
        "overview": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.",
        "moods": ["Emotional", "Suspenseful"],
        "poster_path": "/3bhkrj6PMMn799icGR7y2fGsC45.jpg"
    },

    # --- ROMANCE / RELATIONSHIPS ---
    {
        "id": 23,
        "title": "La La Land",
        "year": 2016,
        "genres": ["Romance", "Music", "Drama", "Comedy"],
        "director": "Damien Chazelle",
        "cast": ["Ryan Gosling", "Emma Stone", "John Legend"],
        "runtime": 128,
        "language": "English",
        "rating": 8.0,
        "vote_count": 15000,
        "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
        "moods": ["Romantic", "Emotional", "Relaxing", "Inspirational"],
        "poster_path": "/uDO8zWDhfNs1FSNy5vqy7qqEPX5.jpg"
    },
    {
        "id": 24,
        "title": "About Time",
        "year": 2013,
        "genres": ["Romance", "Drama", "Fantasy", "Comedy"],
        "director": "Richard Curtis",
        "cast": ["Domhnall Gleeson", "Rachel McAdams", "Bill Nighy"],
        "runtime": 123,
        "language": "English",
        "rating": 7.8,
        "vote_count": 6500,
        "overview": "At the age of 21, Tim discovers he can travel in time and change what happens and has happened in his own life. His decision to make his world a better place by getting a girlfriend turns out not to be as easy as you might think.",
        "moods": ["Romantic", "Emotional", "Relaxing", "Inspirational", "Funny"],
        "poster_path": "/iCeJyJmB209U14sT3Z26l596u0z.jpg"
    },
    {
        "id": 25,
        "title": "Before Sunrise",
        "year": 1995,
        "genres": ["Romance", "Drama"],
        "director": "Richard Linklater",
        "cast": ["Ethan Hawke", "Julie Delpy", "Andrea Eckert"],
        "runtime": 101,
        "language": "English",
        "rating": 8.1,
        "vote_count": 4000,
        "overview": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. However, both know that this will probably be their only night together.",
        "moods": ["Romantic", "Relaxing", "Emotional"],
        "poster_path": "/kh1A4u79k9XJ5d5395X01m4k.jpg"
    },
    {
        "id": 26,
        "title": "Amélie",
        "year": 2001,
        "genres": ["Romance", "Comedy"],
        "director": "Jean-Pierre Jeunet",
        "cast": ["Audrey Tautou", "Mathieu Kassovitz", "Rufus"],
        "runtime": 122,
        "language": "French",
        "rating": 8.3,
        "vote_count": 7500,
        "overview": "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, along the way, discovers love.",
        "moods": ["Romantic", "Relaxing", "Funny", "Inspirational"],
        "poster_path": "/d9K7SrrA21johCfjO2qZ6nnEQ7W.jpg"
    },

    # --- THRILLER / MYSTERY / SUSPENSE ---
    {
        "id": 27,
        "title": "Shutter Island",
        "year": 2010,
        "genres": ["Mystery", "Thriller", "Drama"],
        "director": "Martin Scorsese",
        "cast": ["Leonardo DiCaprio", "Mark Ruffalo", "Ben Kingsley"],
        "runtime": 138,
        "language": "English",
        "rating": 8.2,
        "vote_count": 21000,
        "overview": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.",
        "moods": ["Mind-bending", "Suspenseful", "Spooky"],
        "poster_path": "/kveQ0c2N5v5gZ7rFv0kU03pQc1x.jpg"
    },
    {
        "id": 28,
        "title": "Se7en",
        "year": 1995,
        "genres": ["Mystery", "Thriller", "Crime"],
        "director": "David Fincher",
        "cast": ["Morgan Freeman", "Brad Pitt", "Kevin Spacey"],
        "runtime": 127,
        "language": "English",
        "rating": 8.6,
        "vote_count": 19000,
        "overview": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
        "moods": ["Suspenseful", "Spooky"],
        "poster_path": "/69xm4jU5F2r7Y4HCuo2Cxv7v26v.jpg"
    },
    {
        "id": 29,
        "title": "The Prestige",
        "year": 2006,
        "genres": ["Drama", "Mystery", "Sci-Fi"],
        "director": "Christopher Nolan",
        "cast": ["Hugh Jackman", "Christian Bale", "Scarlett Johansson"],
        "runtime": 130,
        "language": "English",
        "rating": 8.5,
        "vote_count": 14000,
        "overview": "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.",
        "moods": ["Mind-bending", "Suspenseful"],
        "poster_path": "/bdN3g140Y7d6OFhJWtQj40a35j3.jpg"
    },
    {
        "id": 30,
        "title": "Memento",
        "year": 2000,
        "genres": ["Mystery", "Thriller"],
        "director": "Christopher Nolan",
        "cast": ["Guy Pearce", "Carrie-Anne Moss", "Joe Pantoliano"],
        "runtime": 113,
        "language": "English",
        "rating": 8.4,
        "vote_count": 8500,
        "overview": "A man with short-term memory loss attempts to track down his wife's murderer.",
        "moods": ["Mind-bending", "Suspenseful"],
        "poster_path": "/fQ3as6w8Ju221nvg867N29y962s.jpg"
    },
    {
        "id": 31,
        "title": "Prisoners",
        "year": 2013,
        "genres": ["Drama", "Mystery", "Thriller"],
        "director": "Denis Villeneuve",
        "cast": ["Hugh Jackman", "Jake Gyllenhaal", "Viola Davis"],
        "runtime": 153,
        "language": "English",
        "rating": 8.1,
        "vote_count": 10000,
        "overview": "When Keller Dover's daughter and her friend go missing, he takes matters into his own hands as the police pursue multiple leads and the pressure mounts.",
        "moods": ["Suspenseful", "Emotional"],
        "poster_path": "/tuJu7a721P1Ico2uB22oV4t6jB6.jpg"
    },

    # --- HORROR / SPOOKY ---
    {
        "id": 32,
        "title": "Get Out",
        "year": 2017,
        "genres": ["Horror", "Mystery", "Thriller"],
        "director": "Jordan Peele",
        "cast": ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
        "runtime": 104,
        "language": "English",
        "rating": 7.7,
        "vote_count": 15000,
        "overview": "A young Afro-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception eventually reaches a boiling point.",
        "moods": ["Spooky", "Suspenseful", "Mind-bending"],
        "poster_path": "/1E5o570s414h15tVejq0t124uOI.jpg"
    },
    {
        "id": 33,
        "title": "Hereditary",
        "year": 2018,
        "genres": ["Horror", "Mystery", "Drama"],
        "director": "Ari Aster",
        "cast": ["Toni Collette", "Milly Shapiro", "Alex Wolff"],
        "runtime": 127,
        "language": "English",
        "rating": 7.3,
        "vote_count": 6800,
        "overview": "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother.",
        "moods": ["Spooky", "Emotional", "Suspenseful"],
        "poster_path": "/db8ui382w5jRrm6Un7m4W7vjQKi.jpg"
    },
    {
        "id": 34,
        "title": "The Conjuring",
        "year": 2013,
        "genres": ["Horror", "Thriller"],
        "director": "James Wan",
        "cast": ["Vera Farmiga", "Patrick Wilson", "Lili Taylor"],
        "runtime": 112,
        "language": "English",
        "rating": 7.5,
        "vote_count": 10000,
        "overview": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
        "moods": ["Spooky", "Suspenseful"],
        "poster_path": "/wMF02S6v4t4fh4eku4q3a0ISqdH.jpg"
    },
    {
        "id": 35,
        "title": "A Quiet Place",
        "year": 2018,
        "genres": ["Horror", "Sci-Fi", "Drama"],
        "director": "John Krasinski",
        "cast": ["Emily Blunt", "John Krasinski", "Millicent Simmonds"],
        "runtime": 90,
        "language": "English",
        "rating": 7.5,
        "vote_count": 12000,
        "overview": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.",
        "moods": ["Spooky", "Suspenseful", "Emotional"],
        "poster_path": "/nA1tmM9Ku2M1P45N7e52H9L3Q5w.jpg"
    },

    # --- INTERNATIONAL / FOREIGN LANGUAGE ---
    {
        "id": 36,
        "title": "Parasite",
        "year": 2019,
        "genres": ["Drama", "Thriller", "Comedy"],
        "director": "Bong Joon Ho",
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "runtime": 132,
        "language": "Korean",
        "rating": 8.6,
        "vote_count": 16500,
        "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "moods": ["Mind-bending", "Suspenseful", "Funny", "Emotional"],
        "poster_path": "/7IiTT05Z212z17kQnQsiu5J4v4q.jpg"
    },
    {
        "id": 37,
        "title": "Spirited Away",
        "year": 2001,
        "genres": ["Animation", "Fantasy", "Adventure"],
        "director": "Hayao Miyazaki",
        "cast": ["Rumi Hiiragi", "Miyu Irino", "Mari Natsuki"],
        "runtime": 125,
        "language": "Japanese",
        "rating": 8.6,
        "vote_count": 14000,
        "overview": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
        "moods": ["Inspirational", "Relaxing", "Emotional", "Romantic"],
        "poster_path": "/393mh24afj26kzxyii796e95c10.jpg"
    },
    {
        "id": 38,
        "title": "Pan's Labyrinth",
        "year": 2006,
        "genres": ["Fantasy", "Drama", "War"],
        "director": "Guillermo del Toro",
        "cast": ["Ivana Baquero", "Ariadna Gil", "Sergi López"],
        "runtime": 118,
        "language": "Spanish",
        "rating": 8.2,
        "vote_count": 9000,
        "overview": "In the Falangist Spain of 1944, the young stepdaughter of a sadistic army officer escapes into an eerie but captivating fantasy world.",
        "moods": ["Spooky", "Emotional", "Inspirational"],
        "poster_path": "/5xZl6w66eE6s4p4F1bM2W1R6VzG.jpg"
    },
    {
        "id": 39,
        "title": "Your Name",
        "year": 2016,
        "genres": ["Animation", "Romance", "Drama", "Fantasy"],
        "director": "Makoto Shinkai",
        "cast": ["Ryunosuke Kamiki", "Mone Kamishiraishi", "Ryo Narita"],
        "runtime": 106,
        "language": "Japanese",
        "rating": 8.4,
        "vote_count": 9500,
        "overview": "Two strangers find themselves linked in a bizarre way. When a connection is formed, will distance be the only thing to keep them apart?",
        "moods": ["Romantic", "Emotional", "Mind-bending", "Inspirational"],
        "poster_path": "/xq1Ugd62d23K2knRUx6xxuALTZB.jpg"
    },
    {
        "id": 40,
        "title": "Intouchables",
        "year": 2011,
        "genres": ["Drama", "Comedy"],
        "director": "Olivier Nakache",
        "cast": ["François Cluzet", "Omar Sy", "Anne Le Ny"],
        "runtime": 112,
        "language": "French",
        "rating": 8.5,
        "vote_count": 12000,
        "overview": "After he becomes a quadriplegic from a paragliding accident, an aristocrat hires a young man from the projects to be his caregiver.",
        "moods": ["Funny", "Inspirational", "Relaxing", "Emotional"],
        "poster_path": "/rK0z9c490mC9g275Wz55hXoU4b7.jpg"
    },

    # --- ANIMATION / FAMILY ---
    {
        "id": 41,
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "genres": ["Animation", "Action", "Adventure", "Sci-Fi"],
        "director": "Bob Persichetti",
        "cast": ["Shameik Moore", "Jake Johnson", "Hailee Steinfeld"],
        "runtime": 117,
        "language": "English",
        "rating": 8.4,
        "vote_count": 14000,
        "overview": "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
        "moods": ["Action-packed", "Inspirational", "Funny", "Emotional"],
        "poster_path": "/iiZZdoQBEYQ5VjR7aJ5VfE5v1fD.jpg"
    },
    {
        "id": 42,
        "title": "Wall-E",
        "year": 2008,
        "genres": ["Animation", "Sci-Fi", "Family", "Adventure"],
        "director": "Andrew Stanton",
        "cast": ["Ben Burtt", "Elissa Knight", "Jeff Garlin"],
        "runtime": 98,
        "language": "English",
        "rating": 8.4,
        "vote_count": 16000,
        "overview": "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.",
        "moods": ["Relaxing", "Romantic", "Emotional", "Inspirational"],
        "poster_path": "/hktGpQn8711l7HjBf1816P3JvF3.jpg"
    },
    {
        "id": 43,
        "title": "Coco",
        "year": 2017,
        "genres": ["Animation", "Family", "Fantasy", "Music"],
        "director": "Lee Unkrich",
        "cast": ["Anthony Gonzalez", "Gael García Bernal", "Benjamin Bratt"],
        "runtime": 105,
        "language": "English",
        "rating": 8.4,
        "vote_count": 16000,
        "overview": "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.",
        "moods": ["Emotional", "Inspirational", "Relaxing", "Funny"],
        "poster_path": "/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg"
    },

    # --- MORE HIDDEN GEMS / DIVERSE MOODS ---
    {
        "id": 44,
        "title": "Primer",
        "year": 2004,
        "genres": ["Sci-Fi", "Drama", "Thriller"],
        "director": "Shane Carruth",
        "cast": ["Shane Carruth", "David Sullivan", "Casey Gooden"],
        "runtime": 77,
        "language": "English",
        "rating": 6.8,
        "vote_count": 1500,
        "overview": "Four software engineers who build what they think is a mechanism for reducing the weight of objects find they've accidentally built a time machine.",
        "moods": ["Mind-bending", "Suspenseful"],
        "poster_path": "/9Q4H47d121H0B4J3c6o2W91iN0.jpg"
    },
    {
        "id": 45,
        "title": "The Fall",
        "year": 2006,
        "genres": ["Fantasy", "Drama", "Adventure"],
        "director": "Tarsem Singh",
        "cast": ["Lee Pace", "Catinca Untaru", "Justine Waddell"],
        "runtime": 117,
        "language": "English",
        "rating": 7.8,
        "vote_count": 1200,
        "overview": "In a hospital on the outskirts of 1920s Los Angeles, an injured stuntman begins to tell an imaginative story to a little girl with a broken arm.",
        "moods": ["Inspirational", "Emotional", "Relaxing"],
        "poster_path": "/l624gS3JzWbY35l2LgD5nS3t3l7.jpg"
    },
    {
        "id": 46,
        "title": "Klaus",
        "year": 2019,
        "genres": ["Animation", "Comedy", "Family", "Adventure"],
        "director": "Sergio Pablos",
        "cast": ["Jason Schwartzman", "J.K. Simmons", "Rashida Jones"],
        "runtime": 97,
        "language": "English",
        "rating": 8.2,
        "vote_count": 2200,
        "overview": "A simple act of kindness always sparks another, even in a frozen, faraway place. When Smeerensburg's new postman, Jesper, befriends toymaker Klaus, their gifts melt an age-old feud.",
        "moods": ["Relaxing", "Funny", "Inspirational", "Emotional"],
        "poster_path": "/qAP4nwQ482W3x5l94H20rM8yC91.jpg"
    },
    {
        "id": 47,
        "title": "The Secret in Their Eyes",
        "year": 2009,
        "genres": ["Drama", "Mystery", "Romance"],
        "director": "Juan José Campanella",
        "cast": ["Ricardo Darín", "Soledad Villamil", "Pablo Rago"],
        "runtime": 129,
        "language": "Spanish",
        "rating": 8.2,
        "vote_count": 2800,
        "overview": "A retired legal counselor writes a novel hoping to find closure for one of his past unresolved homicide cases and for his unreciprocated love with his superior.",
        "moods": ["Suspenseful", "Romantic", "Emotional"],
        "poster_path": "/w35t1F979o243t0773j5p4yD6J5.jpg"
    },
    {
        "id": 48,
        "title": "Hunt for the Wilderpeople",
        "year": 2016,
        "genres": ["Comedy", "Drama", "Adventure"],
        "director": "Taika Waititi",
        "cast": ["Sam Neill", "Julian Dennison", "Rima Te Wiata"],
        "runtime": 101,
        "language": "English",
        "rating": 7.8,
        "vote_count": 3200,
        "overview": "A national manhunt is ordered for a rebellious kid and his foster uncle who go missing in the wild New Zealand bush.",
        "moods": ["Funny", "Relaxing", "Inspirational", "Emotional"],
        "poster_path": "/8E9ZJt5w08v4w72lV83Qp6V7vP.jpg"
    },
    {
        "id": 49,
        "title": "Perfect Blue",
        "year": 1997,
        "genres": ["Animation", "Thriller", "Mystery"],
        "director": "Satoshi Kon",
        "cast": ["Junko Iwao", "Rica Matsumoto", "Shinpachi Tsuji"],
        "runtime": 81,
        "language": "Japanese",
        "rating": 8.0,
        "vote_count": 3100,
        "overview": "A retired pop singer turned actress's sense of reality starts to slip away as she is stalked by an obsessed fan and haunted by reflections of her past.",
        "moods": ["Mind-bending", "Suspenseful", "Spooky"],
        "poster_path": "/6WTiOCfDPP8XV4jqfloiVWf7KHq.jpg"
    },
    {
        "id": 50,
        "title": "Roma",
        "year": 2018,
        "genres": ["Drama"],
        "director": "Alfonso Cuarón",
        "cast": ["Yalitza Aparicio", "Marina de Tavira", "Diego Cortina Autrey"],
        "runtime": 135,
        "language": "Spanish",
        "rating": 7.7,
        "vote_count": 3900,
        "overview": "A year in the life of a middle-class family's maid in Mexico City in the early 1970s.",
        "moods": ["Relaxing", "Emotional"],
        "poster_path": "/t099xZ8s6yD1jW3S588k9881881.jpg"
    }
]

SIMULATED_PERSONAS = [
    {
        "name": "Alex (Sci-Fi Nerd)",
        "ratings": {
            1: 5,  # Inception
            2: 5,  # Interstellar
            3: 5,  # Matrix
            4: 4,  # Blade Runner 2049
            5: 5,  # Arrival
            6: 4,  # Coherence
            20: 4, # Fight Club
            29: 5, # The Prestige
            30: 4, # Memento
            44: 5, # Primer
            13: 2, # Grand Budapest
            23: 1, # La La Land
            24: 2  # About Time
        }
    },
    {
        "name": "Sarah (Romance & Musicals)",
        "ratings": {
            23: 5, # La La Land
            24: 5, # About Time
            25: 4, # Before Sunrise
            26: 5, # Amélie
            7: 4,  # Eternal Sunshine
            19: 5, # Forrest Gump
            13: 4, # Grand Budapest
            39: 5, # Your Name
            40: 4, # Intouchables
            1: 1,  # Inception
            3: 1,  # The Matrix
            9: 1,  # Mad Max
            11: 2  # John Wick
        }
    },
    {
        "name": "Marcus (Action Buff)",
        "ratings": {
            8: 5,  # Dark Knight
            9: 5,  # Mad Max
            10: 5, # Gladiator
            11: 5, # John Wick
            12: 4, # Kill Bill
            3: 4,  # Matrix
            1: 4,  # Inception
            20: 4, # Fight Club
            41: 5, # Spider-Man
            25: 1, # Before Sunrise
            26: 1, # Amélie
            50: 2  # Roma
        }
    },
    {
        "name": "Emily (Horror / Thriller Fan)",
        "ratings": {
            27: 5, # Shutter Island
            28: 5, # Se7en
            32: 5, # Get Out
            33: 5, # Hereditary
            34: 4, # The Conjuring
            35: 4, # A Quiet Place
            49: 4, # Perfect Blue
            6: 4,  # Coherence
            20: 5, # Fight Club
            14: 1, # Superbad
            15: 2, # Groundhog Day
            43: 2  # Coco
        }
    },
    {
        "name": "David (Art-house & Drama Critic)",
        "ratings": {
            18: 5, # Shawshank
            22: 5, # Godfather
            36: 5, # Parasite
            38: 4, # Pan's Labyrinth
            50: 5, # Roma
            21: 5, # Whiplash
            4: 4,  # Blade Runner 2049
            5: 4,  # Arrival
            25: 4, # Before Sunrise
            11: 1, # John Wick
            14: 1, # Superbad
            34: 2  # The Conjuring
        }
    },
    {
        "name": "Kenji (Animation Enthusiast)",
        "ratings": {
            37: 5, # Spirited Away
            39: 5, # Your Name
            41: 5, # Spider-Verse
            42: 4, # Wall-E
            43: 5, # Coco
            46: 5, # Klaus
            49: 4, # Perfect Blue
            13: 4, # Grand Budapest
            2: 4,  # Interstellar
            8: 2,  # Dark Knight
            28: 1, # Se7en
            33: 1  # Hereditary
        }
    },
    {
        "name": "Jessica (Comedy / Feel-Good)",
        "ratings": {
            13: 5, # Grand Budapest
            14: 5, # Superbad
            15: 4, # Groundhog Day
            16: 4, # Knives Out
            17: 4, # Shaun of the Dead
            48: 5, # Wilderpeople
            19: 5, # Forrest Gump
            40: 5, # Intouchables
            46: 4, # Klaus
            22: 1, # Godfather
            28: 2, # Se7en
            33: 1, # Hereditary
            44: 1  # Primer
        }
    },
    {
        "name": "Sophia (Indie / Hidden Gems)",
        "ratings": {
            6: 5,  # Coherence
            44: 4, # Primer
            45: 5, # The Fall
            47: 4, # Secret in Their Eyes
            48: 4, # Wilderpeople
            49: 4, # Perfect Blue
            26: 4, # Amélie
            46: 4, # Klaus
            13: 4, # Grand Budapest
            3: 2,  # Matrix
            22: 3, # Godfather
            11: 2  # John Wick
        }
    }
]
