import { useState } from "react";
import { askQuestion } from "../services/api";


const issuesByDomain = {
  "Consumer Protection": [
    "Consumer Definition",
    "Consumer Rights",
    "Filing Complaint",
    "Mediation",
    "Defective Product",
    "Refund / Replacement",
    "Deficiency in Service",
    "Unfair Trade Practice",
    "Product Liability"
  ],

  "Cyber / IT": [
    "UPI Fraud",
    "Unauthorized Access",
    "Identity Theft",
    "Online Payment Fraud",
    "Cyber Crime"
  ],

  "Employment / Labour": [
    "Wrongful Termination",
    "Unpaid Salary",
    "Workplace Rights",
    "Employment Dispute"
  ],

  "Property": [
    "Property Dispute",
    "Landlord Tenant Dispute",
    "Ownership Dispute",
    "Property Transfer"
  ],

  "Family Law": [
    "Divorce",
    "Maintenance",
    "Child Custody",
    "Domestic Dispute"
  ],

  "Motor Vehicle": [
    "Road Accident",
    "Motor Insurance Claim",
    "Vehicle Compensation",
    "Traffic Dispute"
  ]
};


export default function RightsGuide() {

  const [domain, setDomain] = useState("");

  const [issueType, setIssueType] = useState("");

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const handleDomainChange = (event) => {

    setDomain(event.target.value);

    setIssueType("");

  };


  const handleSubmit = async (event) => {

    event.preventDefault();

    setError("");

    setAnswer(null);


    if (!domain) {

      setError(
        "Please select a legal domain."
      );

      return;

    }


    if (!issueType) {

      setError(
        "Please select the specific legal issue."
      );

      return;

    }


    if (!question.trim()) {

      setError(
        "Please describe your legal problem."
      );

      return;

    }


    try {

      setLoading(true);


      const result = await askQuestion(

        question,

        domain,

        issueType

      );


      setAnswer(result);


    } catch (err) {

      console.error(err);

      setError(
        "Unable to process your request. Please make sure the backend is running."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div
      style={{
        maxWidth: "900px",
        margin: "40px auto",
        padding: "20px"
      }}
    >

      <h1>
        Legal Rights Guide
      </h1>


      <p>
        Select your legal domain and issue before
        asking your question. This helps the system
        retrieve more relevant legal provisions.
      </p>


      <form
        onSubmit={handleSubmit}
      >

        {/* DOMAIN */}

        <div
          style={{
            marginBottom: "20px"
          }}
        >

          <label>
            <strong>
              Legal Domain
            </strong>
          </label>

          <br />

          <select
            value={domain}
            onChange={handleDomainChange}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "8px"
            }}
          >

            <option value="">
              Select legal domain
            </option>

            {Object.keys(issuesByDomain).map(
              (item) => (

                <option
                  key={item}
                  value={item}
                >
                  {item}
                </option>

              )
            )}

          </select>

        </div>


        {/* ISSUE */}

        {domain && (

          <div
            style={{
              marginBottom: "20px"
            }}
          >

            <label>
              <strong>
                Specific Legal Issue
              </strong>
            </label>

            <br />

            <select
  value={issueType}
  onChange={(event) => {
    setIssueType(event.target.value);
  }}
  style={{
    width: "100%",
    padding: "12px",
    marginTop: "8px"
  }}
>
  <option value="">
    Select specific issue
  </option>

  {domain === "Consumer Protection" && (
    <>
      <option value="Consumer Definition">
        Consumer Definition
      </option>

      <option value="Consumer Rights">
        Consumer Rights
      </option>

      <option value="Filing Complaint">
        Filing Complaint
      </option>

      <option value="Mediation">
        Mediation
      </option>

      <option value="Defective Product">
        Defective Product
      </option>

      <option value="Refund / Replacement">
        Refund / Replacement
      </option>

      <option value="Deficiency in Service">
        Deficiency in Service
      </option>

      <option value="Unfair Trade Practice">
        Unfair Trade Practice
      </option>

      <option value="Product Liability">
        Product Liability
      </option>
    </>
  )}

  {domain === "Cyber / IT" && (
    <>
      <option value="UPI Fraud">
        UPI Fraud
      </option>

      <option value="Unauthorized Access">
        Unauthorized Access
      </option>

      <option value="Identity Theft">
        Identity Theft
      </option>

      <option value="Online Payment Fraud">
        Online Payment Fraud
      </option>

      <option value="Cyber Crime">
        Cyber Crime
      </option>
    </>
  )}

  {domain === "Employment / Labour" && (
    <>
      <option value="Wrongful Termination">
        Wrongful Termination
      </option>

      <option value="Unpaid Salary">
        Unpaid Salary
      </option>

      <option value="Workplace Rights">
        Workplace Rights
      </option>

      <option value="Employment Dispute">
        Employment Dispute
      </option>
    </>
  )}

  {domain === "Property" && (
    <>
      <option value="Property Dispute">
        Property Dispute
      </option>

      <option value="Landlord Tenant Dispute">
        Landlord Tenant Dispute
      </option>

      <option value="Ownership Dispute">
        Ownership Dispute
      </option>

      <option value="Property Transfer">
        Property Transfer
      </option>
    </>
  )}

  {domain === "Family Law" && (
    <>
      <option value="Divorce">
        Divorce
      </option>

      <option value="Maintenance">
        Maintenance
      </option>

      <option value="Child Custody">
        Child Custody
      </option>

      <option value="Domestic Dispute">
        Domestic Dispute
      </option>
    </>
  )}

  {domain === "Motor Vehicle" && (
    <>
      <option value="Road Accident">
        Road Accident
      </option>

      <option value="Motor Insurance Claim">
        Motor Insurance Claim
      </option>

      <option value="Vehicle Compensation">
        Vehicle Compensation
      </option>

      <option value="Traffic Dispute">
        Traffic Dispute
      </option>
    </>
  )}
</select>

          </div>

        )}

        {/* QUESTION */}

        <div
          style={{
            marginBottom: "20px"
          }}
        >

          <label>
            <strong>
              Describe Your Problem
            </strong>
          </label>

          <br />

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            placeholder="Describe what happened in simple language..."
            rows={7}
            style={{
              width: "100%",
              padding: "12px",
              marginTop: "8px",
              resize: "vertical"
            }}
          />

        </div>


        {/* ERROR */}

        {error && (

          <div
            style={{
              marginBottom: "20px",
              padding: "12px",
              border: "1px solid #cc0000"
            }}
          >

            {error}

          </div>

        )}


        {/* SUBMIT */}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "12px 24px",
            cursor: loading
              ? "not-allowed"
              : "pointer"
          }}
        >

          {loading
            ? "Analyzing..."
            : "Explain My Legal Rights"
          }

        </button>

      </form>


      {/* RESULT */}

      {answer && (

        <div
          style={{
            marginTop: "40px"
          }}
        >

          <h2>
            Legal Explanation
          </h2>


          <div
            style={{
              whiteSpace: "pre-wrap",
              padding: "20px",
              border: "1px solid #ddd"
            }}
          >

            {answer.answer}

          </div>


          <div
            style={{
              marginTop: "20px"
            }}
          >

            <strong>
              Confidence:
            </strong>

            {" "}

            {answer.confidence}

          </div>


          {/* SOURCES */}

          {answer.sources &&
            answer.sources.length > 0 && (

              <div
                style={{
                  marginTop: "25px"
                }}
              >

                <h3>
                  Retrieved Legal Sources
                </h3>


                {answer.sources.map(
                  (source, index) => (

                    <div
                      key={index}
                      style={{
                        padding: "15px",
                        marginBottom: "10px",
                        border: "1px solid #ddd"
                      }}
                    >

                      <strong>
                        {source.act}
                      </strong>

                      <br />

                      {source.section}

                      <br />

                      {source.title}

                    </div>

                  )
                )}

              </div>

            )}

        </div>

      )}

    </div>

  );

}