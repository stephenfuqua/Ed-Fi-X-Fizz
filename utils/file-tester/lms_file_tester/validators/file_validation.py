# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import re
import sys
from typing import List

import pandas as pd

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
sys.path.append(os.path.join("..", "..", "src", "file-utils"))
from lms_file_utils import file_reader as fread  # type: ignore # noqa: E402


date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def _validate_columns(expected: set, df: pd.DataFrame, file_type: str) -> List[str]:
    actual = set(df.columns)

    if actual == expected:
        return list()

    extra = actual.difference(expected)
    missing = expected.difference(actual)

    # introduce a temporary type check error
    extra_msg = str(extra) if len(extra) > 0 else "{none}"
    missing_msg=str(missing) if len(missing) > 0 else "{none}"

    return [
        f"{file_type} file contains extra columns {extra_msg} and is missing columns {missing_msg}"
    ]


def _file_is_empty(file_type: str) -> List[str]:
    return [f"{file_type} file could not be read or the file does not exist."]


def _validate_date_formats(
    df: pd.DataFrame, file_type: str
) -> List[str]:
    errors: List[str] = list()

    cols = list(df.columns)

    for column in [c for c in cols if (c.endswith("Date") or c.endswith("DateTime"))]:
        test_value = df.iloc[0][column]
        if pd.notna(test_value) and date_pattern.match(str(test_value)) is None:
            errors.append(f"{file_type} file has an invalid timestamp format for {column}")

    return errors


def validate_users_file(input_directory: str) -> List[str]:
    """
    Validates that the latest users file has the expected columns and all
    columns whose names end with `Date` or `DateTime` have the proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_users(input_directory, nrows=2)

    if df.empty:
        return _file_is_empty("Users")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "UserRole",
            "LocalUserIdentifier",
            "SISUserIdentifier",
            "Name",
            "EmailAddress",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Users"
    ) + _validate_date_formats(df, "Users")


def validate_sections_file(input_directory: str) -> List[str]:
    """
    Validates that the latest sections file has the expected columns and all
    columns whose names end with `Date` or `DateTime` have the proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_sections(input_directory, nrows=2)

    if df.empty:
        return _file_is_empty("Sections")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "SISSectionIdentifier",
            "Title",
            "SectionDescription",
            "Term",
            "LMSSectionStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Sections"
    ) + _validate_date_formats(df, "Sections")


def validate_system_activities_file(input_directory: str) -> List[str]:
    """
    Validates that the latest system activities file has the expected columns and all
    columns whose names end with `Date` or `DateTime` have the proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_system_activities(input_directory, nrows=2)

    if df.empty:
        return _file_is_empty("System Activities")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "LMSUserSourceSystemIdentifier",
            "ActivityDateTime",
            "ActivityType",
            "ActivityStatus",
            "ParentSourceSystemIdentifier",
            "ActivityTimeInMinutes",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "System Activities"
    ) + _validate_date_formats(df, "System Activities")


def validate_section_associations_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    """
    Validates that the latest section associations file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    sections: pd.DataFrame
        DataFrame containing section information read from a Sections file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_section_associations(input_directory, sections, nrows=2)

    if df.empty:
        return _file_is_empty("Section Associations")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "EnrollmentStatus",
            "StartDate",
            "EndDate",
            "LMSUserSourceSystemIdentifier",
            "LMSSectionSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Section Associations"
    ) + _validate_date_formats(df, "Section Associations")


def validate_section_activities_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    """
    Validates that the latest section activities file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    sections: pd.DataFrame
        DataFrame containing section information read from a Sections file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_section_activities(input_directory, sections, nrows=2)

    if df.empty:
        return _file_is_empty("Section Activities")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "ActivityType",
            "ActivityDateTime",
            "ActivityStatus",
            "MessagePost",
            "TotalActivityTimeInMinutes",
            "LMSSectionSourceSystemIdentifier",
            "UserSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Section Activities"
    ) + _validate_date_formats(df, "Section Activities")


def validate_assignments_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    """
    Validates that the latest assignments file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    sections: pd.DataFrame
        DataFrame containing section information read from a Sections file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_assignments(input_directory, sections, nrows=2)

    if df.empty:
        return _file_is_empty("Assignments")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Title",
            "AssignmentCategory",
            "AssignmentDescription",
            "StartDateTime",
            "EndDateTime",
            "DueDateTime",
            "SubmissionType",
            "MaxPoints",
            "LMSSectionSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Assignments"
    ) + _validate_date_formats(df, "Assignments")


def validate_submissions_file(
    input_directory: str, assignments: pd.DataFrame
) -> List[str]:
    """
    Validates that the latest submissions file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    assignments: pd.DataFrame
        DataFrame containing assignments information read from a Assignments file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_submissions(input_directory, assignments, nrows=2)

    if df.empty:
        return _file_is_empty("Submissions")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "SubmissionStatus",
            "SubmissionDateTime",
            "EarnedPoints",
            "Grade",
            "AssignmentSourceSystemIdentifier",
            "LMSUserSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Submissions"
    ) + _validate_date_formats(df, "Submissions")


def validate_grades_file(input_directory: str, sections: pd.DataFrame) -> List[str]:
    """
    Validates that the latest grades file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    sections: pd.DataFrame
        DataFrame containing section information read from a Sections file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_grades(input_directory, sections, nrows=2)

    if df.empty:
        return _file_is_empty("Grades")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Grade",
            "GradeType",
            "LMSUserLMSSectionAssociationSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Grades"
    ) + _validate_date_formats(df, "Grades")


def validate_attendance_events_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    """
    Validates that the latest attendance events file has the expected
    columns and all columns whose names end with `Date` or `DateTime` have the
    proper format.

    Parameters
    ----------
    input_directory: str
        Base / parent directory containing files created by an LMS extractor.
    sections: pd.DataFrame
        DataFrame containing section information read from a Sections file.

    Returns
    -------
    List[str]
        List containing detailed error messages, if any.
    """
    df = fread.get_all_attendance_events(input_directory, sections, nrows=2)

    if df.empty:
        return _file_is_empty("Attendance Events")

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "EventDate",
            "AttendanceStatus",
            "LMSSectionAssociationSystemIdentifier",
            "LMSUserSourceSystemIdentifier",
            "LMSUserLMSSectionAssociationSourceSystemIdentifier",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(
        expected, df, "Attendance Events"
    ) + _validate_date_formats(df, "Attendance Events")
