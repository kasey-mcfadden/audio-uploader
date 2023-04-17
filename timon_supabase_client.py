from typing import List, Optional, Union
from dotenv import load_dotenv
from supabase import create_client
import os
from audit import Audit

load_dotenv()
supabase_url = os.environ.get('TIMON_SUPABASE_URL')
supabase_anon_key = os.environ.get('TIMON_SUPABASE_ANON_KEY')

client = create_client(supabase_url, supabase_anon_key)

def get_total_audits_count() -> int:
    """Gets the total number of audits in the database.

    Returns:
        An integer representing the total number of audits of artwork.
    """
    response = client.from_('auditing').select("audit_id", count="exact").execute() # We only need the 'id' column for counting purposes

    count = response.count
    print('Total count:', count)
    return int(count)

def get_all_audits() -> List[Audit]:
    response = client.from_('auditing').select('*').execute()

    data = response.data

    if not data:
        raise Exception('No audits found')

    return [Audit(
        audit_id = audit['audit_id'],
        auditor = audit['auditor'],
        content = audit['content'],
        start_time = audit['start_time'],
        publish_time = audit['publish_time'],
        flagged = audit['flagged'],
        art_id = audit['art_id'],
        chatgpt_time = audit['chatgpt_time'],
        skipped = audit['skipped'],
        gpt_output = audit['gpt_output'],
        gpt_model = audit['gpt_model']
    ) for audit in data]

def main():
    """
    The main function of the program.
    """

    audits = get_all_audits()
    print(audits[0])

if __name__ == '__main__':
    main()