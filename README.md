# rateboard
Displays times, currency pairs and bitcoin rates from multiple public sources

Requires:
- Python 2.7+ (tested on Raspberry Pi3 running jessie)
- PyQt4
- simplejson

Operation:
$ python rateboard-main &

- refreshes each widget on a random interval to avoid spamming public APIs
- rotates background color (R key advances)
- Q key quits

Notes:
- wait 10-15 minutes for rates to appear - respects the API providers by not hitting them all at once
- No guarantees as to the semantic meaning or accuracy of the data pulled from various APIs
- Expect API providers will to change the APIs and break widgets occasionally (do your own maintenance, contribs welcome)
- author(s) may change rateboard code in unexpected and temporarily broken ways without warning, notification or contrition

Donations: 1JCGwHgWNioGgyA52HFnKNfKBtEux2RSwj
