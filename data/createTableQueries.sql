/*
How we created table
*/
DROP TABLE IF EXISTS ARTIST CASCADE;
CREATE TABLE ARTIST (
  Name VARCHAR(100) PRIMARY KEY
  );

-- via songTable.CSV
DROP TABLE IF EXISTS SONG CASCADE;
CREATE TABLE SONG (
  Name VARCHAR(100),
  Artist VARCHAR(100),
  BillboardYear INTEGER,
  Ranking INTEGER
);

\COPY SONG(Name, Artist, BillboardYear,Ranking) FROM 'songTable.csv' CSV

ALTER TABLE SONG ADD ID SERIAL UNIQUE;

-- via wordcountTable.CSV
DROP TABLE IF EXISTS WORDCOUNT CASCADE;
CREATE TABLE WORDCOUNT (
  SongID INTEGER REFERENCES SONG(ID),
  Word VARCHAR(100),
  Frequency INTEGER,
  PRIMARY KEY(Word, SongID)
  );

\COPY WORDCOUNT(SongID, Word, Frequency) FROM 'wordcountTable.csv' CSV

DROP TABLE IF EXISTS COMMONWORDS;
CREATE TABLE COMMONWORDS (
	Word VARCHAR(100)
);

\COPY COMMONWORDS(Word) FROM 'commonWords.csv' CSV