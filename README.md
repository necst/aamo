AAMO: Another Android Malware Obfuscator
========================================

We release our set of code-obfuscation scripts tailored for Android
applications. We assume that the original application can be disassembled into
Smali.


Obfuscation Operators
---------------------

We currently support:

* Android specific
  * Repackaging
  * Reassembly
  * Re-alignment

* Simple control-flow modifications
  * Junk code insertion
  * Debug symbols stripping
  * Defunct code insertion
  * Unconditional jump insertion

* Advanced control-flow modifications
  * Call indirection
  * Code reordering
  * Reflection
  * Opaque predicate insertion

* Renaming
  * Non-code files and resource renaming
  * Fields and methods renaming
  * Package renaming

* Encryption
  * Resource encryption (asset files)
  * Native code encryption
  * Data encryption (strings)


Contributors
------------

* Federico Pellegatta (main developer)
* [Federico Maggi](https://github.com/phretor) (advisor, maintainer)
* [Mila Dalla Preda](https://profs.sci.univr.it/~dallapre) (advisor, contributor)


Support
-------

AAMO is supported by the [FACE][1] research project, under the FIRB 2013
funding program of the Italian Ministry of University and Research.


[1]:  http://www.face-project.it        “FACE: Formal Avenue for Chasing malwarE”
