# Dead simple package manager for minecraft.
mcpm is a package manager that gets mods from modrinth, one of it's strengths
is that it can handle multiple folders, and it has a very small codebase, mcpm is just a python script!, with 2 json files, ofc.

Setup:
first, install fabric, forge, etc.<br/>
Then, install the binary *must include the json files!*<br/>
then run this command:
```bat
$ mcpm add <NAMEOF DIRECTORY> <DIRECTORY TO MODS FOLDER>
; mcpm add fabric-1.18.2 %APPDATA%\.minecraft\<nameof mods folder, for example, 'fabric-mods'.> 
```

After that, you can install mods with:
```bat
$ mcpm install <MOD> <nameof directory, in this example, fabric-1.18.2>
```

removing mods is the exact same syntax as 'install', but you use 'remove' instead of 'install'.

list shows all installed mods:
```bat
$ mcpm list <nameof directory, in this example, fabric-1.18.2>
```

check tests if the mod is installed:
```bat
$ mcpm check <MOD> <nameof directory, in this example, fabric-1.18.2>
```

info shows info about the mod:
```bat
$ mcpm info <MOD>
```

examples:
```bat
$ mcpm add fabric-1.18.2 C:\Users\ME\AppData\Roaming\.minecraft\mods
$ mcpm install sodium fabric-1.18.2
$ mcpm remove sodium fabric-1.18.2
$ mcpm list fabric-1.18.2
$ mcpm check sodium fabric-1.18.2
$ mcpm info sodium
```