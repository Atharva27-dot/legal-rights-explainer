import { useState } from "react";
import toast from "react-hot-toast";
import { uploadEvidence, extractEvidenceText } from "../services/api";

export default function EvidenceUploader({ onEvidenceChange, onSkip }) {
  const [files, setFiles] = useState([]);
  const [extracting, setExtracting] = useState({});

  const allowedTypes = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ];

  const maxSize = 10 * 1024 * 1024;

  const updateFiles = (nextFiles) => {
    setFiles(nextFiles);
    onEvidenceChange?.(nextFiles);
  };

  const extractFile = async (file, index, currentFiles) => {
    if (!file.fileId) return;

    try {
      setExtracting((p) => ({ ...p, [index]: true }));

      const result = await extractEvidenceText(file.fileId);

      const nextFiles = currentFiles.map((item, itemIndex) =>
        itemIndex === index
          ? {
              ...item,
              extractionStatus: result.extraction_status,
              extractedText: result.text || "",
              characterCount: result.character_count || 0,
            }
          : item
      );

      updateFiles(nextFiles);

      if (result.extraction_status === "TEXT_EXTRACTED") {
        toast.success(`${file.name}: text extracted.`);
      } else if (result.extraction_status === "NO_TEXT_FOUND") {
        toast.warning(`${file.name}: no selectable text found.`);
      } else if (result.extraction_status === "OCR_PENDING") {
        toast.success(`${file.name}: uploaded. OCR is pending.`);
      }
    } catch (error) {
      console.error(error);
      toast.error(
        error?.response?.data?.detail ||
          `${file.name}: unable to extract text.`
      );
    } finally {
      setExtracting((p) => ({ ...p, [index]: false }));
    }
  };

  const handleUpload = async (event) => {
    const selectedFiles = Array.from(event.target.files || []);

    for (const file of selectedFiles) {
      if (!allowedTypes.includes(file.type)) {
        toast.error(`${file.name}: unsupported file type.`);
        continue;
      }

      if (file.size > maxSize) {
        toast.error(`${file.name}: file must be below 10 MB.`);
        continue;
      }

      try {
        toast.loading(`Uploading ${file.name}...`, {
          id: `evidence-${file.name}`,
        });

        const result = await uploadEvidence(file);

        const item = {
          name: file.name,
          size: file.size,
          type: file.type,
          fileId: result.file_id,
          uploaded: true,
          extractionStatus: null,
          extractedText: "",
          characterCount: 0,
        };

        const nextFiles = [...files, item];
        updateFiles(nextFiles);

        toast.success(`${file.name} uploaded.`, {
          id: `evidence-${file.name}`,
        });

        await extractFile(item, nextFiles.length - 1, nextFiles);
      } catch (error) {
        console.error(error);
        toast.error(
          error?.response?.data?.detail ||
            `${file.name}: upload failed.`,
          { id: `evidence-${file.name}` }
        );
      }
    }

    event.target.value = "";
  };

  const handleRemove = (indexToRemove) => {
    updateFiles(
      files.filter((_, index) => index !== indexToRemove)
    );
  };

  return (
    <div className="border border-indigo-200 bg-indigo-50 rounded-2xl p-6">
      <div className="mb-4">
        <h3 className="text-xl font-bold text-slate-800">
          📎 Supporting Evidence
        </h3>
        <p className="text-sm text-slate-600 mt-1">
          Upload documents that may help us understand your case.
          Evidence is optional.
        </p>
      </div>

      <div className="border-2 border-dashed border-indigo-300 rounded-2xl p-7 text-center bg-white">
        <div className="text-4xl mb-2">📄</div>

        <p className="font-semibold text-slate-700">
          Upload supporting documents
        </p>

        <p className="text-xs text-slate-500 mt-1">
          Invoice, receipt, warranty, screenshots, emails or transaction
          records
        </p>

        <p className="text-xs text-slate-400 mt-2">
          PDF, JPG, PNG or DOCX · Maximum 10 MB per file
        </p>

        <label className="inline-flex items-center justify-center mt-5 bg-indigo-700 hover:bg-indigo-600 text-white rounded-xl px-6 py-3 cursor-pointer font-semibold">
          + Upload Evidence
          <input
            type="file"
            multiple
            accept=".pdf,.jpg,.jpeg,.png,.docx"
            onChange={handleUpload}
            className="hidden"
          />
        </label>

        {onSkip && (
          <button
            type="button"
            onClick={onSkip}
            className="block mx-auto mt-3 text-sm text-slate-600 hover:text-indigo-700 underline"
          >
            Continue without evidence
          </button>
        )}
      </div>

      {files.length > 0 && (
        <div className="mt-5 space-y-3">
          <p className="font-semibold text-slate-700">
            Uploaded Evidence ({files.length})
          </p>

          {files.map((file, index) => (
            <div
              key={`${file.fileId || file.name}-${index}`}
              className="bg-white border border-slate-200 rounded-xl p-4"
            >
              <div className="flex items-center justify-between gap-4">
                <p className="font-medium text-slate-700 truncate">
                  {file.name}
                </p>

                <button
                  type="button"
                  onClick={() => handleRemove(index)}
                  className="text-red-600 hover:text-red-800 font-semibold"
                >
                  Remove
                </button>
              </div>

              <p className="text-xs text-slate-500 mt-1">
                {(file.size / (1024 * 1024)).toFixed(2)} MB
              </p>

              <div className="mt-2 text-xs">
                {extracting[index] ? (
                  <span className="text-indigo-600">
                    Extracting text...
                  </span>
                ) : file.extractionStatus === "TEXT_EXTRACTED" ? (
                  <span className="text-green-600">
                    ✓ Text extracted ({file.characterCount} characters)
                  </span>
                ) : file.extractionStatus === "NO_TEXT_FOUND" ? (
                  <span className="text-amber-600">
                    ⚠ No selectable text found
                  </span>
                ) : file.extractionStatus === "OCR_PENDING" ? (
                  <span className="text-amber-600">
                    ⚠ Image uploaded — OCR pending
                  </span>
                ) : (
                  <span className="text-slate-400">
                    Uploaded — extraction pending
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
