# semantic_analysis

This repository contains a minimal requirement management prototype. The goal is
to store software requirements, preprocess them and build simple vector
representations so that related requirements can be discovered when new items
arrive.

## Features
- Bag-of-words embedding built from preprocessed tokens
- Pre-processing pipeline:
  1. lower case conversion
  2. removal of redundant phrases
  3. light lemmatization
  4. stop word removal
  5. enrichment with tags such as `SECURITY` or `PERFORMANCE`
- In-memory graph connecting requirements with cosine similarity above a
  threshold
- Utility to integrate new requirements and return related ones
- Simple benchmark script and unit tests

## Usage
Run the benchmark:
```bash
python benchmark.py
```

Run the unit tests:
```bash
python -m unittest discover -s tests
```
