<!--
Copyright (C) 2023 Siemens AG

SPDX-License-Identifier: MIT
-->

# Contributions to Industrial Edge Device Kit are always welcome! #

## Did you find a bug? ##

* Ensure the bug was not already reported by searching the [open issues](https://github.com/industrial-edge/reference-architecture-for-industrial-ai-on-azure/issues).
* Check the [closed issues](https://github.com/industrial-edge/reference-architecture-for-industrial-ai-on-azure/issues?q=is%3Aissue+is%3Aclosed) for solutions to problems other users had.
* If you're unable to find an issue addressing your problem, open a new issue.
* Be sure to include a clear title and a clear description, log files, screenshots, code samples and/or executables so that we can understand and reproduce the problem.

## Do you want to contribute code? ##

Thanks for your interest in contributing. Anybody is free to propose any changes to this repository using Merge Requests. We appreciate every Merge Request, but merging cannot be guaranteed. Before you submit your code, please check the following prerequisites: 
 
* use git to manage your changes [*recommended*]
* please follow common code conventions
* add the required copyright header to each new file introduced
* structure patches logically, in small steps [**required**]
    * one separable functionality/fix/refactoring = one patch
    * do not mix those three into a single patch (e.g. first refactor, then
      add a new functionality that builds onto the refactoring)
    * after each patch, the tree still has to build and work, i.e. do not add
      even temporary breakages inside a patch series (helps when tracking down
      bugs)
    * use `git rebase -i` to restructure a patch series
* test patches sufficiently (obvious, but...) [**required**]
* you have to sign the [Siemens Contributor License Agreement](https://cla-assistant.io/industrial-edge/) which is provided in the repository and send it via email

# Thank you! #
