"use client";

import { useState } from "react";
import HyrosLogo from "./HyrosLogo";

/**
 * The 16:9 title card: white stage, Hyros lockup sweeping in.
 *
 * Sequence — the mark's columns streak in from the left and assemble, the
 * wordmark wipes open behind them, then a single gloss band sweeps across the
 * finished lockup. `replayKey` remounts the animated subtree to restart it.
 */
export default function HyrosIntro({
  size = 180,
  replayKey = 0,
  className = "",
}: {
  size?: number;
  replayKey?: number;
  className?: string;
}) {
  return (
    <div
      className={`relative w-full overflow-hidden bg-white ${className}`}
      style={{ aspectRatio: "16 / 9" }}
    >
      <div className="absolute inset-0 grid place-items-center">
        <div key={replayKey} className="hyros-gloss-host relative">
          <HyrosLogo size={size} animated />
        </div>
      </div>
    </div>
  );
}

/** Title card plus a replay control — for previewing the animation. */
export function HyrosIntroDemo({ size = 180 }: { size?: number }) {
  const [replayKey, setReplayKey] = useState(0);

  return (
    <div className="w-full">
      <HyrosIntro
        size={size}
        replayKey={replayKey}
        className="rounded-xl border border-edge"
      />
      <button
        onClick={() => setReplayKey((k) => k + 1)}
        className="mt-4 rounded-lg border border-edge bg-panel px-3 py-1.5 text-sm text-slate-300 hover:border-accent hover:text-slate-100"
      >
        Replay
      </button>
    </div>
  );
}
