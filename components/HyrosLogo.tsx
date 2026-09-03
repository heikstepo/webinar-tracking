/**
 * Hyros lockup: pixel mark + serif wordmark, drawn as vectors so it stays
 * crisp at any size and each piece can animate independently.
 *
 * The mark is an 8x9 cell grid — crenellated top, two square counters, and
 * slotted feet. Cells are merged into vertical runs per column so a column
 * carries a single transform; that is what the sweep-in staggers.
 */
const GRID = [
  "##.##.##",
  "########",
  "########",
  "########",
  "##.##.##",
  "########",
  "########",
  "##.##.##",
  "##.##.##",
];

const COLS = GRID[0].length;
const ROWS = GRID.length;

type Run = { y: number; h: number };

function columnRuns(col: number): Run[] {
  const runs: Run[] = [];
  let start: number | null = null;
  for (let row = 0; row <= ROWS; row++) {
    const filled = row < ROWS && GRID[row][col] === "#";
    if (filled && start === null) start = row;
    if (!filled && start !== null) {
      runs.push({ y: start, h: row - start });
      start = null;
    }
  }
  return runs;
}

const COLUMNS = Array.from({ length: COLS }, (_, col) => columnRuns(col));

/**
 * Columns are separate <g> elements so they can animate independently, which
 * leaves a hairline seam between them at non-integer render sizes. A sliver of
 * horizontal overlap closes it; at 1/160th of a cell it is not visible.
 */
const BLEED = 0.006;

/** Per-column entrance delay, in seconds. The left column lands first. */
const COLUMN_STAGGER = 0.045;

export const MARK_ASPECT = COLS / ROWS;

export function HyrosMark({
  height,
  animated = false,
  delay = 0,
  className,
}: {
  height: number;
  animated?: boolean;
  delay?: number;
  className?: string;
}) {
  return (
    <svg
      viewBox={`0 0 ${COLS} ${ROWS}`}
      width={height * MARK_ASPECT}
      height={height}
      className={className}
      fill="currentColor"
      role="img"
      aria-label="Hyros"
    >
      {COLUMNS.map((runs, col) => (
        <g
          key={col}
          className={animated ? "hyros-col" : undefined}
          style={
            animated
              ? { animationDelay: `${delay + col * COLUMN_STAGGER}s` }
              : undefined
          }
        >
          {runs.map((run) => (
            <rect
              key={run.y}
              x={col - BLEED}
              y={run.y}
              width={1 + BLEED * 2}
              height={run.h}
            />
          ))}
        </g>
      ))}
    </svg>
  );
}

export const WORDMARK_FONT =
  '"Playfair Display", "Bodoni MT", Didot, "Times New Roman", serif';

export default function HyrosLogo({
  /** Height of the mark in px; the wordmark is sized from it. */
  size = 180,
  animated = false,
  className = "",
}: {
  size?: number;
  animated?: boolean;
  className?: string;
}) {
  return (
    <div
      className={`inline-flex items-center text-hyros ${className}`}
      style={{ gap: size * 0.26 }}
    >
      <HyrosMark height={size} animated={animated} className="shrink-0" />
      <span
        className={animated ? "hyros-word" : undefined}
        style={{
          fontFamily: WORDMARK_FONT,
          fontWeight: 700,
          fontSize: size * 0.82,
          lineHeight: 1,
          letterSpacing: "-0.005em",
        }}
      >
        Hyros
      </span>
    </div>
  );
}
