import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://news-summaries-db.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'Kphv2Koml95kLH7vSQsSLzLs0GvLgWmiwEeUIXKxuPUlNR4O7KKIEb0RBPgpjHgP0HizUGuFcVOAACDbvR62FA=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'news-summaries'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'summaries'),
}
