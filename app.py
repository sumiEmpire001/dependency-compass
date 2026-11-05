"""Inspect pinned Python package requirements in a JSON dependency manifest."""
import argparse
import json
import re
import sys

NAME=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
VERSION=re.compile(r"^[0-9]+(?:\.[0-9]+)*(?:[a-zA-Z0-9.+-]*)$")

def analyze(data):
    packages=data.get("packages",[])
    if not isinstance(packages,list): raise ValueError("packages must be an array")
    issues=[]
    seen=set()
    for index,pkg in enumerate(packages):
        if not isinstance(pkg,dict): raise ValueError("each package must be an object")
        name=pkg.get("name","")
        version=pkg.get("version","")
        if not isinstance(name,str) or not NAME.fullmatch(name):
            issues.append({"index":index,"issue":"invalid name"})
            continue
        normalized=re.sub(r"[-_.]+","-",name).lower()
        if normalized in seen: issues.append({"index":index,"issue":"duplicate package"})
        seen.add(normalized)
        if not isinstance(version,str) or not VERSION.fullmatch(version):
            issues.append({"index":index,"issue":"missing or non-exact version"})
    return {"healthy":not issues,"packages":len(packages),"issues":issues}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Check dependency manifest hygiene")
    parser.add_argument("manifest")
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args(argv)
    try:
        with open(args.manifest,encoding="utf-8") as f: data=json.load(f)
        if not isinstance(data,dict): raise ValueError("manifest must be an object")
        report=analyze(data)
    except (OSError,ValueError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2
    print(json.dumps(report,indent=2))
    return 0 if report["healthy"] else 1

if __name__=="__main__": raise SystemExit(main())
