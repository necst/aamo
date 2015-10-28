AAMO: Another Android Malware Obfuscator
========================================

We release our set of code-obfuscation scripts tailored for Android
applications. We assume that the original application can be disassembled into
Smali.


Usage
-----

    $ mkdir dir_with_apks_to_obfuscate/     # fill the dir with some APKs
    $ vim obfuscators/obfuscators.py

Set the `obfuscator_to_apply` variable to define the list of obfuscators you
want to apply. For example:

    obfuscator_to_apply = [
        'Resigned',
        'Alignment',
        'Rebuild',
        'Fields',
        'Debug',
        'Indirections',
        'Defunct',
        'StringEncrypt',
        'Renaming',
        'Reordering',
        'Goto',
        'ArithmeticBranch',
        'Nop',
        'Asset',
        'Intercept',
        'Raw',
        'Resource',
        'Lib',
        'Restring',
        'Manifest',
        'Reflection']

You can choose a subset of obfuscators (recommended).

    $ python obfuscators/obfuscators.py

Enjoy your obfuscated APKs.


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


Bugs
----

There might be plenty of bugs. Feel free to fork and send us pull requests!


Contributors
------------

* Federico Pellegatta (main developer)
* [Federico Maggi](https://github.com/phretor) (advisor, maintainer)
* [Mila Dalla Preda](https://profs.sci.univr.it/~dallapre) (advisor, contributor)


Support
-------

AAMO is supported by the [FACE](http://www.face-project.it) research project,
under the FIRB 2013 funding program of the Italian Ministry of University and
Research (grant agreement N. RBFR13AJFT).
