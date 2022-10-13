<a name="readme-top"></a>

<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/logo.PNG" />
</p>
  <p align="center"> Array based deobfuscation made easier.
    <br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
     <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

On an effort to reduce time consuming deobfuscation analysis, JSDeFr was created initially to automatically deobfuscate array-based techniques (string array replace, array shuffling, array rotate). Having achieved a constant rate of successful deobfuscation, more obfuscation techniques will be added to the toolkit with the goal of creating a framework.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

  ```sh
  pip install -r requirenments.txt
  ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

tldr; 
  ```sh
  python JSDeFr.py -js index.js -o new.js --mode2 --beautify  
  ```

<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/running.PNG" />
</p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Selecting a Mode
Popular obfuscation tools replace intended strings with obfuscated function calls ( eg. 0x4fg312(222) ). The provided argument then is (in most cases) substracted with an established number which I like to call **the magic number**.
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/magic_num.PNG" />
</p>
The result of this logic then is used as index for the correct values array (the secrets array).
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/secrets_array.PNG" />
</p>

Now selecting a mode will depend on performing manual inspection of the script (also, if the incorrect mode is selected you will get an error). This can be done by indentifying the shuffle array logic section of the secript where a group of parseInt calls are made. 
### Mode 1
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/parseint.png" />
</p>

In this example, we can see that inside the parseInt calls, there are calls to the function that returns the value gathered from the secrets array (_0x1c143b(395)).
Mode 1 only works with function calls with one argument.
### Mode 2
Deobfuscating with mode two requires extra steps to be performed after running the script. Since two arguments are present (eg. _0x2ddb23(777, -9911), the one that is used against the magic number must be chosen.

<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/prompt.PNG" />
</p>

<!-- EXAMPLES -->
## Examples
mode1_example3.js_ presents one known bug to be aware.
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/could_not_rotate.PNG" />
</p>

In some occasions, automatic finding of secrets array does not work as intended. One work around is to manually find the secrets array within the script and replace the variable inside JSDeOb.py
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/copy_array.PNG" />
</p>
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/paste_array.PNG" />
</p>
<p align="center">
  <img src="https://github.com/monterrozagera/array_deobfs/raw/master/images/now_rotates.PNG" />
</p>
<!-- ROADMAP -->

## Roadmap

- [ ] Custom Mode (configurable)
- [ ] Control Flow Flatening deobfs
- [ ] Base64 decode

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Gerardo Monterroza - [linkedin](https://www.linkedin.com/in/gerardo-monterroza-8208aa192/) - [github](https://github.com/monterrozagera) - monterrozagerardo@protonmail.com
<p align="right">(<a href="#readme-top">back to top</a>)</p>
