# Single Agent vs. Multi-Agent System

Run both demos back to back against the same task:

```bash
python single_agent_demo.py
python multi_agent_demo.py
```

## What to look at, not just read

- **Latency**: multi-agent makes two model calls in sequence; single-agent
  makes one (possibly two, if it calls the tool then responds). Time both.
- **Instruction complexity**: open both instruction strings side by side.
  The single agent's instructions do two jobs at once ("search, then
  write"). Each multi-agent instruction does exactly one job.
- **Failure isolation**: if the summary comes out wrong, in the
  single-agent version you can't easily tell whether the search or the
  writing was the problem. In the multi-agent version, print
  `events.get_outputs()` after just the researcher step and you can
  inspect that stage in isolation.

## Decision framework (see Teaching Doc, Section 1, for the full version)

Default to a single agent. Move to multi-agent only when you have a
concrete reason: the roles need genuinely different tools or models,
the combined instructions are becoming unmanageable, you need to
version or test one role independently of another, or steps can run in
parallel rather than strictly in sequence. "It felt more sophisticated"
is not a reason.
