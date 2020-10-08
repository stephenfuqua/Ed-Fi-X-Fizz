# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd  # type: ignore
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)


STUDENT_USER_ROLE = "Student"
TEACHER_USER_ROLE = "Teacher"


def _students_or_teachers_to_users_df(
    students_or_teachers_df: pd.DataFrame, lms_udm_user_role: str
) -> pd.DataFrame:
    """
    Convert a Students or Teachers API DataFrame to a LMSUsers DataFrame

    Parameters
    ----------
    students_or_teachers_df: DataFrame
        is a Students or Teachers API DataFrame
    lms_udm_user_role
        is the LMS UDM user role as a string

    Returns
    -------
    DataFrame
        a LMSUsers DataFrame based on the given Students or Teachers API DataFrame

    DataFrame columns are:
        EmailAddress: The primary e-mail address for the user
        EntityStatus: The status of the record
        LocalUserIdentifier: The user identifier assigned by a school or district
        Name: The full name of the user
        SISUserIdentifier: The user identifier defined in the Student Information System (SIS)
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        UserRole: The role assigned to the user
        CreateDate: Date this record was created
        LastModifiedDate: Date this record was last updated
    """
    assert isinstance(students_or_teachers_df, pd.DataFrame)
    assert "userId" in students_or_teachers_df.columns
    assert "profile.name.fullName" in students_or_teachers_df.columns
    assert "profile.emailAddress" in students_or_teachers_df.columns

    result: pd.DataFrame = students_or_teachers_df[
        ["userId", "profile.name.fullName", "profile.emailAddress"]
    ]
    result = result.rename(
        columns={
            "userId": "SourceSystemIdentifier",
            "profile.name.fullName": "Name",
            "profile.emailAddress": "EmailAddress",
        }
    )

    # Student records are per-course, so there may be duplicates
    result.drop_duplicates(inplace=True)
    result["SourceSystem"] = SOURCE_SYSTEM
    result["UserRole"] = lms_udm_user_role
    result["EntityStatus"] = ENTITY_STATUS_ACTIVE

    result["LocalUserIdentifier"] = ""  # No local id available from API
    result["SISUserIdentifier"] = ""  # No SIS id available from API
    result["CreateDate"] = ""  # No create date available from API
    result["LastModifiedDate"] = ""  # No modified date available from API

    return result


def students_and_teachers_to_users_df(
    students_df: pd.DataFrame, teachers_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert Students and Teachers API DataFrames to an LMS UDM DataFrame

    Parameters
    ----------
    students_df: DataFrame
        is a Students API DataFrame
    teachers_df: DataFrame
        is a Teachers API DataFrame

    Returns
    -------
    DataFrame
        a LMSUsers DataFrame based on the given Teachers API DataFrame

    DataFrame columns are:
        EmailAddress: The primary e-mail address for the user
        EntityStatus: The status of the record
        LocalUserIdentifier: The user identifier assigned by a school or district
        Name: The full name of the user
        SISUserIdentifier: The user identifier defined in the Teacher Information System (SIS)
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
    """
    assert isinstance(students_df, pd.DataFrame)
    assert isinstance(teachers_df, pd.DataFrame)

    assert "userId" in students_df.columns
    assert "profile.name.fullName" in students_df.columns
    assert "profile.emailAddress" in students_df.columns

    assert "userId" in teachers_df.columns
    assert "profile.name.fullName" in teachers_df.columns
    assert "profile.emailAddress" in teachers_df.columns

    users_from_students_df: pd.DataFrame = _students_or_teachers_to_users_df(
        students_df, STUDENT_USER_ROLE
    )
    users_from_teachers_df: pd.DataFrame = _students_or_teachers_to_users_df(
        teachers_df, TEACHER_USER_ROLE
    )

    return pd.concat(
        [users_from_students_df, users_from_teachers_df], ignore_index=True, sort=False
    )
