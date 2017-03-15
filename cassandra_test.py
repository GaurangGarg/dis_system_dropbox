import logging

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)


KEYSPACE = "files"


def initialize_cassandra_cluster():
    destroy_cassandra_cluster()
    create_cassandra_cluster()


def create_cassandra_cluster():
    cluster = Cluster(['52.40.197.16', '52.11.0.58', '54.70.142.196', '54.70.139.205', '52.27.28.162'])
    session = cluster.connect()

    log.info("creating keySpace...")
    session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '4' }
            """ % KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    log.info("creating table...")

    session.execute("""
            CREATE TABLE fileinfo (
                filename text,
                filecontent text,
                PRIMARY KEY (filename, filecontent)
            )
            """)


def destroy_cassandra_cluster():
    try:
        cluster = Cluster(['52.40.197.16', '52.11.0.58', '54.70.142.196', '54.70.139.205', '52.27.28.162'])
        session = cluster.connect()
        session.execute("DROP KEYSPACE " + KEYSPACE)
    except Exception as e:
        log.exception(e.message)


def cassandra_test():
    cluster = Cluster(['52.40.197.16', '52.11.0.58', '54.70.142.196', '54.70.139.205', '52.27.28.162'])
    session = cluster.connect()

    log.info("creating keyspace...")
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '4' }
        """ % KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    log.info("creating table...")
    session.execute("""
        CREATE TABLE fileinfo (
            filename text,
            filecontent text,
            PRIMARY KEY (filename, filecontent)
        )
        """)

    query = SimpleStatement("""
        INSERT INTO fileinfo (filename, filecontent)
        VALUES (%(key)s, %(a)s)
        """, consistency_level=ConsistencyLevel.ONE)

    prepared = session.prepare("""
        INSERT INTO fileinfo (filename, filecontent)
        VALUES (?, ?)
        """)

    for i in range(10):
        log.info("inserting row %d" % i)
        session.execute(query, dict(key="key%d" % i, a='a'))
        session.execute(prepared.bind(("key%d" % i, 'b')))

    future = session.execute_async("SELECT * FROM fileinfo")
    log.info("key\tcol1")
    log.info("---\t----")

    rows = []
    try:
        rows = future.result()
    except Exception as e:
        log.exception(e.message)

    for row in rows:
        log.info('\t'.join(row))

    session.execute("DROP KEYSPACE " + KEYSPACE)

if __name__ == "__main__":
    initialize_cassandra_cluster()
