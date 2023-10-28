import logging
import os
import random
import time
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter

import psycopg2
from psycopg2.extras import NamedTupleCursor
from psycopg2.errors import SerializationFailure, Error
#from psycopg2.rows import namedtuple_row
db_url = "postgresql://calhack:Ucdc5Rfgws0pVlEk8bdAsg@bumble-stag-3694.g95.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

def createConn():
    try: 
        conn = psycopg2.connect(db_url,
                                     application_name="$ docs_simplecrud_psycopg3", 
                                     cursor_factory=NamedTupleCursor)
    except Exception as e:
            logging.fatal("database connection failed")
            logging.fatal(e)
            return
    return conn


def run_transaction(conn, op, max_retries=3):
    with conn.transaction():
        for retry in range(1, max_retries + 1):
            try:
                op(conn) 

                # If we reach this point, we were able to commit, so we break
                # from the retry loop.
                return

            except SerializationFailure as e:
                # This is a retry error, so we roll back the current
                # transaction and sleep for a bit before retrying. The
                # sleep time increases for each failed transaction.
                logging.debug("got error: %s", e)
                conn.rollback()
                logging.debug("EXECUTE SERIALIZATION_FAILURE BRANCH")
                sleep_seconds = (2**retry) * 0.1 * (random.random() + 0.5)
                logging.debug("Sleeping %s seconds", sleep_seconds)
                time.sleep(sleep_seconds)

            except psycopg.Error as e:
                logging.debug("got error: %s", e)
                logging.debug("EXECUTE NON-SERIALIZATION_FAILURE BRANCH")
                raise e

        raise ValueError(
            f"transaction did not succeed after {max_retries} retries")

def createTable(conn):
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    with conn.cursor() as cur:
        try:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS patients (id UUID PRIMARY KEY, name VARCHAR(30), therapist VARCHAR(30))"
            )
            conn.commit()  # Commit the transaction
            print("Table 'patients' created successfully.")
        except psycopg.Error as e:
            conn.rollback()  # Rollback the transaction in case of an error
            print(f"Error creating table: {e}")
        # cur.execute(
        #     "UPSERT INTO accounts (id, balance) VALUES (%s, 1000), (%s, 250)", (id1, id2))
        # logging.debug("create_accounts(): status message: %s",
        #               cur.statusmessage)
    return [id1, id2]

if __name__ == '__main__':
    conn = createConn()
    createTable(conn)
    conn.close()