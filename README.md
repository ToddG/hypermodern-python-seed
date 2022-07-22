# hypermodern-python-seed

Generate python seed apps based on `cjolowicz's` [hypermodern-python][1]. Note
that `cjolowicz` has also created a [seed][3] repo. I prefer this one b/c I only
pulled in the ideas that are relevant to the projects I build, today. This repo
also builds and runs the code within a Docker container. Abstracting dependencies
makes it faster to get started. That said, it's also totally viable to install the
dependencies locally and not use Docker at all.

## Dependencies

* python3
* [cookiecutter][4]
* Docker

See [hypermodern-python][1] for further installation instructions and a deep dive 
into each of the technoloiges used here (and for a whole lot more technologies that
I opted to omit). 

## Quick Start

    cookiecutter https://github.com/ToddG/hypermodern-python-seed

    ...answer the questions

    cd [created directory]
    ./scripts/build-container.sh
    ./scripts/run-command.sh    
    firefox docs/_build/html/index.html


## Notes

* Check out the README in the created directory for further context and commands.

# Links

* [hypermodern-python][1]
* [hypermodern-python-seed repo][3]
* [pytype issues][2]
* [cookiecutter][4]

[1]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[2]: https://github.com/google/pytype/issues/731
[3]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[4]: https://github.com/cookiecutter/cookiecutter
