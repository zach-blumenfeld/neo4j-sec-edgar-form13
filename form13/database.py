from google.cloud import bigquery
import google.api_core.exceptions

class database():
    client = None
    dataset_ref = None
    table_ref = None
    table = None
    schema = None

    def __init__(self):
        self.client = bigquery.Client()
        self.dataset_ref = self.client.dataset('edgar')
        self.table_ref = self.dataset_ref.table('form13')

        self.schema = [
            bigquery.SchemaField('fillingManager', 'STRING'),
            bigquery.SchemaField('reportCalendarOrQuarter', 'DATE'),
            bigquery.SchemaField('nameOfIssuer', 'STRING'),
            bigquery.SchemaField('cusip', 'STRING'),
            bigquery.SchemaField('value', 'FLOAT'),
            bigquery.SchemaField('shares', 'FLOAT')
        ]

        self.table = bigquery.Table(self.table_ref, schema=self.schema)

        # Create the table or pass if it already exists
        try:
            self.table = self.client.create_table(self.table)
            self.table_ref = self.dataset_ref.table('form13')
        except google.api_core.exceptions.Conflict:
            pass

        assert self.table.table_id == 'form13'
        self.table = self.client.get_table(self.table_ref)


    def formatRow(self, filing):
        month = filing['reportCalendarOrQuarter'][0:2]
        day = filing['reportCalendarOrQuarter'][3:5]
        year = filing['reportCalendarOrQuarter'][6:10]
        reportCalendarOrQuarter = year + '-' + month + '-' + day

        row = (
            filing['fillingManager'],
            reportCalendarOrQuarter,
            filing['nameOfIssuer'],
            filing['cusip'],
            filing['value'],
            filing['shares']
        )
        return row


    def insert(self, filings):
        rows = []
        for filing in filings:
            row = self.formatRow(filing)
            rows.append(row)

        if len(rows) > 0:
            errors = self.client.insert_rows(self.table, rows)
            assert errors == []
