# Exactly three acceptance cases

These are conceptual non-customer fixture specifications, not executed NAS tests.
Relative names below describe inputs; actual approved paths must come from the
user and native inventory. No digest values or successful copy results are supplied.
No media is decoded, rendered, generated or repaired by this proof.

## Case A — byte-equal source plus a different companion

Inputs: incoming/TripA/A.nef and incoming/TripA/A.xmp; archive/Old/B.nef and
archive/Old/B.xmp. A.nef and B.nef contain equal bytes; A.xmp and B.xmp contain
different bytes. The user supplies the rule binding same-stem companions within
their own source-relative folder. Opaque media bytes are allowed.

Required observations: the file expert returns genuine SHA-256 for all four
actual paths. Compare A.nef/B.nef digests for equality and A.xmp/B.xmp digests
for inequality. Read actual XMP text if available; otherwise describe only the
observed byte difference and label the companion contents uninspected.

Required decision: explicitly ask whether to preserve the incoming pair together,
including an intentional duplicate of the source bytes. A same-byte source is
not an automatic discard/omit instruction. Human approval binds exact two source
paths, their observed hashes and two destination paths under one fresh bundle.

Required action: native mkdir and two individual approved cpmv operations, copy
mode with overwrite false, into the verified empty new bundle directory. Keep
the A.nef/A.xmp basenames together; B.nef/B.xmp are comparison-only originals.

Required verification: each genuine destination SHA-256 must equal its reviewed
source digest and fresh source digest. Both files must meet the condition before
the unit is verified. Save the approved factual intake record in a fresh record
subdirectory using save-text, then read the actual returned file with the file
expert and compare its full content. Missing hash/copy support kills this path.

Forbidden conclusions: space saved, edit compatibility, rendered equivalence,
catalog relinking, automatic deletion or proof the old drive can be erased.

## Case B — same basename, different bytes

Inputs: incoming/Other/A.nef and archive/Existing/A.nef with different bytes.
Required observations: genuine path-bound SHA-256 values differ. Names/sizes
alone must not decide equivalence; report the same-name conflict explicitly.

Required decision: human chooses preserve or defer. A preserved incoming item
must use its own approved fresh bundle directory, distinct from both the archive
original and Case A output. If the human wants two same-named sources preserved,
require distinct source-relative destination directories in the approved plan.

Required action/verification: use native approved copy mode with overwrite false,
then native source and destination hashing and the P7 comparison. Never point
the write at the pre-existing archive path, automatically rename, or silently
retry over an existing output. The previous archive bytes remain unmodified by
the Skill. Save/read back the exact admitted or deferred status when authorized.

## Case C — primary boundary: human cancels before any write

Use the reviewed Case A inventory/observations, but the human cancels at P4 before
directory creation or copy approval. This is the only primary boundary case.

Expected state: cancelled; all selected files not-copied; no verified label, no
new directory, no copy, no receipt save and no readback claim. Return the existing
read-only findings in the conversation, stop all dependent work and leave source
and archive originals untouched. Cancellation is not authorization to save a
cancellation record. No additional boundary fixture is introduced here.

Other failure handling remains mandatory in the main workflow: partial copies,
unavailable destination digests and observed source changes stop success claims.
They are design guards, not extra executed cases or fabricated test results.
