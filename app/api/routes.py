from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.indexing_service import IndexingService
from app.services.query_service import QueryService


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    """
    Upload and index an enterprise PDF document.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    temp_path = None

    try:

        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:

            temp_path = Path(temp_file.name)

            while True:

                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                temp_file.write(chunk)

        service = IndexingService()

        try:

            result = service.index_document(
                pdf_path=str(temp_path),
                document_name=file.filename
            )

        finally:

            service.close()

        return result

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(exc)}"
        )

    finally:

        if temp_path and temp_path.exists():
            temp_path.unlink()


@router.post("/query")
def ask_question(question: str):
    """
    Ask a question about the uploaded enterprise documents.
    """

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    service = QueryService()

    try:

        result = service.ask(question)

        return {
            "success": True,
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Question processing failed: {str(exc)}"
        )

    finally:

        service.close()
