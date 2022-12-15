import requests
import json
import os
import argparse

parser = argparse.ArgumentParser(description='Pk results file saver')
parser.add_argument('--pks', nargs="*", type=str, default=[], help='list of PKs to get the result from')

def get_result_file(pk_list):
    for pk in pk_list:
        url=f"https://ars-prod.transltr.io/ars/api/messages/{pk}?trace=y"
        r = requests.get(url)
        parent_rj = r.json()
        with open(f'{pk}.json', "w") as outfile:
            result_list = []
            for child in parent_rj['children']:
                child_pk=child['message']
                url=f"https://ars-prod.transltr.io/ars/api/messages/{child_pk}"
                try:
                    response = requests.get(url)
                    child_rj = response.json()
                except HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')
                except JSONDecodeError:
                    print('Response could not be serialized')  

                result_list.append(child_rj)
            json.dump(result_list, outfile, indent=4) 


def main():
    args = parser.parse_args()
    pk_list = getattr(args,"pks")
    get_result_file(pk_list)


if __name__== '__main__':
    main()