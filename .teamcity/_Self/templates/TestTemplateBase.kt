// SPDX-License-Identifier: Apache-2.0
// Licensed to the Ed-Fi Alliance under one or more agreements.
// The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
// See the LICENSE and NOTICES files in the project root for more information.

package _self.templates

import jetbrains.buildServer.configs.kotlin.v2019_2.*
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.freeDiskSpace
import jetbrains.buildServer.configs.kotlin.v2019_2.buildFeatures.swabra
import jetbrains.buildServer.configs.kotlin.v2019_2.buildSteps.powerShell
import jetbrains.buildServer.configs.kotlin.v2019_2.triggers.vcs

open class TestTemplateBase : Template({
    name = "Python Test Template Base Class"
    id = RelativeId("TestTemplateBase")

    artifactRules = "+:%project.directory%/htmlcov => coverage.zip"
    option("shouldFailBuildOnAnyErrorMessage", "true")

    vcs {
        root(DslContext.settingsRoot, "%vcs.checkout.rules%")
    }

    steps {
        powerShell {
            name = "Install Poetry"
            formatStderrAsError = true
            workingDir = "eng"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            scriptMode = script {
                content = """
                    pip install poetry --user
                """.trimIndent()
            }
        }
        powerShell {
            name = "Install"
            formatStderrAsError = true
            workingDir = "eng"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            scriptMode = script {
                content = """
                    python ./build.py install ../%project.directory%
                """.trimIndent()
            }
        }
        powerShell {
            name = "Run Tests with Coverage"
            formatStderrAsError = true
            workingDir = "eng"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            scriptMode = script {
                content = """
                    python ./build.py coverage:html ../%project.directory%
                """.trimIndent()
            }
        }
        powerShell {
            name = "Type Check"
            formatStderrAsError = true
            workingDir = "eng"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            scriptMode = script {
                content = """
                    python ./build.py typecheck:xml ../%project.directory%
                """.trimIndent()
            }
        }
        powerShell {
            name = "Style Check"
            formatStderrAsError = true
            workingDir = "eng"
            executionMode = BuildStep.ExecutionMode.RUN_ON_SUCCESS
            scriptMode = script {
                content = """
                    python ./build.py lint ../%project.directory%
                """.trimIndent()
            }
        }
    }

    features {
        freeDiskSpace {
            id = "jetbrains.agent.free.space"
            requiredSpace = "%build.feature.freeDiskSpace%"
            failBuild = true
        }
        swabra {
            forceCleanCheckout = true
        }
        feature {
            type = "xml-report-plugin"
            param("xmlReportParsing.reportType", "junit")
            param("xmlReportParsing.reportDirs", """
                +:%project.directory%/mypy.xml
            """.trimIndent())
        }
    }
})
