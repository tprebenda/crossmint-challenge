# Crossmint Challenge

This repo was created for the Crossmint coding challenge, currently including Phase 1.

Phase 2 contains the required POLYanet configuration, but I was unable to determine the pattern to 
programmatically create the SOLoon and comETH entities without explicitly providing coordinates, so they are
not included.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

I have included a `requirements.txt` file that you can use to install the required packages, like so:

```bash
pip install -r requirements.txt
```

## Usage

Invoke the main script with the intended Phase as a command line argument, like so:

Phase 1:

```bash
python main.py phase1
```

Phase 2:

```bash
python main.py phase2
```


## Limitations

The project correctly creates the X-shape for Phase 1 of the challenge, but I was only able to create the 
Crossmint logo shape with POLYanets for Phase 2.

I could not discern a pattern for SOLoons and comETHs, so they are not generated by the program.