"""
This is a little test suite for process_congress_records.py
"""
import process_congress_records


process_congress_records.get_pdf(year=2020, doc_id=10039988)
process_congress_records.get_pdf(year=2020, first="Joe", last="Wilson")
