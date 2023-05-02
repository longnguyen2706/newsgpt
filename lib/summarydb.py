import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
from typing import Dict, Optional

import lib.config as config
from lib.newsgpt import NewsCategory, NewsLength
import datetime

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

##############################################################################


def generate_id(category: NewsCategory, length: NewsLength) -> str:
    # with datetime
    return f"{datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')}-{category}-{length}"

##############################################################################


class SummaryDB:
    def __init__(self):
        """
        Initialize the SummaryDB class
        """
        self.client = cosmos_client.CosmosClient(
            HOST, {'masterKey': MASTER_KEY},
            user_agent="CosmosDBPython", user_agent_overwrite=True)
        self.init_containers()

    def init_containers(self):
        """
        NOTE: there's some issue when reading the table when the container is created via the azure
                web GUI. The container must be created via the python api.
        """
        try:
            self.db = self.client.create_database(id=DATABASE_ID)
            print('Database with id \'{0}\' created'.format(DATABASE_ID))
        except exceptions.CosmosResourceExistsError:
            self.db = self.client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))

        # setup container for summary
        try:
            self.container = self.db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/partitionKey'))
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))
        except exceptions.CosmosResourceExistsError:
            self.container = self.db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

    def write_summary(
        self, category: NewsCategory, length: NewsLength, summary: str
    ) -> Optional[str]:
        id = generate_id(category, length)
        item = {
            "id": id,
            "partitionKey": id,
            "category": category,
            "length": length,
            "summary": summary,
        }
        try:
            self.container.create_item(body=item)
        except exceptions.CosmosResourceExistsError as e:
            print("item already exists, updating...")
            self.container.replace_item(item=id, body=item)
        return id

    def read_summary(self, id: str) -> Optional[Dict]:
        try:
            return self.container.read_item(
                id, id)  # id and partition key are the same
        except exceptions.CosmosResourceNotFoundError as e:
            print(e)
            print("item not found")
            return None

    def query_overall_latest_summary(self) -> Optional[Dict]:
        try:
            return list(self.container.query_items(
                query="SELECT TOP 1 * FROM c ORDER BY c._ts DESC",
                enable_cross_partition_query=True
            ))[0]
        except IndexError as e:
            print("no items found")
            return None

    def query_latest_summary(self, category, length) -> Optional[Dict]:
        try:
            return list(self.container.query_items(
                query="SELECT TOP 1 * FROM c WHERE c.category = '{0}' AND c.length = {1} ORDER BY c._ts DESC".format(
                    category, length),
                enable_cross_partition_query=True
            ))[0]
        except IndexError as e:
            print("no items found")
            return None


if '__main__' == __name__:
    summary_db = SummaryDB()

    summary_db.write_summary(NewsCategory.BUSINESS, NewsLength.SHORT, "Nothing intersting today")
    summary_db.write_summary(NewsCategory.TECHNOLOGY, NewsLength.SHORT, "this is a summary of tech")

    print("----------all---------")
    latest = summary_db.query_overall_latest_summary()
    print(latest)

    print("-----------business--------")
    latest = summary_db.query_latest_summary(NewsCategory.BUSINESS, NewsLength.SHORT)
    print(latest)
