import ast
import fileinput
import json
import re
import urllib.request
from aws_quota.check import ALL_CHECKS

descriptions = {}
services = set()

for chk in ALL_CHECKS:
    if not chk.service_code or not chk.quota_code:
        continue
    try:
        # undocumented way to fetch service quota descriptions, no guarantees this won't change later
        contents = urllib.request.urlopen(
            "https://dt4ho68y70y55.cloudfront.net/en/{}/{}/description".format(
                chk.service_code, chk.quota_code
            )
        ).read()
        data = json.loads(contents.decode("utf-8"))
        descriptions[(data['ServiceCode'], data['LimitCode'])] = data['LimitDescription']
        services.add(data['ServiceCode'],)
    except Exception as e:
        print(
            "Failed to get description for {}/{} : {}".format(
                chk.service_code, chk.quota_code, e
            )
        )

r_desc = re.compile(r"(\s+description\s+=\s).*")
r_service = re.compile(r"\s+service_code\s+=\s(.*)")
r_quota = re.compile(r"\s+quota_code\s+=\s(.*)")

for s in set(services):
    filename = "aws_quota/check/{}.py".format(s)
    if s == "elasticloadbalancing":
        filename = "aws_quota/check/elb.py"
    elif s == "lambda":
        filename = "aws_quota/check/lambdas.py"
    elif s == "iam":
        continue

    try:
        service = None
        quota = None
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                if r_desc.match(line):
                    continue

                find_svc = r_service.findall(line)
                if find_svc:
                    service = ast.literal_eval(find_svc[0])

                find_quota = r_quota.findall(line)
                if find_quota:
                    quota =  ast.literal_eval(find_quota[0])

                print(line, end='')
                if service and quota:
                    dsc = descriptions[(service, quota)]
                    print('    description = "{}"'.format(dsc))
                    service = None
                    quota = None

        
        print("Updated {} description in {}".format(chk.quota_code, filename))
    except Exception as e:
        print(
            "Failed to update description for {}/{} : {}".format(
                chk.service_code, chk.quota_code, e
            )
        )
