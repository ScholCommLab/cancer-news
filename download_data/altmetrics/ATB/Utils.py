# -*- coding: utf-8 -*-
"""Utils

Collection of helper functions

author: Asura Enkhbayar <asura.enkhbayar@gmail.com>
"""

import requests

# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


# Retrieve App Access Token
# ToDo: improve error handling
def resolve_doi(doi):
    """
    Simple function to resolve a DOI via CrossRef
    """
    try:
        response = requests.head('https://doi.org/{}'.format(doi), allow_redirects=True, timeout=3)
        return response.url
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.TooManyRedirects:
        return 'tooManyRedirects'
    except requests.exceptions.RequestException:
        return 'RequestException'
