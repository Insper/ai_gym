# Change log

All notable changes to this project will be documented in this file.

## [0.3.6] 2026-09-02

### Added

### Changed

### Fixed

makelabel function getting a tuple instead of a node



## [0.3.5] 2026-09-02

### Added

Replay function that simulates the graph search after the search has been done. (Faster than live tracing)

### Changed

### Fixed

## [0.3.4] 2026-08-25

### Added

### Changed

Removed all documentations and code related to parallel search
Improved custom.css
Add cron job to build and fetch data on build
Script that fetches contributors data
Custom script to add dinamicaly the contributors to the HTML

### Fixed

## [0.3.3] 2026-08-21

### Added

Added a stop function to the trace graph
Added detailed to methods in VacuumWorldGeneric.py example
Added detailed descriptions to methods in U2.py example
Added detailed to methods in Puzzle8.py example

### Changed

Changed examples text to english

### Fixed

Fixed AEstrela tuple return to trace_graph function

## [0.3.2] 2026-08-12

### Added

Heuristic and CPS State descritpion
Prunning descriptions
A redirect to Examples page

### Changed

Algorithm -> Class table refacted with a more descriptive usage

### Fixed

Wrong type of algorithm shown on the algorithm usage example

## [0.3.1] 2026-08-10

### Added

A tutorial on how to install the trace feature

### Changed

### Fixed

Fixed multiples instances of diplay on tracing to one display and later updating

## [0.3.0] 2026-04-08

### Added

A wrapper that runs any other search algorithm in parallel, 
distributing the workload across all CPU cores of the machine.

### Changed

### Fixed

## [0.2.6] 2026-01-26

### Added

### Changed

### Fixed

Add type hints fix pylint warnings and format files

## [0.2.5] 2025-09-12

### Added

* The graphviz dependency in the README.md file.

### Changed

* The version of the package in the `setup.py` file.

### Fixed


## [0.2.4] 2025-08-31

### Added

* Graphical visualization of search algorithm tracing

### Changed

### Fixed


## [0.2.2] 2025-01-28

### Added

### Changed

* Refactor all code to use the pylint standard
* Remove the unnecessary code in examples files

### Fixed


## [0.2.0] 2024-09-04

### Added

* A new form of tracing the search algorithms

### Changed

* Refactor search module interface for cleaner interaction
* Using sets to lower time complexity on general pruning

### Fixed

## [0.1.9] 2023-10-02

### Added

### Changed

### Fixed

* Fixed bug in A* algorithm.

## [0.1.7] 2023-09-21

### Added

* CD/CI workflow with GitHub Actions to deploy this package to PyPI. None feature added.

### Changed

### Fixed


## [0.1.6] 2023-09-20

### Added

### Changed

### Fixed

* Fixed bug in Uniform Cost Search algorithm.


## [0.1.5] 2023-09-18

### Added

* Pruning option in search method for all algorithms in SearchAlgorithms.py. 

### Changed

### Fixed
