#!/usr/bin/env python3

import argparse
import requests
import os
import sys
import subprocess
import shutil

SOURCE_SUBDIR = "crates"
DOCSET_SUBDIR = "docsets"
CRATES_API = "https://crates.io/api/v1/crates/"

def gen_docset(crate_name):
    """generates or updates the docset for this crate."""

    repo = get_repo_url(crate_name)
    if repo is None:
        raise Exception("no repo returned for {}".format(crate_name))
    print("generating docs for {} from {}".format(crate_name, repo))
    local_path = repo.split('/')[-1]
    if not os.path.exists(local_path):
        clone_repo(repo)
    return update_docs(local_path, crate_name)


def get_repo_url(crate_name):
    """gets the url for the repository associated with `crate_name` on crates.io"""

    crates_path = "https://crates.io/api/v1/crates/" + crate_name
    headers = {'user-agent': '@cmyr\'s dash docset generation, colin@cmyr.net'}
    resp = requests.get(crates_path, headers=headers)
    if resp.status_code != 200:
        raise "crates.io returned %d for %s" % (resp.status_code, crate_name)
    json = resp.json()
    return json["crate"]["repository"]

    
def clone_repo(repo_path):
    subprocess.check_call("git clone {}".format(repo_path), shell=True)
    print("cloned {}".format(repo_path))

    
def update_docs(crate_dir, crate_name):
    os.chdir(crate_dir)
    try:
        subprocess.check_call("git diff-index --quiet HEAD --", shell=True)
    except subprocess.CalledProcessError:
        raise "crate {} has dirty working directory, will not update".format(crate_dir)

    # head_sha = resolve_rev("HEAD")
    subprocess.check_call("git fetch && git checkout origin/master", stdout=sys.stdout, shell=True)
    print("updated {} to origin/master".format(crate_name))
    # master_sha = resolve_rev("origin/master")
    # if head_sha == master_sha and os.path.exists(os.path.join(crate_dir, "target", "doc")):
    #     raise Exception("crate {} unchanged, will not update".format(crate_name))

    subprocess.check_call("cargo doc", shell=True, stdout=sys.stdout)
    subprocess.check_call("rsdocs-dashing target/doc/{} docset".format(crate_name), stdout=sys.stdout, shell=True)
    subprocess.check_call("dashing build --config docset/dashing.json --source docset/build".format(crate_name), stdout=sys.stdout, shell=True)
    docset_path = os.path.join(os.getcwd(), "{}.docset".format(crate_name))
    return docset_path


def resolve_rev(rev_id):
    """Given an arbitrary git revision id, returns the commit's hash"""
    output = subprocess.check_output("git rev-parse {}".format(rev_id), shell=True)
    return output.decode('utf-8').strip()


def main():
    parser = argparse.ArgumentParser(description='create or update a dash docset')
    parser.add_argument(
        'crate_names',
        type=str,
        nargs='+',
        help='a list of crate names to generate or update docs for')
    
    args = parser.parse_args()
    base_dir = os.getcwd()
    out_dir = os.path.join(base_dir, DOCSET_SUBDIR)
    source_dir = os.path.join(base_dir, SOURCE_SUBDIR)
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
    
    for crate in args.crate_names:
        os.chdir(source_dir)
        print("generating docs for", crate)
        try:
            docset_path = gen_docset(crate)
            dest_path = os.path.join(out_dir, os.path.split(docset_path)[-1])
            assert dest_path.endswith(".docset")
            shutil.move(docset_path, dest_path)
            print("updated", dest_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
