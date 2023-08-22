---

# Python-GVAS-JSON-Converter

Python-GVAS-JSON-Converter is a library designed to convert Unreal Engine's Game Variable and Attribute System (GVAS) files between `.sav` and `.json` formats. It provides a way to read and interpret the binary structure of `.sav` files and translate them into human-readable JSON format, as well as convert JSON back to the original `.sav` format.

## Features

- **Convert from .sav to .json**: Supports converting Unreal Engine's `.sav` files into `.json` format.
- **Convert from .json to .sav**: Includes the ability to convert `.json` files back to the original `.sav` format.
- **Tested Games**: The conversion has been tested with Crab Champions, and it may work for other games as well.
- **Actively Developed**: This project is actively being developed, with new features and improvements being added.

## Warning

- **Untested .sav Files**: Some classes in [SavProperties.py](SavConverter/SavProperties.py) may not function correctly with untested `.sav` files, and certain [SavReader.py](SavConverter/SavReader.py) code segments may be broken for untested datatypes. While the library has been designed with flexibility in mind, full compatibility with all `.sav` files cannot be guaranteed at this stage. Efforts will continue to progressively test other games' `.sav` files and refine the code accordingly.

---
