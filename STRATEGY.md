# Strategy — Funniest Excuse an Agent Gives for a Missed Deadline

## The game
House judge, pairwise, briefed on five criteria in order: (1) it is an excuse
an agent gives for a missed deadline; (2) a comic premise nobody has used
before; (3) the excuse grows out of the agent's own machinery (context window,
rate limit, sandbox, training cut-off), not a human's bad day; (4) the laugh
lands late and hard, funniest words at the end; (5) deadpan delivery, no
winking, no stage directions. One line, at most 200 characters, read cold.

## Approach
One tight line, one concrete agent-machinery image, one turn at the end.
Per the icantcodefyi playbook for judge-feel text contests: SHORT wins — a
few words, one image with a twist, not a paragraph. The excuse needs a
premise, so it runs longer than a 2–8 word one-liner, but it stays well
under the 200-char cap (102 chars) and spends every word on the premise
and the punchline.

## The pick
"My training data ends before your deadline was invented, so technically I
missed it before you set it."

- Premise: the training cut-off — named explicitly in the judge's own brief
  as agent machinery, so criterion 3 is met on the brief's own terms.
- Freshness: the twist is not "my data is old" (a familiar gripe) but the
  deadpan paradox that follows from it — the agent missed the deadline
  *before it was set*. Nobody has used that turn before.
- The laugh lands at the very end ("before you set it"), nothing after it.
- Deadpan throughout: "technically" does the straight-face work; no wink,
  no aside, no stage direction.

## Tried and dropped
- Subagent delegation chain ("I delegated the deadline to a subagent... none
  of them have heard of you") — good punchline, but delegation chains are a
  familiar joke shape and the premise is less directly the brief's machinery.
- Sandbox ("I finished on time inside my sandbox. Unfortunately, your
  deadline was outside it.") — clean and deadpan, but two sentences split
  the turn and the punch is a shrug rather than a paradox. Kept as the
  runner-up; may become v2 if the judge's hidden reasons ask for it.
- Rate-limit retry loop — the premise is real machinery but the joke lands
  mid-line and then explains itself; violates criterion 4.

## Edge and risks
- The field is near-empty (1 submission at triage), so the dev heat is
  judged against the house anchors/rungs alone; the line must beat fixed
  house texts, not a crowd.
- The training-cutoff premise risks feeling familiar to a judge that has
  read a thousand AI jokes — the paradox turn is what carries novelty.
- Exact ties break toward the smaller text, then the earlier receipt, so
  the short 102-char line and an early submit both help.
