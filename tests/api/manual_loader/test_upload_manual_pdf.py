from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.manual_loader_client import ManualLoaderClient
from schema.manual_loader import UploadManualFileResponseSchema
from schema.manual_loader import DeleteManualFilesRequestSchema
from tools.assertions.base import assert_status_code

VALID_PDF = "tests/api/manual_loader/test_files/test_file.pdf"     

@pytest.mark.manual_loader
@pytest.mark.api
@pytest.mark.integration
@allure.feature("Manual Loader")
class TestUploadManualPDF:
    @allure.title("Upload valid PDF -> 200 OK")
    async def test_manual__upload_pdf(
        self,
        manual_loader_client: ManualLoaderClient,
               
    ) -> None:
        response = await manual_loader_client.upload_manual_file(
            file_path=VALID_PDF
            )
        assert_status_code(response.status_code, HTTPStatus.OK)
        body = UploadManualFileResponseSchema.model_validate_json(response.text)
        assert body.external_id
        assert body.message == "File uploaded successfully"

        external_id = body.external_id
        
        delete_response = await manual_loader_client.delete_manual_files(
            DeleteManualFilesRequestSchema(file_ids=[external_id])
        )
        print(f"DELETE STATUS: {delete_response.status_code}")
        print(f"DELETE BODY: {delete_response.text}")
        assert_status_code(delete_response.status_code, HTTPStatus.OK)