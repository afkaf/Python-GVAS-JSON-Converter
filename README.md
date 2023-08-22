---

# Python-GVAS-JSON-Converter

Python-GVAS-JSON-Converter is a library designed to convert Unreal Engine's Game Variable and Attribute System (GVAS) files between `.sav` and `.json` formats. It provides a way to read and interpret the binary structure of `.sav` files and translate them into human-readable JSON format.

## Features

- **Convert from .sav to .json**: The library currently supports converting Unreal Engine's `.sav` files into `.json` format.
- **Tested Games**: The conversion has been tested with Crab Champions, and it may work for other games as well.
- **Work in Progress**: This project is actively being developed, with new features and improvements being added.

## Upcoming Features

- **Convert back to .sav**: Work is underway to enable the conversion of JSON files back to the original `.sav` format.

## Warning

- **Untested .sav Files**: Some classes in `SavProperties.py` may not function correctly with untested `.sav` files, and certain `SavReader.py` code segments may be broken for untested datatypes. While the library has been designed with flexibility in mind, full compatibility with all `.sav` files cannot be guaranteed at this stage. I will be progressively testing other games' `.sav` files and refining the code accordingly.

---
