from argparse import ArgumentParser
from pyLBL import Database, HitranWebApi


def main(api_key, database_path):
    # Create the database.
    webapi = HitranWebApi(api_key)
    database = Database(database_path)
    database.create(webapi)


if __name__ == "__main__":
    parser = ArgumentParser("Create the spectral database.")
    parser.add_argument("api_key", help="HITRAN API key.")
    parser.add_argument("database_path", help="Path to the database file.")
    args = parser.parse_args()
    main(args.api_key, args.database_path)
