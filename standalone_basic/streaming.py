import requests

r = requests.get('https://d6886867-65e1-427f-891f-096e62a49f59-bluemix:5350511abb6e5fa9f439e7a9f324ec56643fda233c87fe9b6459ed4fe70c879c@d6886867-65e1-427f-891f-096e62a49f59-bluemix.cloudant.com/authdb/_changes?feed=continuous', stream=True)

for line in r.iter_lines():

    # filter out keep-alive new lines
    if line:
        decoded_line = line.decode('utf-8')
        print(decoded_line)
