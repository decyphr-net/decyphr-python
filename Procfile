release: pip3 install https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-2.2.0/pt_core_news_sm-2.2.0.tar.gz
web: gunicorn lang.wsgi:application --preload --log-level debug