"""
legal_parser.py

Extracts legal structure from Acts and performs
definition-aware chunking for Section 2.
"""

import re


class LegalParser:

    def extract_metadata(self, text: str):

        # -----------------------------
        # Extract Act Name
        # -----------------------------
        act = "Unknown Act"

        act_match = re.search(
            r'Consumer Protection Act,\s*2019',
            text,
            flags=re.IGNORECASE
        )

        if act_match:
            act = "Consumer Protection Act, 2019"

        chunks = []

        current_chapter = "Unknown Chapter"

        # Match every section
        section_pattern = r'(?m)^(\d+)\.\s'

        matches = list(re.finditer(section_pattern, text))

        for i, match in enumerate(matches):

            start = match.start()

            end = (
                len(text)
                if i == len(matches) - 1
                else matches[i + 1].start()
            )

            chunk = text[start:end].strip()

            # -----------------------------
            # Find current chapter
            # -----------------------------
            before = text[:start]

            chapter_matches = re.findall(
                r'CHAPTER\s+[IVXLC]+',
                before,
                flags=re.IGNORECASE
            )

            if chapter_matches:
                current_chapter = chapter_matches[-1]

            section = re.match(r'(\d+)', chunk).group(1)

            first_line = chunk.splitlines()[0]

            title = first_line

            # ======================================================
            # SPECIAL HANDLING FOR SECTION 2 (Definitions)
            # ======================================================

            if section == "2":

                definition_pattern = r'\((\d+)\)\s+"([^"]+)"\s+means'

                definitions = list(
                    re.finditer(
                        definition_pattern,
                        chunk,
                        flags=re.IGNORECASE
                    )
                )

                if definitions:

                    for j, definition in enumerate(definitions):

                        d_start = definition.start()

                        d_end = (
                            len(chunk)
                            if j == len(definitions) - 1
                            else definitions[j + 1].start()
                        )

                        definition_chunk = chunk[d_start:d_end].strip()

                        definition_name = definition.group(2)

                        chunks.append({

                            "section":
                                f"Section 2({definition.group(1)})",

                            "chapter":
                                current_chapter,

                            "title":
                                f"Definition - {definition_name}",

                            "content":
                                definition_chunk,

                            "act":
                                act

                        })

                    # Skip adding the whole Section 2
                    continue

            # ======================================================
            # NORMAL SECTIONS
            # ======================================================

            chunks.append({

                "section":
                    f"Section {section}",

                "chapter":
                    current_chapter,

                "title":
                    title,

                "content":
                    chunk,

                "act":
                    act

            })

        return chunks