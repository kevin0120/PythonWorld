from access_parser import AccessParser

if __name__ == '__main__':
    # .mdb or .accdb file
    db = AccessParser("data1.accdb")

    # Print DB tables
    print(db.catalog)

    # # Tables are stored as defaultdict(list) -- table[column][row_index]
    table = db.parse_table("data")

    # Pretty print all tables
    db.print_database()
