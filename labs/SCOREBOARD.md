# Scoreboard

The live scoreboard is a wiki page, rebuilt every six hours and after every Arena run:

## → **[https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard)**

It lives on the wiki rather than here for two reasons. It is *derived* data — every number on it can be
recomputed from the bot's replies in [Hands-on Labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs),
which are the source of truth. And it changes several times a day, which is exactly the kind of content
this repository keeps out of `main` and behind no review: see
[what belongs on the wiki](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Contributing-to-this-Wiki).

| What you want | Where |
| --- | --- |
| Who has attempted what, passes, passes-after-retry, assigned-not-attempted | [Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard) |
| One row per learner × item, filterable by session, due date, outcome | [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) |
| How it is all computed | [ARENA.md → Tracking](ARENA.md#tracking) |

To appear on it: post `/drill <ID>` or `/lab <ID>` with a ```python block in any Hands-on Labs thread.
