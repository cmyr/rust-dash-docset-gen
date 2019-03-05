# Generating Dash docsets for third party rust crates

This repo contains a simple script for quickly generating Dash compatible docsets for third-party Rust crates.

## Requirements

- python3
- the requests library: `pip3 install requests`
- [dashing](https://github.com/technosophos/dashing): `brew install dashing`
- [rsdocs-dashing](https://github.com/hobofan/rsdocs-dashing): `cargo install rsdocs-dashing`

## Usage

`./gen_docsets.py serde crossbeam rand log regex`

This will clone the repos for these crates (assuming the name passed is used on [crates.io](https://crates.io),
generate the docsets, and copy them into the `docsets` subdir. These `.docset` files can be added to Dash in
dash's preferences.
