# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult

FAKE_KEY = "TEST_KEY"
FAKE_SECRET = "TEST_SECRET"
FAKE_ENDPOINT_URL = "FAKE_URL"
DEFAULT_URL = "https://api.schoology.com/v1/"


@pytest.fixture
def default_request_client():
    return RequestClient(FAKE_KEY, FAKE_SECRET)


class TestRequestClient:
    class Test_when_constructing:
        def test_given_not_passing_in_a_url_then_use_the_DEFAULT_URL(self):
            request_client = RequestClient(FAKE_KEY, FAKE_SECRET)
            assert request_client.base_url == DEFAULT_URL

        def test_given_custom_url_then_use_it_for_the_base_url(self):

            # Arrange
            custom_url = "a_custom_url"

            # Act
            request_client = RequestClient(FAKE_KEY, FAKE_SECRET, custom_url)

            # Assert
            assert request_client.base_url == custom_url

    class Test_when_building_request_header:
        def test_then_consumer_key_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=FAKE_KEY,
            )

        def test_then_oauth_word_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value="OAuth",
            )

        def _present_in_header(self, request_header, header_key, contained_value):
            header_section = request_header[header_key]
            return header_section.find(contained_value) != -1

    class Test_when_get_method_is_called:
        def test_and_error_occurs_then_raise_an_HTTPError(
            self, requests_mock, default_request_client
        ):
            expected_url = DEFAULT_URL + FAKE_ENDPOINT_URL

            # Arrange
            requests_mock.get(expected_url, reason="BadRequest", status_code=400, text="no good")

            # Act
            try:
                default_request_client.get(FAKE_ENDPOINT_URL)

                raise RuntimeError("expected an error to occur")
            except RuntimeError as ex:
                assert str(ex) == "BadRequest (400): no good"

        def test_given_no_parameters_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get(None)

    class Test_when_getting_assignments:
        class Test_given_there_is_one_assignments:
            @pytest.fixture
            def result(self, default_request_client, requests_mock):
                section_id = 3324
                page_size = 435
                expected_url_1 = "https://api.schoology.com/v1/sections/3324/assignments?start=0&limit=435"

                # Arrange
                text = '{"assignment": [{"id":"b"}]}'
                called = set()

                def callback(request, context):
                    called.add(request.url)
                    return text

                requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)

                # Act
                result = default_request_client.get_assignments(section_id, page_size)

                return result

            # def test_then_it_should_return_the_assignment(self, result, requests_mock):
            #     assert result["id"] == "b"

        class Test_given_two_pages_of_assignments:
            @pytest.fixture
            def result(self, default_request_client, requests_mock):
                section_id = 3324
                page_size = 1
                expected_url_1 = "https://api.schoology.com/v1/sections/3324/assignments?start=0&limit=1"
                expected_url_2 = "https://api.schoology.com/v1/sections/3324/assignments?start=1&limit=1"

                # Arrange
                text_1 = '{"assignment": [{"id":"b"}], "links":{"next":"'+expected_url_2+'"}}'
                text_2 = '{"assignment": [{"id":"c"}]}'

                def callback(request, context):
                    if request.url == expected_url_1:
                        return text_1
                    else:
                        return text_2

                requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)
                requests_mock.get(expected_url_2, reason="OK", status_code=200, text=callback)

                # Act
                result = default_request_client.get_assignments(section_id, page_size)

                return result

            def test_then_it_should_return_two_assignment(self, result: PaginatedResult, requests_mock):
                assert result.get_next_page() is not None

            def test_result_should_contain_first_assignment(self, result: PaginatedResult, requests_mock):
                assert len([r for r in result.current_page_items if r["id"] == "b"]) == 1

            def test_result_should_contain_second_assignment(self, result, requests_mock):
                assert len([r for r in result.get_next_page().current_page_items if r["id"] == "c"]) == 1

    class Test_when_get_section_by_course_id_method_is_called:
        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(
            self, default_request_client: RequestClient, requests_mock
        ):
            course_id = 1
            expected_url_1 = "https://api.schoology.com/v1/courses/1/sections"
            expected_url_2 = "https://api.schoology.com/v1/courses/2/sections"

            # Arrange
            text = '{"section": [{"a":"b"}]}'
            called = set()

            def callback(request, context):
                called.add(request.url)
                return text

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)
            requests_mock.get(expected_url_2, reason="OK", status_code=200, text=callback)

            # Act
            response = default_request_client.get_section_by_course_id(course_id)

            # Assert
            assert expected_url_1 in called, "URL 1 not called"

            assert isinstance(response, PaginatedResult), "expected response to be a PaginatedResult"
            assert len(response.current_page_items) == 1, "expected one result"

    class Test_when_get_submissions_by_section_id_and_grade_item_id_method_is_called:
        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/sections/1/submissions/1234564"

            # Arrange
            text = '{"revision":[{"revision_id": 1,"uid": 100032890,"created": 1598631506,"num_items": 1,"late": 0,"draft": 0}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_submissions_by_section_id_and_grade_item_id("1", "1234564")

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["uid"] == 100032890

    class Test_when_get_users_method_is_called:
        def test_given_the_get_call_returns_empty_response_then_return_empty_PaginatedResult(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/users"

            # Arrange
            text = '{"user":[]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_users()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 0

        def test_given_the_get_call_returns_users_then_return_list_of_users(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/users"

            # Arrange
            text = '{"user":[{"uid": 100032890}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_users()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["uid"] == 100032890

    class Test_when_build_pagination_params_method_is_called:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client._build_query_params_for_first_page([])

        def test_given_correct_parameter_then_url_is_built_correctly(
            self, default_request_client
        ):
            # Arrange
            items_per_page = 17
            expected_result = "start=0&limit=17"

            # Act
            result = default_request_client._build_query_params_for_first_page(
                items_per_page
            )

            # Assert
            assert result == expected_result

    class Test_when_getting_all_courses:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_courses([])

        def test_given_correct_parameter_then_returns_expected_data(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/courses"

            # Arrange
            text = '{"course":[{"id": 100032890, "title": "English I"}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_courses()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["id"] == 100032890


def describe_when_getting_enrollments_with_two_pages():
    @pytest.fixture
    def result(requests_mock):
        section_id = 3324
        page_size = 1
        expected_url_1 = "https://api.schoology.com/v1/sections/3324/enrollments?start=0&limit=1"
        expected_url_2 = "https://api.schoology.com/v1/sections/3324/enrollments?start=1&limit=1"

        enrollments_1 = '[{"id": 12345}]'
        response_1 = '{"enrollment": '+enrollments_1+',"total": "2","links": {"self": "...","next": "'+expected_url_2+'"}}'

        enrollments_2 = '[{"id": 99999}]'
        response_2 = '{"enrollment": '+enrollments_2+', "total": "2", "links": {"self": "..."}}'

        # Arrange

        def callback(request, context):
            if request.url == expected_url_1:
                return response_1
            else:
                return response_2

        requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)
        requests_mock.get(expected_url_2, reason="OK", status_code=200, text=callback)

        client = RequestClient(FAKE_KEY, FAKE_SECRET)

        # Act
        result = client.get_enrollments(section_id, page_size)

        return result

    def it_should_return_two_pages(result: PaginatedResult):
        assert result.get_next_page() is not None

    def it_should_contain_the_first_enrollment(result: PaginatedResult):
        assert len([r for r in result.current_page_items if r["id"] == 12345]) == 1

    def it_should_contain_the_second_enrollment(result):
        assert len([r for r in result.get_next_page().current_page_items if r["id"] == 99999]) == 1


def describe_when_getting_attendance():
    @pytest.fixture
    def result(requests_mock):
        section_id = 3324
        expected_url_1 = "https://api.schoology.com/v1/sections/3324/attendance"

        event_1 = '[{"id": 12345}]'
        response_1 = '{"date": '+event_1+',"totals": { "total": [{"status":1,"count":1 }]}}'

        # Arrange
        requests_mock.get(expected_url_1, reason="OK", status_code=200, text=response_1)

        client = RequestClient(FAKE_KEY, FAKE_SECRET)

        # Act
        result = client.get_attendance(section_id)

        return result

    def it_should_return_one_event(result):
        assert len(result) == 1


def describe_when_getting_section_updates():
    @pytest.fixture
    def result(requests_mock):
        section_id = 3324
        expected_url_1 = "https://api.schoology.com/v1/sections/3324/updates"

        update_1 = '[{"id": 12345}]'
        response_1 = '{"update": '+update_1+',"total": 1, "links": {"self": "ignore"}}'

        # Arrange
        requests_mock.get(expected_url_1, reason="OK", status_code=200, text=response_1)

        client = RequestClient(FAKE_KEY, FAKE_SECRET)

        # Act
        result = client.get_section_updates(section_id)

        return result

    def it_should_return_one_update(result: PaginatedResult):
        assert len(result.current_page_items) == 1


def describe_when_getting_section_update_replies():
    @pytest.fixture
    def result(requests_mock):
        section_id = 3324
        update_id = 4435
        expected_url_1 = "https://api.schoology.com/v1/sections/3324/updates/4435/comments"

        update_comment_1 = '[{"id": 12345}]'
        response_1 = '{"comment": '+update_comment_1+',"total": 1, "links": {"self": "ignore"}}'

        # Arrange
        requests_mock.get(expected_url_1, reason="OK", status_code=200, text=response_1)

        client = RequestClient(FAKE_KEY, FAKE_SECRET)

        # Act
        result = client.get_section_update_replies(section_id, update_id)

        return result

    def it_should_return_one_update(result: PaginatedResult):
        assert len(result.current_page_items) == 1
