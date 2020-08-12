import psycopg2

# TODO: Someway to translate between song and songID
# TODO: Handle songs which appeared in consecutive years who show up twice?
# TODO: Add artist on word result page



def connect(user,password):
	'''
	Establishes a connection to the database with the following credentials:
		user - username, which is also the name of the database
		password - the password for this database on perlman

	Returns: a database connection.

	Note: exits if a connection cannot be established.
	'''
	try:
		connection = psycopg2.connect(database=user, user=user,password=password)
	except Exception as e:
		print("Connection error: ", e)
		exit()
	return connection

class DataSource:
	'''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	'''
	def __init__(self):
		user = 'ec2-user'
		password = 'rainbowtrout1612'
		self.connection = connect(user,password)

	def closeConnection(self):
		self.connection.close()

	def getWordInstancesInSong(self, word, songID):
		"""
		Retrieves the number of instances of a word in a SONG.

		Arguments:
			word - the word whose count will be retrieved.
			songID - the song ID of the word's which will be retrieved.
		"""
		try:
			cursor = self.connection.cursor()
			query = "SELECT Frequency FROM WORDCOUNT WHERE SongID = (%s) AND Word = (%s)"
			cursor.execute(query,(songID,word))
			result = cursor.fetchone()
			if result:
				return result[0]
			else:
				return 0

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return 0

	def getWordInstancesInYear(self, word, year):
		'''
		Returns: An integer saying how many times the word was said in that year.

		TODO: CLEAN THIS UP????
		TODO: Make all the ifs their own query?
		'''
		try:
			if not isinstance(word, str) or (not isinstance(year, int)):
				raise TypeError
			elif not word.isalnum():
				raise ValueError
			elif (year < 1965) or (year > 2015):
				raise ValueError('year should be within the range 1965-2015. The value of x was: {}'.format(year))
			else:
				#TODO: Could this be a seperate query?
				cursor = self.connection.cursor()
				query = "SELECT SUM(COUNTSOFWORD.Frequency) FROM (SELECT SONG.ID FROM SONG WHERE SONG.BillboardYear = (%s)) AS SONGSINYEAR JOIN (SELECT * FROM WORDCOUNT WHERE wordcount.Word = (%s)) AS COUNTSOFWORD ON SONGSINYEAR.ID = COUNTSOFWORD.SongID GROUP BY COUNTSOFWORD.Word"
				cursor.execute(query, (str(year), word))

				result = cursor.fetchone()
				if result:
					return result[0]
				else:
					return 0
		except Exception as e:
				raise e #Raised again so unittest suite can read it
				return None

	def getUniqueWordInstancesInYear(self, word, year):
		'''
		Returns: An integer saying how many times the word was in a song that year.

		'''
		try:
			if not isinstance(word, str) or (not isinstance(year, int)):
				raise TypeError
			elif not word.isalnum():
				raise ValueError
			elif (year < 1965) or (year > 2015):
				raise ValueError('year should be within the range 1965-2015. The value of x was: {}'.format(year))
			else:
				cursor = self.connection.cursor()
				query = "SELECT COUNT(*) FROM (SELECT SONG.ID FROM SONG WHERE SONG.BillboardYear = (%s)) AS SONGSINYEAR JOIN (SELECT * FROM WORDCOUNT WHERE wordcount.Word = (%s)) AS COUNTSOFWORD ON SONGSINYEAR.ID = COUNTSOFWORD.SongID"
				cursor.execute(query, (str(year), word))

				results = cursor.fetchall()
				if len(results) != 0: #fetchall returns a list, we only care about the first
					return results[0][0]
				else:
					return 0
		except Exception as e:
				raise e #Rasied again so unittest suite can read it
				return None

	def getWordTrendList(self, word, year1=1965, year2=2015):
		"""
		Returns a list of word frequency over time.
		Useful for a bar graph.
		"""
		try:
			dict = []
			i = year1
			while i < year2 + 1:
				instances = self.getWordInstancesInYear(word, i)
				dict.append(instances)
				i = i + 1
			return dict
		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getTopXWordsofArtist(self, artistName, numberOfWords=50):
		"""
		Retrieves the number of instances of a word in a SONG.

		Arguments:
			word - the word whose count will be retrieved.
			songID - the song ID of the word's which will be retrieved.
		"""
		try:
			cursor = self.connection.cursor()
			query = ("SELECT UNCOMMONWORDS.Word, SUM(UNCOMMONWORDS.Frequency) "
						"FROM "
							"(SELECT * FROM WORDCOUNT "
								"WHERE WORDCOUNT.Word NOT IN (SELECT COMMONWORDS.Word FROM COMMONWORDS)) AS UNCOMMONWORDS "
							"JOIN "
							"(SELECT SONG.ID, SONG.Artist FROM SONG "
								"WHERE SONG.Artist LIKE (%s)) AS SONGSBYARTIST "
							"ON UNCOMMONWORDS.SongID = SONGSBYARTIST.ID "
						"GROUP BY UNCOMMONWORDS.Word "
						"ORDER BY SUM(UNCOMMONWORDS.Frequency) DESC "
						"LIMIT (%s);")
			artistName = '%' + artistName + '%'
			cursor.execute(query, (artistName, str(numberOfWords)))
			result = cursor.fetchall()
			if result:
				return result
			else:
				return 0
		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def isWordInSong(self, word, songID):
		"""
		Retrieves the number of instances of a word in a SONG.

		Arguments:
			connection - the current connection to the database.
			word - the word that will be checked.
			songID - the song ID of the song that will be checked.
		"""
		try:
			results = self.getWordInstancesInSong(self, word, songID)
			if results != 0:
				return True
			else:
				return False

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)

	def getTopXWordsInYear(self, year, numberOfWords=100):
		"""
		Retrieves the X most used words for a given year.

		Arguments:
			numberOfWords - the number of words that will be retrieved before we cut off.
			year - the year from which we will retrieve our list of top words.
		"""
		try:
			if (year < 1965) or (year > 2015):
				raise ValueError('year should be within the range 1965-2015.')
				print(year)
			else:
				cursor = self. connection.cursor()
				query = ("SELECT YEARCOUNTS.Word, SUM(YEARCOUNTS.Frequency) AS Frequency "
						 "FROM ((SELECT SONG.ID FROM SONG WHERE SONG.BillboardYear = (%s)) AS SongYear "
						 "JOIN WORDCOUNT ON SongYear.ID = WORDCOUNT.SongID AND WORDCOUNT.Word NOT IN (SELECT COMMONWORDS.WORD FROM COMMONWORDS)) AS YEARCOUNTS "
						 "GROUP BY YEARCOUNTS.Word ORDER BY SUM(YEARCOUNTS.Frequency) DESC LIMIT (%s) ;")

				cursor.execute(query, (str(year),str(numberOfWords)))
				return cursor.fetchall()
		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getTopXSongsInYear(self, year, numberOfSongs=100):
		"""
		Retrieves the 10 most popular songs for a given year.

		Arguments:
			year - the year from which we will retrieve our list of top songs.
		"""
		try:

			cursor = self. connection.cursor()
			query = ("SELECT SONG.Ranking, SONG.Artist, SONG.Name "
						"FROM SONG "
							"WHERE SONG.BillboardYear = (%s) "
						"ORDER BY SONG.Ranking ASC "
						"LIMIT (%s);")

			cursor.execute(query, (str(year), str(numberOfSongs)))
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getTopXSongsWithMyWord(self, word, numberOfSongs=50):
		"""
		Retrieves the X songs of all time that use a given word.

		Arguments:
			word - the word that will be the basis for choosing songs.
			numberOfSongs - the number of songs we will retrieve before we cut off.
		"""
		try:
			cursor = self.connection.cursor()
			query = "SELECT SONG.Name, TOPWORDS.Frequency FROM SONG, (SELECT WORDCOUNT.SongID, WORDCOUNT.Frequency FROM WORDCOUNT WHERE WORDCOUNT.Word = (%s)) AS TOPWORDS WHERE SONG.ID = TOPWORDS.SongID ORDER BY TOPWORDS.Frequency DESC LIMIT (%s);"
			cursor.execute(query, (word,str(numberOfSongs)))
			return cursor.fetchall()

		except Exception as e:
			print ("Something went wrong when executing the query: ", e)
			return None

	def getTopXWordsInYearRange(self, year1, year2, numberOfWords = 200):
		"""
		Retrieves the X most used words within a given year range.

		Arguments:
			numberOfWords - the number of words that will be retrieved before we cut off.
			year1 - the year to start on
			year2 - the end year
		"""
		try:
			if year1 > year2:
				raise ValueError('make sure first year is smaller than second')
			elif (year1 < 1965) or (year1 > 2015) or (year2 < 1965) or (year2 > 2015) :
				raise ValueError('both years should be within the range 1965-2015.')
			else:
				cursor = self.connection.cursor()
				query = ("SELECT YearRangeCounts.Word, SUM(YearRangeCounts.Frequency) AS Frequency "
						 "FROM ((SELECT SONG.ID FROM SONG WHERE SONG.BillboardYear BETWEEN (%s) AND (%s)) AS SongsFromYearRange "
						 "JOIN WORDCOUNT ON SongsFromYearRange.ID = WORDCOUNT.SongID AND WORDCOUNT.WORD NOT IN (SELECT COMMONWORDS.WORD FROM COMMONWORDS)) "
						 "AS YearRangeCounts GROUP BY YearRangeCounts.Word ORDER BY SUM(YearRangeCounts.Frequency) DESC LIMIT (%s) ;")

				cursor.execute(query, (str(year1), str(year2), str(numberOfWords)))
				return cursor.fetchall()
		except Exception as e:
			print("Something went wrong when executing the query: ", e)
			return None



def main():
	data = DataSource()
	pass
	data.closeConnection()
if  __name__ == '__main__':
	main()
