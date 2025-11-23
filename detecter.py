import sys
from googleapiclient.discovery import build 

def predict_phishing(url, api_key):
    """
    Checks a URL using the Google Safe Browsing API v4.
    Returns "Phishing/Malware" or "Legitimate".
    """
    try:
        service = build('safebrowsing', 'v4', developerKey=api_key)
    except Exception as e:
        print(f"  > Error building service: {e}")
        print("  > (Did you 'pip install google-api-python-client'?)")
        return "Unknown (Client Error)"

    body_to_check = {
        'client': {
            'clientId':      "my-phishing-detector",
            'clientVersion': "1.0.0"
        },
        'threatInfo': {
            'threatTypes':      ["SOCIAL_ENGINEERING", "MALWARE", "UNWANTED_SOFTWARE"],
            'platformTypes':    ["ANY_PLATFORM"],
            'threatEntryTypes': ["URL"],
            'threatEntries': [
                {'url': url}
            ]
        }
    }

    try:
        request = service.threatMatches().find(body=body_to_check)
        response = request.execute()

        if response.get('matches'):
            threat_type = response['matches'][0]['threatType']
            print(f"  > Detected as: {threat_type}")
            return "Phishing/Malware"
        else:
            return "Legitimate"

    except Exception as e:
       
        print(f"  > Error during API call: {e}")
        return "Unknown (API Error)"

if __name__ == "__main__":
    
    API_KEY = "enter your api key" 
    
    if API_KEY == "PASTE_YOUR_GOOGLE_API_KEY_HERE":
        print("API Key not set!")
        print("   Get one from the Google Cloud Console.")
    else:
        print("API Key is active")
        print("   Enter a URL to check. Type 'exit' or 'q' to quit.\n")
        
        while True:
            url_to_check = input("Enter a URL to check: ") 

            if url_to_check.lower() in ["exit", "q"]:
                print("Exiting detector.")
                break 
            
            if not url_to_check:
                continue

            result = predict_phishing(url_to_check, API_KEY)
            print(f"  → Result: {result}\n" + ("-"*30))
