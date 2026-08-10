class CitationGenerator:
    """
    Generates structured citations from retrieved chunks.
    """

    def generate_citations(self, retrieved_chunks):
        """
        Generate unique citations from retrieved chunks.

        Returns:
            List of citation dictionaries.
        """

        citations = []
        seen = set()

        for chunk in retrieved_chunks:

            document_name = chunk["document_name"]
            page_number = chunk["page"]

            citation_key = (
                document_name,
                page_number
            )

            if citation_key in seen:
                continue

            seen.add(citation_key)

            citations.append(
                {
                    "document": document_name,
                    "page": page_number
                }
            )

        return citations
