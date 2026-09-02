-- FF4 Eligibility computation script

-- Add eligibility and reason columns if not present (idempotent for SQLite)
ALTER TABLE "FF4 Eligibility" ADD COLUMN IF NOT EXISTS eligible TEXT;
ALTER TABLE "FF4 Eligibility" ADD COLUMN IF NOT EXISTS reason TEXT;

-- Calculation logic for FF4 eligibility (mirroring Python + CSV logic, column names as in CSV)
UPDATE "FF4 Eligibility"
SET
    eligible =
        CASE
            -- Not eligible if Top 12 in *any* previous FF event
            WHEN
                ("FF1 Placing" > 0 AND "FF1 Placing" < 17)
                OR ("FF2 Placing" > 0 AND "FF2 Placing" < 17)
                OR ("FF3 Placing" > 0 AND "FF3 Placing" < 33)
                OR ("BB1 Placing" > 0 AND "BB1 Placing" < 9)
                OR ("BB2 Placing" > 0 AND "BB2 Placing" < 9)
                OR ("FF1 Placing" != -1 AND "FF2 Placing" != -1 AND "FF3 Placing" != -1)
            THEN 'No'
            ELSE 'Yes'
        END,
    reason =
        CASE
            WHEN "FF1 Placing" > 0 AND "FF1 Placing" < 17
                THEN 'Top 16 in FF1 (Placed #' || "FF1 Placing" || ')'
            WHEN "FF2 Placing" > 0 AND "FF2 Placing" < 17
                THEN 'Top 16 in FF2 (Placed #' || "FF2 Placing" || ')'
            WHEN "FF3 Placing" > 0 AND "FF3 Placing" < 33
                THEN 'Top 32 in FF3 (Placed #' || "FF3 Placing" || ')'
            WHEN "BB1 Placing" > 0 AND "BB1 Placing" < 9
                THEN 'Bracket finalist in BB1 (Placed #' || "BB1 Placing" || ')'
            WHEN "BB2 Placing" > 0 AND "BB2 Placing" < 9
                THEN 'Bracket finalist in BB2 (Placed #' || "BB2 Placing" || ')'
            WHEN "FF1 Placing" != -1 AND "FF2 Placing" != -1 AND "FF3 Placing" != -1
                THEN 'Played in FF1, FF2, and FF3'
            ELSE 'Eligible for FF4'
        END
;