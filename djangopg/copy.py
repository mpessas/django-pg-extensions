# -*- coding: utf-8 -*-

import csv
from cStringIO import StringIO
from django.db import connections
from django.db.models import AutoField


def _convert_to_csv_form(data):
    """Convert the data to a form suitable for CSV."""
    # NULL values should be an empty column
    if data is None:
        return ''
    # Empty strings should be different to NULL values
    if data == '':
        return '""'
    # CSV needs to be encoded to UTF8
    if isinstance(data, unicode):
        return data.encode('UTF-8')
    return data


def _send_csv_to_postgres(fd, conn, table_name, columns):
    """
    Send the CSV file to PostgreSQL for inserting the entries.

    Use the COPY command for faster insertion and less WAL generation.

    :param fd: A file-like, CSV-formatted object with the data to send.
    :param conn: The connection object.
    """
    columns = map(conn.ops.quote_name, columns)
    cursor = conn.cursor()
    sql = "COPY %s(%s) FROM STDIN WITH CSV"
    try:
        cursor.copy_expert(sql % (table_name, ','.join(columns)), fd)
    finally:
        cursor.close()


def copy_insert(model, entries, columns=None, using='default'):
    """
    Add the given entries to the database using the COPY command.

    The caller is required to handle the transaction.

    :param model: The model class the entries are for.
    :param entries: An iterable of entries to be inserted.
    :param columns: A list of columns that will have to be populated.
        By default, we use all columns but the primary key.
    :param using: The database connection to use.
    """
    table_name = model._meta.db_table
    conn = connections[using]

    if columns is None:
        fields = [
            f for f in model._meta.fields if not isinstance(f, AutoField)
        ]
        columns = [f.column for f in fields]
    else:
        fields = [model._meta.get_field_by_name(col)[0] for col in columns]

    # Construct a StringIO from the entries
    fd = StringIO()
    csvf = csv.writer(fd)
    for entry in entries:
        row = [
            _convert_to_csv_form(
                f.get_db_prep_save(getattr(entry, f.column), connection=conn)
            )
            for f in fields
        ]
        csvf.writerow(row)
    # Move the fp to the beginning of the string
    fd.seek(0)
    _send_csv_to_postgres(fd, conn, table_name, columns)
