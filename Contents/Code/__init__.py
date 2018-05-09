class RadarrAgent(Agent.Movies):

	name = 'Radarr'
	languages = [Locale.Language.NoLanguage]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):
		if media.primary_agent == 'com.plexapp.agents.imdb':
			self.append_default_metadata_search_result(results, media)
		else:
			self.append_matching_metadata_search_result(results, media, lang)

	def append_default_metadata_search_result(self, results, media):
		results.Append(MetadataSearchResult(
			id = media.primary_metadata.id,
			score = 100
		))

	def append_matching_metadata_search_result(self, results, media, lang):
		json = self.get_api_data('/movie')
		if not json:
			return
		movies = JSON.ObjectFromString(json)
		for movie in movies:
			self.append_matching_movie_metadata_search_result(results, media, lang)

	def append_matching_movie_metadata_search_result(self, results, media, lang):
		if movie['title'] != media.title:
			return
		score = self.get_score(media, movie)
		results.Append(MetadataSearchResult(
			id = movie['imdbId'],
			name = movie['title'],
			year = movie['year'],
			score = score,
			lang = lang
		))

	def update(self, metadata, media, lang):
		json = self.get_api_data('/movie')
		if not json:
			return
		movies = JSON.ObjectFromString(json)
		names = list()
		for movie in movies:
			if movie['imdbId'] == metadata.id:
				self.update_metadata(metadata, movie, names)
		metadata.art.validate_keys(names)
		metadata.posters.validate_keys(names)

	def get_score(self, media, movie):
		if media.year and int(media.year) > 1900 and int(media.year) == movie['year']:
			return 100
		return 90

	def update_metadata(self, metadata, movie, names):
		metadata.genres = movie['genres']
		metadata.tags = movie['tags']
		metadata.collections = movie['genres']
		metadata.duration = movie['runtime'] * 60 * 1000
		metadata.rating = movie['ratings']['value']
		metadata.original_title = movie['title']
		metadata.title = movie['title']
		metadata.year = movie['year']
		metadata.originally_available_at = Datetime.ParseDate(movie['inCinemas']).date()
		metadata.studio = movie['studio']
		metadata.summary = movie['overview']
		for image in movie['images']:
			self.update_image_metadata(metadata, image, names)

	def update_image_metadata(self, metadata, image, names):
		radarr_image_url = self.create_full_url(image['url'])
		radarr_image = self.get_api_data(image['url'])
		names.append(radarr_image_url)
		if image['coverType'] == 'fanart':
			metadata.art[radarr_image_url] = Proxy.Media(radarr_image)
		elif image['coverType'] == 'poster':
			metadata.posters[radarr_image_url] = Proxy.Media(radarr_image)

	def get_api_data(self, uri):
		request_url = self.create_authorized_full_url(uri)
		try:
			return HTTP.Request(request_url).content
		except:
			Log('Error requesting {}'.format(request_url))
			return None

	def create_authorized_full_url(self, uri):
		full_url = self.create_full_url(uri)
		if not full_url:
			return None
		if not Prefs['radarr_api_key']:
			Log('Enter your Radarr API key in the agent\'s preferences')
			return None
		return '{}?apikey={}'.format(full_url, Prefs['radarr_api_key'])

	def create_full_url(self, uri):
		if not Prefs['radarr_url']:
			Log('Enter your Radarr URL in the agent\'s preferences')
			return None
		base_url = Prefs['radarr_url'].rstrip('/')
		return '{}/api{}'.format(base_url, uri)
