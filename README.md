Bash Generator
===================

A simple Bash template generator using `getopts` . This only supports single character flags(short flags like `-a` etc). 

At maximum you can get a bash script having complexity up to 
```
gen_script.sh [-c | -d param1 |-e param2] -f -g param3
```
i.e 

* Flag without argument parameter. (like `-f` `-c`)
* Flag with single argument. ( like `-g param3`, `-d param1`,`-e param2`)
* Mutually exclusive flags containing both *Flag without argument parameter* and *Flag with single argument*. ( like `-c | -d param1 |-e param2`). It implies that only one of the flag out of `c, d, e` can be used in a specific run.


----------


Requirements
-------------
> Needs **Python 3** and can be run on console.

Usage
-------------

### Explanation
The program may ask following questions
```
Choose your argument type(1/2/3/0 without '.')
1. Flag option, having no following argument like "b" in `cmd -b`.
2. Argument option, having one following option like "c" in `cmd -b -c param1`.
3. Mutually exclusive parameters, combination of above 1 & 2 like `cmd [-b|-c param1|-d param2] `.
0. To break out
```
- If you input `1`: You are opting for a flag without argument.
- If you input `2`: You are opting for a flag with single argument.
- If you input `3`: You are opting for mutually exclusive flags explained above.
- If you input `0`: You are opting for no more parameters and program will proceed for dumping the generated template.

##### Lets see what happens if you input `2`

- Enter Flag value (single character):    **r**

This will be the flag. In this case `-r`

- Enter name for function (default = r_func):     **replace_names**

This will be the name of the function that will be called when `-r` is passed on command line. In this case it generates
```
replace_name() {
    local param_replace_names=$1
    err "Unimplemented -r (replace_names) with param $param_replace_names"
}
```
and in the case statement
```
r)
   replace_names "$OPTARG"
   ;;
```

- PROTOTYPE for argument (default = < ANY >):       **<'@' joined file names>**

This is for help section. And in this case will generate 
```
Usage: ${0##*/} -r <'@' joined file names>
```

- Tell what this option does (default = < TODO >):  **replaces file name from -i list with this list (position wise)**

Again for help section and will generate
```
    -r	replaces file name from -i list with this list (position wise)
```

- If all is fine above should I commit?    (Y/n): 

Most important question. A capital implies default assumption. If  `n` is entered it will forget all the inputs for the *current flag*. This is here to rescue when a faulty input has been given in any previous question. So if you choose `n` in current case, `-r` flag will be forgotten and can be re-entered again.

##### Special question with Mutex
```
Now choose one of them(1/2/7/0 without '.')
1. Flag parameters, no options.
2. Argument parameters, having one parameter.
7. (dangerous)**Clear mutex entries in this session**
0. To break out
```
- *Clear mutex entries in this session* : Implies all the mutually exclusive parameters entered after choosing `3` in main question  will be forgotten. However it will not forget any other mutexes entered before choosing this mutex.




### Examples

Have a look inside examples folder. Here is what each file has

- `pdfjoin.sh.html`: Console snapshot on my computer. Text in bold *Indian Red* is input.
- `pdfjoin.sh`: The generated template
- `postPdfJoin.sh`: The complete script built on template
- `inp.txt`: Inputs dump (used in creation of `pdfjoin.sh` template)

### Automation and Editing

In case, there is a need to alter an earlier generated script, a short hand method is available without repeating the lengthy generation process once again. The script is self aware of inputs that generated it which can be dumped using `--dumpinput` flag.
```
./pdfjoin.sh --dumpinput > inp.txt
```
Modify the contents of *inp.txt* , **specially output file name**, otherwise it will **overwrite previously generated file** and you can **lose** your added content.
Finally run:
```
./gbash.py <inp.txt
```


Todo
--------------
- The script has limitations of getopts i.e. long flags are not supported (like `--version`). In future versions this limitation has to be overcome.
-  Adding support for python 2.
- More options in generation like handling stdin and stdout etc.


Copyrights
---------------
No jokes please. 


