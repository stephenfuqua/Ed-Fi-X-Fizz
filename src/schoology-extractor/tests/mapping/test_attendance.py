# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from schoology_extractor.mapping.attendance import map_to_udm


def describe_when_mapping_empty_list():
    def it_should_return_empty_DataFrame():
        result = map_to_udm(list(), pd.DataFrame())

        assert result.empty


def describe_when_mapping_Schoology_list_to_EdFi_DataFrame():
    @pytest.fixture
    def result() -> pd.DataFrame:
        attendance_events = [{
            "date": "2020-08-28",
            "statuses": {
                "status": [
                    {
                        "status_code": 1,
                        "attendances": {
                            "attendance": [
                                {
                                    "enrollment_id": 12345,
                                    # This year is deliberately different from the one above, only for testing purposes
                                    "date": "2021-08-28",
                                    "status": 1,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12346,
                                    "date": "2022-08-28",
                                    "status": 2,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12347,
                                    "date": "2023-08-28",
                                    "status": 3,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12348,
                                    "date": "2024-08-28",
                                    "status": 4,
                                    "comment": "",
                                },
                            ]
                        }
                    }
                ]
            },
        }]

        section_associations = [
            {
                "SourceSystemIdentifier": 12345,
                "LMSUserSourceSystemIdentifier": 5678,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
                "CreateDate": None,
                "LastModifiedDate": None
            },
            {
                "SourceSystemIdentifier": 12346,
                "LMSUserSourceSystemIdentifier": 5677,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
                "CreateDate": None,
                "LastModifiedDate": None
            },
            {
                "SourceSystemIdentifier": 12347,
                "LMSUserSourceSystemIdentifier": 5676,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
            },
            {
                "SourceSystemIdentifier": 12348,
                "LMSUserSourceSystemIdentifier": 5675,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
            },
        ]

        # Arrange
        section_associations = pd.DataFrame(section_associations)

        # Act
        return map_to_udm(attendance_events, section_associations)

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 8

    def it_should_have_schoology_as_source_system(result):
        assert result["SourceSystem"].iloc[0] == "Schoology"

    def it_should_map_enrollment_id_and_date_to_source_system_identifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == "12345#2020-08-28"

    def it_should_map_date_to_event_date(result):
        assert result["EventDate"].iloc[0] == "2020-08-28"

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] == ""

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] == ""

    @pytest.mark.parametrize(
        "index,expected", [(0, "present"), (1, "absent"), (2, "late"), (3, "excused")]
    )
    def it_should_map_attendance_status_1_to_present(result, index, expected):
        assert result["AttendanceStatus"].iloc[index] == expected

    @pytest.mark.parametrize(
        "index,expected", [(0, 5678), (1, 5677), (2, 5676), (3, 5675)]
    )
    def it_should_map_lms_user_source_system_identifier_from_section_association(
        result, index, expected
    ):
        assert result["LMSUserSourceSystemIdentifier"].iloc[index] == expected

    @pytest.mark.parametrize("index,expected", [(0, 555), (1, 555), (2, 555), (3, 555)])
    def it_should_map_lms_section_source_system_identifier_from_section_association(
        result, index, expected
    ):
        assert result["LMSSectionSourceSystemIdentifier"].iloc[index] == expected


def describe_when_mapping_Schoology_list_to_EdFi_DataFrame_With_additional_mapping():
    def it_should_return_final_output_from_the_sync_method():
        def mapper(df: pd.DataFrame) -> pd.DataFrame:
            return pd.DataFrame([{"one": 1}])

        attendance_events = [{
            "date": "2020-08-28",
            "statuses": {
                "status": [
                    {
                        "status_code": 1,
                        "attendances": {
                            "attendance": [
                                {
                                    "enrollment_id": 12345,
                                    "date": "2021-08-28",
                                    "status": 1,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12346,
                                    "date": "2022-08-28",
                                    "status": 2,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12347,
                                    "date": "2023-08-28",
                                    "status": 3,
                                    "comment": "",
                                },
                                {
                                    "enrollment_id": 12348,
                                    "date": "2024-08-28",
                                    "status": 4,
                                    "comment": "",
                                },
                            ]
                        }
                    }
                ]
            },
        }]

        section_associations = [
            {
                "SourceSystemIdentifier": 12345,
                "LMSUserSourceSystemIdentifier": 5678,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
                "CreateDate": None,
                "LastModifiedDate": None
            },
            {
                "SourceSystemIdentifier": 12346,
                "LMSUserSourceSystemIdentifier": 5677,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
                "CreateDate": None,
                "LastModifiedDate": None
            },
            {
                "SourceSystemIdentifier": 12347,
                "LMSUserSourceSystemIdentifier": 5676,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
            },
            {
                "SourceSystemIdentifier": 12348,
                "LMSUserSourceSystemIdentifier": 5675,
                "LMSSectionSourceSystemIdentifier": 555,
                "EnrollmentStatus": "active",
                "SourceSystem": "Schoology",
                "StartDate": None,
                "EndDate": None,
            },
        ]

        # Arrange
        section_associations = pd.DataFrame(section_associations)

        # Act
        result = map_to_udm(attendance_events, section_associations, mapper)

        # Assert
        assert result.iloc[0]["one"] == 1
