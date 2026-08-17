"""
legal_parser.py

Parser for Indian legal Acts.

Handles:
- Act detection
- Domain detection
- Chapter detection
- Section detection
- Amendment-note filtering
- Omitted-section filtering
- Alphanumeric sections such as 43A, 66C, 66D
"""

import re


class LegalParser:

    # ============================================================
    # ACT DETECTION
    # ============================================================

    def detect_act(
        self,
        text: str,
        source_file: str = ""
    ):

        combined = (
            f"{text[:15000]} {source_file}"
        ).lower()

        if re.search(
            r"consumer\s+protection\s+act[\s,]*2019",
            combined,
            flags=re.IGNORECASE
        ):
            return "Consumer Protection Act, 2019"

        if re.search(
            r"information\s+technology\s+act[\s,]*2000",
            combined,
            flags=re.IGNORECASE
        ):
            return "Information Technology Act, 2000"

        if "consumer_protection" in source_file.lower():
            return "Consumer Protection Act, 2019"

        if "information_technology" in source_file.lower():
            return "Information Technology Act, 2000"

        return "Unknown Act"

    # ============================================================
    # DOMAIN
    # ============================================================

    def detect_domain(self, act: str):

        act_lower = act.lower()

        if "consumer protection" in act_lower:
            return "Consumer Protection"

        if "information technology" in act_lower:
            return "Cyber / IT"

        return "General Legal"

    # ============================================================
    # CHECK WHETHER A LINE IS AN AMENDMENT NOTE
    # ============================================================

    def is_amendment_note(self, text: str):

        text_lower = text.lower().strip()

        amendment_phrases = [

            "subs. by",

            "substituted by",

            "ins. by",

            "inserted by",

            "omitted by",

            "repealed by",

            "rep. by",

            "for section",

            "for sections",

            "w.e.f.",

            "ibid.",

            "act 10 of 2009",

            "act 21 of 2000",

            "act 47 of 2008"

        ]

        return any(
            phrase in text_lower
            for phrase in amendment_phrases
        )

    # ============================================================
    # CHECK OMITTED SECTION
    # ============================================================

    def is_omitted_section(self, text: str):

        text_lower = text.lower()

        return (
            "[omitted]" in text_lower
            or
            "[omitted.]" in text_lower
            or
            "section omitted" in text_lower
        )

    # ============================================================
    # SECTION HEADER
    # ============================================================

    def is_section_header(self, line: str):

        line = line.strip()

        # Supports:
        #
        # 43.
        # 43A.
        # 66.
        # 66C.
        # 66-D.
        #
        # Does NOT match ordinary numbered paragraphs.

        return re.match(
            r"^\d+[A-Z]?(?:-[A-Z])?\.\s+",
            line,
            flags=re.IGNORECASE
        )

    # ============================================================
    # EXTRACT SECTION NUMBER
    # ============================================================

    def extract_section_number(
        self,
        line: str
    ):

        match = re.match(
            r"^\s*(\d+[A-Z]?(?:-[A-Z])?)\.\s+",
            line,
            flags=re.IGNORECASE
        )

        if not match:
            return None

        return match.group(1)

    # ============================================================
    # EXTRACT LEGAL SECTIONS
    # ============================================================

    def extract_metadata(
        self,
        text: str,
        source_file: str = ""
    ):

        act = self.detect_act(
            text,
            source_file
        )

        domain = self.detect_domain(
            act
        )

        chunks = []

        current_chapter = (
            "Unknown Chapter"
        )

        # --------------------------------------------------------
        # Normalize line endings
        # --------------------------------------------------------

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        lines = text.splitlines()

        # --------------------------------------------------------
        # Find candidate section positions
        # --------------------------------------------------------

        section_positions = []

        for index, line in enumerate(lines):

            stripped = line.strip()

            if not stripped:
                continue

            if not self.is_section_header(
                stripped
            ):
                continue

            section_number = (
                self.extract_section_number(
                    stripped
                )
            )

            if not section_number:
                continue

            # ----------------------------------------------------
            # Reject amendment-note headings
            # ----------------------------------------------------

            if self.is_amendment_note(
                stripped
            ):
                continue

            # ----------------------------------------------------
            # Reject omitted sections
            # ----------------------------------------------------

            if self.is_omitted_section(
                stripped
            ):
                continue

            section_positions.append(
                (
                    index,
                    section_number
                )
            )

        # --------------------------------------------------------
        # Extract each section
        # --------------------------------------------------------

        for position_index, (
            line_index,
            section_number
        ) in enumerate(
            section_positions
        ):

            # ----------------------------------------------------
            # Determine section end
            # ----------------------------------------------------

            if (
                position_index
                ==
                len(section_positions) - 1
            ):

                end_line = len(lines)

            else:

                end_line = (
                    section_positions[
                        position_index + 1
                    ][0]
                )

            section_lines = lines[
                line_index:end_line
            ]

            section_text = "\n".join(
                section_lines
            ).strip()

            if not section_text:
                continue

            # ----------------------------------------------------
            # Current chapter
            # ----------------------------------------------------

            for previous_line in reversed(
                lines[:line_index]
            ):

                chapter_match = re.search(
                    r"\b(CHAPTER\s+[IVXLC]+A?)\b",
                    previous_line,
                    flags=re.IGNORECASE
                )

                if chapter_match:

                    current_chapter = (
                        chapter_match
                        .group(1)
                        .upper()
                    )

                    break

            # ----------------------------------------------------
            # Title
            # ----------------------------------------------------

            first_line = section_lines[0].strip()

            title = re.sub(
                r"^\d+[A-Z]?(?:-[A-Z])?\.\s*",
                "",
                first_line,
                flags=re.IGNORECASE
            ).strip()

            # ----------------------------------------------------
            # Ignore pure amendment remnants
            # ----------------------------------------------------

            if self.is_amendment_note(
                title
            ):

                continue

            if self.is_omitted_section(
                title
            ):

                continue

            # ----------------------------------------------------
            # Section 2 definitions
            # ----------------------------------------------------

            if section_number == "2":

                definition_pattern = re.compile(
                    r'\((\d+)\)\s+"([^"]+)"\s+means',
                    flags=re.IGNORECASE
                )

                definitions = list(
                    definition_pattern.finditer(
                        section_text
                    )
                )

                if definitions:

                    for definition_index, definition in enumerate(
                        definitions
                    ):

                        definition_start = (
                            definition.start()
                        )

                        if (
                            definition_index
                            ==
                            len(definitions) - 1
                        ):

                            definition_end = (
                                len(section_text)
                            )

                        else:

                            definition_end = (
                                definitions[
                                    definition_index + 1
                                ].start()
                            )

                        definition_text = (
                            section_text[
                                definition_start:
                                definition_end
                            ].strip()
                        )

                        definition_name = (
                            definition.group(2)
                        )

                        chunks.append({

                            "section":
                                f"Section 2({definition.group(1)})",

                            "chapter":
                                current_chapter,

                            "title":
                                f"Definition - {definition_name}",

                            "content":
                                definition_text,

                            "act":
                                act,

                            "domain":
                                domain

                        })

                    continue

            # ----------------------------------------------------
            # Normal section
            # ----------------------------------------------------

            chunks.append({

                "section":
                    f"Section {section_number}",

                "chapter":
                    current_chapter,

                "title":
                    title,

                "content":
                    section_text,

                "act":
                    act,

                "domain":
                    domain

            })

        # ========================================================
        # DEBUG SUMMARY
        # ========================================================

        print()
        print("=" * 60)
        print("LEGAL DOCUMENT PARSER")
        print("=" * 60)

        print(
            "Act:",
            act
        )

        print(
            "Domain:",
            domain
        )

        print(
            "Sections extracted:",
            len(chunks)
        )

        # --------------------------------------------------------
        # Show first 15 extracted sections
        # --------------------------------------------------------

        print()
        print(
            "Sample extracted sections:"
        )

        for chunk in chunks[:15]:

            print(
                f"  {chunk['section']} | "
                f"{chunk['title']}"
            )

        print("=" * 60)
        print()

        return chunks