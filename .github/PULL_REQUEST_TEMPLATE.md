<!--
SPDX-FileCopyrightText: Copyright (C) Siemens AG 2023
SPDX-License-Identifier: MIT
-->

## Do you want to contribute code? ##

Thanks for your interest in contributing. Anybody is free to propose any changes to this repository using Pull Requests. We appreciate every Pull Request, but merging cannot be guaranteed. Before you submit your code, please check the following prerequisites: 
 
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

## Thank you! ##