import os

import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

from app.config import TOP_K_RESULTS

load_dotenv()


class VectorStore:
    """
    Handles all PostgreSQL and pgvector operations.
    """

    def __init__(self):
        """
        Establish database connection.
        """

        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        self.connection.autocommit = True

        register_vector(self.connection)

    def document_exists(self, document_hash: str) -> tuple | None:
        """
        Check whether a document already exists.

        Returns:
            (document_id,) if found
            None otherwise
        """

        cursor = self.connection.cursor()

        query = """
            SELECT id
            FROM documents
            WHERE document_hash = %s;
        """

        cursor.execute(query, (document_hash,))

        result = cursor.fetchone()

        cursor.close()

        return result

    def add_document(
        self,
        document_name: str,
        document_hash: str
    ) -> int:
        """
        Insert document metadata.

        Returns:
            document_id
        """

        cursor = self.connection.cursor()

        query = """
            INSERT INTO documents
            (
                document_name,
                document_hash
            )
            VALUES (%s, %s)
            RETURNING id;
        """

        cursor.execute(
            query,
            (
                document_name,
                document_hash
            )
        )

        document_id = cursor.fetchone()[0]

        cursor.close()

        return document_id

    def add_chunks(
        self,
        document_id: int,
        chunks: list,
        embeddings: list
    ) -> int:
        """
        Store chunks and embeddings.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must be equal."
            )

        cursor = self.connection.cursor()

        query = """
            INSERT INTO document_chunks
            (
                document_id,
                chunk_id,
                page_number,
                chunk_text,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s);
        """

        for chunk, embedding in zip(chunks, embeddings):

            cursor.execute(
                query,
                (
                    document_id,
                    chunk.metadata["chunk_id"],
                    chunk.metadata["page"],
                    chunk.page_content,
                    embedding
                )
            )

        cursor.close()

        return len(chunks)

    def similarity_search(
        self,
        query_embedding,
        top_k: int = TOP_K_RESULTS
    ) -> list:
        """
        Retrieve the most relevant chunks.
        """

        cursor = self.connection.cursor()

        query = """
            SELECT
                d.document_name,
                dc.page_number,
                dc.chunk_text,
                dc.embedding <=> %s::vector AS distance

            FROM document_chunks dc

            JOIN documents d
            ON dc.document_id = d.id

            ORDER BY distance ASC

            LIMIT %s;
        """

        cursor.execute(
            query,
            (
                query_embedding,
                top_k
            )
        )

        rows = cursor.fetchall()
        cursor.close()

        results = []

        for row in rows:
            results.append(
                {
                    "document_name": row[0],
                    "page": row[1],
                    "chunk_text": row[2],
                    "distance": float(row[3])
                }
            )

        return results

    def close(self):
        """
        Close database connection.
        """

        if self.connection:
            self.connection.close()
