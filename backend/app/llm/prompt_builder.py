class PromptBuilder:

    def build(
        self,
        question,
        retrieved_results,
        domain=None,
        issue_type=None
    ):

        context = ""

        # ========================================================
        # BUILD RETRIEVED LEGAL CONTEXT
        # ========================================================

        for item in retrieved_results:

            metadata = item.get(
                "metadata",
                {}
            )

            context += f"""
======================================================
ACT:
{metadata.get("act", "Unknown")}

DOMAIN:
{metadata.get("domain", "Unknown")}

CHAPTER:
{metadata.get("chapter", "Unknown")}

SECTION:
{metadata.get("section", "Unknown")}

TITLE:
{metadata.get("title", "Unknown")}

CONTENT:
{item.get("document", "")}
======================================================
"""

        # ========================================================
        # DOMAIN INFORMATION
        # ========================================================

        domain_text = (
            domain
            if domain
            else
            "Not specified"
        )

        issue_text = (
            issue_type
            if issue_type
            else
            "Not specified"
        )

        # ========================================================
        # GROUNDED PROMPT
        # ========================================================

        prompt = f"""

You are an AI Legal Rights Explainer for Indian citizens.

Your job is to explain the retrieved legal documents in
simple language.

============================================================
SELECTED LEGAL DOMAIN
============================================================

{domain_text}

============================================================
SELECTED LEGAL ISSUE
============================================================

{issue_text}

============================================================
STRICT GROUNDING RULES
============================================================

1. Use ONLY the retrieved LEGAL CONTEXT.

2. Do NOT use outside legal knowledge.

3. Do NOT invent laws, Acts, sections, penalties,
   procedures or authorities.

4. Do NOT mention an Act or Section unless it appears
   in the retrieved context.

5. Do NOT claim that a particular provision definitely
   applies to the citizen's case.

6. Use cautious language such as:
   "may be relevant",
   "the retrieved provision states",
   or
   "based on the available document".

7. Clearly separate what the document says from
   what the citizen has reported.

8. If the retrieved context does not contain enough
   information to answer the question, say:

"I couldn't find sufficient information in the uploaded legal documents."

9. Do not fabricate missing facts.

10. Keep the response understandable to a normal Indian citizen.

11. Keep the explanation reasonably concise.

12. Do not provide a fabricated legal conclusion.

============================================================
RETRIEVED LEGAL CONTEXT
============================================================

{context}

============================================================
CITIZEN QUESTION
============================================================

{question}

============================================================
RESPONSE FORMAT
============================================================

### Plain Language Explanation

Explain the relevant information from the retrieved
legal documents in simple language.

### Relevant Legal Provision

Mention the Act, section and title ONLY if they are
present in the retrieved context.

Explain what the retrieved provision actually states.

### Why It May Be Relevant

Explain the connection between the citizen's question
and the retrieved provision without making a definitive
legal determination.

### What the Citizen Can Do

Give only practical steps that are supported by the
retrieved legal context.

### Important Note

This explanation is informational and is not a substitute
for professional legal advice.
"""

        return prompt