import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load credentials from the JSON file
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']


def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds


def extract_doc_id_from_url(url):
    # Regular expression to extract the document ID from the Google Docs URL
    match = re.search(r'/d/([^/]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Docs URL")


def get_document_text(doc_id, creds):
    service = build('docs', 'v1', credentials=creds)

    # Fetch the document
    document = service.documents().get(documentId=doc_id).execute()
    content = document.get('body').get('content')

    text = ''
    for element in content:
        # Extract text from paragraphs
        if 'paragraph' in element:
            for text_run in element.get('paragraph').get('elements'):
                if 'textRun' in text_run:
                    text += text_run.get('textRun').get('content')

        # Extract text from tables
        if 'table' in element:
            for row in element.get('table').get('tableRows'):
                for cell in row.get('tableCells'):
                    for paragraph in cell.get('content'):
                        if 'paragraph' in paragraph:
                            for text_run in paragraph.get('paragraph').get('elements'):
                                if 'textRun' in text_run:
                                    text += text_run.get('textRun').get('content')   # Tab-separated for cells
                text += '\n'  # New line after each row

    return text


if __name__ == '__main__':
    creds = authenticate()

    # Replace with your Google Doc URL
    doc_url = 'https://docs.google.com/document/d/1BCbpQQUtQ4-vUiUl1xSCh8Hf7D6Cme7Lbp9mk385ePc/edit'

    # Extract the document ID from the URL
    try:
        doc_id = extract_doc_id_from_url(doc_url)
    except ValueError as e:
        print(e)
        exit(1)

    # Extract text
    text = get_document_text(doc_id, creds)
    print(text)