# Generating Dash docsets for third party rust crates

This repo contains a simple script for quickly generating Dash compatible docsets for third-party Rust crates.

## Requirements

- python3
- the requests library: `pip3 install requests`
- [rsdocs-dashing](https://github.com/hobofan/rsdocs-dashing): `cargo install rsdocs-dashing`
- [dashing](https://github.com/technosophos/dashing): `brew install dashing`

## Usage

`./gen_docsets.py serde crossbeam rand log regex`

This will clone the repos for these crates, generate the docsets, and copy them into the `docsets` subdir.
