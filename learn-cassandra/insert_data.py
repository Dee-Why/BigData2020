import logging
import time

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
#from cassandra.cluster import Cluster
#from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


KEYSPACE = "mykeyspace"


def insertData():
    cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
    session = cluster.connect()

    try:
        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        stamp = int(time.time())
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime(stamp))
        log.info("inserting data...")
        session.execute("""
            insert into mytable(timestamp, filename, predictcategory) values('{}', '1_T-shirt.JPEG', 'Shirt')
            """.format(timestamp))
    except Exception as e:
        log.error("Unable to insert data")
        log.error(e)


insertData()

