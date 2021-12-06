# hypermodern-python-seed

Generate python seed apps based on `cjolowicz's` [hypermodern-python][1]. Note
that `cjolowicz` has also created a [seed][3] repo. I prefer this one b/c I only
pulled in the ideas that are relevant to the projects I build, today.

## Dependencies

* python3
* [cookiecutter](https://github.com/cookiecutter/cookiecutter)

See [hypermodern-python][1] for further installation instructions. However, for
the repos that are created that use this repo, the build dependencies have been
abstracted into a docker container.

## Quick Start

    cookiecutter https://github.com/ToddG/hypermodern-python-seed

    ...answer the questions

    nox

## Notes

* Not using --require-hashes mode due to [pytype issue 731][2]

# Links
[1]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[2]: https://github.com/google/pytype/issues/731
[3]: https://github.com/cjolowicz/cookiecutter-hypermodern-python