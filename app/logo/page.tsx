import { HyrosIntroDemo } from "@/components/HyrosIntro";

export const metadata = { title: "Hyros — Logo Animation" };

export default function LogoPage() {
  return (
    <main className="mx-auto max-w-4xl px-5 py-10">
      <h1 className="mb-1 text-xl font-semibold text-slate-50">
        Hyros logo sweep-in
      </h1>
      <p className="mb-6 text-sm text-slate-500">
        16:9 title card. Mark columns streak in from the left, the wordmark
        wipes open, then a gloss band sweeps the lockup.
      </p>
      <HyrosIntroDemo />
    </main>
  );
}
