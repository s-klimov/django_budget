import collections


def extract_records(con, sql: str, params: dict = dict(), many: bool = True):
    """

    :type con: connection to db
    """
    # creating cursor
    cur = con.cursor()
    cur.execute(sql, params)

    def namedtuple_factory(cursor, row):
        Record = collections.namedtuple('BudgetRecord', [column[0].lower() for column in cursor.description])
        return Record(*row)

    cur.row_factory = namedtuple_factory
    records = cur.fetchall() if many else cur.fetchone()
    return records
