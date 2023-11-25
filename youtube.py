import textblob as SentimentAnalyzer
import googleapiclient.discovery as GoogleYouTubeAPI


class YouTube:
    __youtube = None
    __google_api_key: str = 'AIzaSyB-gvVazbsehG-ChOiVhBfgvK01ITNN-cw'  # Put your Google Youtube API client API

    def __init__(self, google_api_key):
        self.__google_api_key = google_api_key
        try:
            self.__youtube = GoogleYouTubeAPI.build("youtube", "v3", developerKey=self.__google_api_key)
        except Exception as exception:
            print('Unable to connect to Youtube: ' + str(exception))

    def get_video_comments(self, **kwargs) -> list | None:
        if not self.__youtube:
            return
        comments = []
        results = self.__youtube.commentThreads().list(**kwargs).execute()

        while results:
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            # Get the next set of comments
            results = self.__youtube.commentThreads().list_next(results, kwargs)

        return comments

    @staticmethod
    def get_comment_feelings(comments) -> dict:
        positive_comments = 0
        for comment in comments:
            sentiment_analyzer = SentimentAnalyzer.TextBlob(comment)
            sentiment_score = sentiment_analyzer.sentiment.polarity
            if sentiment_score > 0:
                positive_comments += 1
        return {
            'Total': len(comments),
            'Positive': positive_comments,
            'Negative': len(comments) - positive_comments
        }
