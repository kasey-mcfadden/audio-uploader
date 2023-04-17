# audio-uploader
Handles audio uploading to internet archive and updating of supabase tables with resulting audio links.

## Setup
Clone this repo locally:
`git clone https://github.com/kasey-mcfadden/audio-uploader.git`

Install python dependencies:
`pip install -r requirements.txt`

Create a `.env` file in the same directory that looks like this:

```
IA_EMAIL=placeholder
IA_PASSWORD=placeholder
S3_ACCESS_KEY=placeholder
S3_SECRET=placeholder
SUPABASE_URL=placeholder
SUPABASE_ANON_KEY=placeholder
AZURE_RESOURCE_NAME=placeholder
AZURE_SUBSCRIPTION_KEY=placeholder
```

Replace with your values and you're good to go.
