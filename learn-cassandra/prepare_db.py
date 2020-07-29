import logging

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

def createKeySpace():
   cluster = Cluster(contact_points=['127.0.0.1'],port=9042)
   session = cluster.connect()

   log.info("Creating keyspace...")
   try:
       session.execute("""
           CREATE KEYSPACE %s
           WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
           """ % KEYSPACE)

       log.info("setting keyspace...")
       session.set_keyspace(KEYSPACE)

       log.info("creating table...")
       session.execute("""
           CREATE TABLE mytable (
               timestamp text,
               filename text,
               predictcategory text,
               PRIMARY KEY (timestamp, filename)
           )
           """)
   except Exception as e:
       log.error("Unable to create keyspace")
       log.error(e)

createKeySpace();



