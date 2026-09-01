# LLM Intuition Bank
### MCQs, diagrams, error-fixing, and a systems recap — companion to Module 01


Zero math. Builds intuition, application, and key-term fluency. TravelMind is the running example.

**How to use this bank**

- Attempt each section closed-book first, then check the key at the end.
- Italic *Breadcrumb* lines are nudges, not answers. Read them only if stuck.
- Diagrams are plain ASCII, so they render in any markdown viewer.
- The recap at the end ties every concept into one mental model. Read it last.

---

## Section A: Single choice

*Guidance: one right option each. Watch for the option that is almost true.*

**A1.** An LLM produces a response by:
- a) retrieving the closest stored answer from a database
- b) predicting one token at a time, conditioned on every prior token
- c) searching the web and pasting the top result
- d) running a fixed script

**A2.** "Llama 4 Scout: 109B total parameters, 17B active" describes:
- a) a bug
- b) quantization
- c) a Mixture-of-Experts design
- d) fine-tuning

**A3.** Which nesting is correct?
- a) LLMs ⊃ Generative AI
- b) Generative AI ⊃ Foundation Models ⊃ LLMs
- c) Foundation Models ⊃ Generative AI
- d) Reasoning LLMs ⊃ LLMs

**A4.** One token is roughly:
- a) one letter
- b) one word
- c) about 4 characters of English
- d) one sentence

**A5.** `temperature = 0` means:
- a) fully deterministic and bit-exact every time
- b) greedy decoding, always take the highest-probability token
- c) the model is switched off
- d) randomness is mathematically impossible

*Breadcrumb: greedy and bit-exact are not the same claim.*

**A6.** "Lost in the middle" refers to:
- a) the model dropping the system prompt
- b) models attending less to the middle of a long context
- c) tokens being deleted at random
- d) the request timing out

**A7.** On most models, output tokens versus input tokens are:
- a) the same price
- b) cheaper
- c) 3 to 5 times more expensive
- d) free

**A8.** Which component turns token IDs into vectors?
- a) tokenizer
- b) embedding layer
- c) output head
- d) stop sequence

**A9.** Hallucination is best described as:
- a) a rare bug removed by retrying
- b) confident, plausible output that may be false, and a structural trait
- c) a hardware fault
- d) a network error

**A10.** A fresh API call carries no memory of earlier calls unless:
- a) you toggle a setting
- b) you resend the prior history yourself
- c) you pay for a higher tier
- d) you pick a larger model

**A11.** For high-volume intent classification in TravelMind, the sensible class is:
- a) Opus class
- b) Sonnet class
- c) Haiku class
- d) a reasoning model on max effort

**A12.** Open-weight models are the right call mainly when you need:
- a) the highest absolute capability ceiling
- b) zero infrastructure work
- c) data sovereignty and the option to self-host
- d) guaranteed native multimodality

**A13.** `max_tokens` controls:
- a) randomness
- b) a hard cap on output length
- c) the context window size
- d) the price per token

**A14.** The same prompt at `temperature 0.7`, sent twice:
- a) always matches exactly
- b) often differs, because sampling is probabilistic
- c) returns an error the second time
- d) costs double

**A15.** A 1M token context window guarantees:
- a) perfect recall across all of it
- b) a ceiling on input size, not a recall guarantee
- c) faster responses
- d) a lower bill

---

## Section B: Multiple choice

*Guidance: select all that apply. Most have two or three correct options. The wrong option is usually an absolute claim ("always", "all", "equal").*

**B1.** Tokens are a unit of:
- a) cost
- b) latency
- c) context budget
- d) a fixed count that is equal across all languages

**B2.** Two transformer LLMs can legitimately differ in:
- a) tokenizer
- b) alignment / RLHF approach
- c) dense versus Mixture-of-Experts
- d) the laws of probability they obey

**B3.** Ways to lower TravelMind's token bill:
- a) trim the system prompt
- b) drop to a smaller model class where quality holds
- c) cap `max_tokens`
- d) raise temperature

**B4.** Signs you should reach for a tool instead of the model's memory:
- a) you need today's live flight status
- b) you need a fact with a real citation
- c) you need a catchy tagline
- d) you need the current weather at the destination

**B5.** Which belong under the Foundation Model umbrella?
- a) LLMs
- b) large pre-trained image generators
- c) a hand-coded if-else rules engine
- d) reasoning LLMs

**B6.** True of Mixture-of-Experts models:
- a) total parameters exceed active parameters
- b) "looks huge, runs cheap"
- c) every parameter fires on every token
- d) inference cost can stay low relative to total size

**B7.** Which lower hallucination risk in production:
- a) retrieval / grounding
- b) guardrails
- c) evaluations
- d) raising temperature

**B8.** Because each API call is stateless:
- a) you must resend history for continuity
- b) history eats into the context budget
- c) longer history costs more tokens
- d) the model quietly stores your data between calls

**B9.** Which are inference knobs on the API surface?
- a) temperature
- b) top_p
- c) max_tokens
- d) the model's parameter count

*Breadcrumb: one of these is fixed when the model is trained, not set per request.*

**B10.** Picking a model by brand name alone is wrong because:
- a) variant differs (dense vs MoE)
- b) context windows differ
- c) cost per token varies widely
- d) all brands behave identically

---

## Section C: Diagrams to decipher

*Guidance: read the ASCII flow, then answer. Two diagrams have a deliberate mistake to catch.*

**C1.** Name the two blank stages, then explain the loop.

```
[ Prompt text ]
      |
      v
[  BLANK 1   ]        <- name this stage
      |
      v
[ Embedding layer ] <-----+
      |                   |
      v                   |
[ Transformer blocks ]    |
      |                   |
      v                   |
[ Output head ]           |
      |                   |
      v                   |
[  BLANK 2   ]        <- name this stage
      |                   |
      v                   |
[ Append token ] ---------+    loop: the appended token re-enters here
```

- BLANK 1 = ____________
- BLANK 2 = ____________
- Why does the arrow loop back? ____________

**C2.** One node is in the wrong place. Name it and say where it belongs.

```
        [ Generative AI ]
               |
               v
      [ Foundation Models ]
               |
               v
           [ LLMs ]
            /      \
           v        v
[ Reasoning LLMs ]   [ Image generator ]   <- something here does not belong
```

- Misplaced node: ____________
- Correct placement and why: ____________

**C3.** This pipeline is scrambled. Rewrite it in the right order.

```
[ Tokenizer ] -> [ Output head ] -> [ Transformer blocks ] -> [ Embedding layer ] -> [ Probabilities ]
```

- Correct order: ____________

**C4.** Everything below draws from one shared budget.

```
[ System prompt ]    --\
[ Chat history ]     ---\
[ Tool definitions ] ---+--> [ Context window budget ]
[ Retrieved chunks ] ---/
[ Room for output ]  --/
```

- If the budget is nearly full and the answer gets cut off, which two do you trim first, and why? ____________
- Which one can you almost never drop? ____________

---

## Section D: Spot the error and rectify

*Guidance: every line is wrong. Rewrite the corrected version in one sentence.*

**D1.** "`temperature 0` makes the model fully deterministic and bit-exact."

**D2.** "A 70B model is always smarter than a 7B model."

**D3.** "With a 1M token window, the model recalls everything in it equally well."

**D4.** "The model remembers our previous conversation on its own."

**D5.** "Output tokens are cheaper than input, so long replies are free money."

**D6.** "Hallucination is a bug we can fully patch out."

**D7.** "The same sentence in Hindi and English costs the same number of tokens."

**D8.** "Generative AI is a kind of LLM."

**D9.** "For TravelMind's refund-amount calculation we set `temperature 1.2` to keep it interesting."

**D10.** "To be safe, route every TravelMind message through the Opus-class model."

---

## Section E: Apply it (TravelMind)

*Guidance: short scenarios. Pick the option and give a one-line reason.*

**E1.** 50,000 inbound messages a day need their intent tagged before routing.
- Class: ________  Temperature: low / high  Reason: ________

**E2.** TravelMind drafts an empathetic apology for a 3-hour delay.
- Class: ________  Temperature: low / high  Reason: ________

**E3.** TravelMind confidently states a refund clause that does not exist in your docs.
- What is happening: ________  Fix 1: ________  Fix 2: ________

**E4.** A single user query in the agent flow burned roughly 6 times the tokens you estimated. Most likely reason?
- ________

**E5.** Decode the PM sentence in plain English.
> "Run TravelMind on Llama 4 Scout via Bedrock with a guardrail, low temperature, 200K context."
- Llama 4 Scout: ________
- Bedrock: ________
- guardrail: ________
- low temperature: ________
- 200K context: ________

---

# More question types

## Section F: Match the pair

*Guidance: match each term on the left to its one meaning on the right. Two terms are sampling knobs, do not swap them.*

| Term | | Meaning |
|---|---|---|
| F-a Tokenizer | | 1. caps how long the output can get |
| F-b Embedding layer | | 2. confident output that may be false |
| F-c Temperature | | 3. total params huge, active params small |
| F-d top_p | | 4. each token depends on all prior tokens |
| F-e max_tokens | | 5. randomness dial on token sampling |
| F-f Context window | | 6. filters content, PII, denied topics |
| F-g Hallucination | | 7. total text the model can hold at once |
| F-h Mixture-of-Experts | | 8. turns text into integer IDs |
| F-i Autoregressive | | 9. turns token IDs into vectors |
| F-j Guardrail | | 10. keeps the smallest set of top tokens whose probability mass clears a threshold |

---

## Section G: Put it in order

*Guidance: write the sequence. No math, just the right chain.*

**G1.** Order the inference stages: `Output head`, `Tokenizer`, `Sample token`, `Embedding layer`, `Transformer blocks`.

**G2.** Order the nesting from widest to narrowest: `LLMs`, `Generative AI`, `Reasoning LLMs`, `Foundation Models`.

**G3.** Order by cost per output token, cheapest first: `Opus class`, `Haiku class`, `Sonnet class`.

---

## Section H: Fill the blank, key terms

*Guidance: one word or short phrase per blank. Tests term recall.*

**H1.** Splitting text into integer IDs is the job of the ____.

**H2.** A window of 200K ____ holds roughly 300 pages of text.

**H3.** ____ sampling keeps the smallest set of top tokens whose probability mass passes a threshold.

**H4.** A model with 109B total but 17B ____ parameters is a Mixture-of-Experts.

**H5.** The trait where a model answers confidently but possibly falsely is ____.

**H6.** Because generation is ____, each token depends on every token before it.

**H7.** For TravelMind to recall a passenger across turns, the ____ must resend the history.

**H8.** A ____ filters PII and denied topics around the model.

---

## Section I: Odd one out

*Guidance: pick the item that does not belong and say why in a few words.*

**I1.** Opus class · Sonnet class · Haiku class · Tokenizer

**I2.** temperature · top_p · top_k · parameter count

**I3.** Hallucination · stale knowledge · no native memory · GPU overheating

**I4.** Retrieval · guardrails · evaluations · raising temperature

**I5.** Llama · Qwen · DeepSeek · GPT

---

## Section J: Complete the analogy

*Guidance: fill the blanks. Several answers can work, the key shows one good fit.*

**J1.** Tokens are to an LLM bill what ____ are to an electricity bill.

**J2.** A Mixture-of-Experts model is like a ____ that only wakes the specialist it needs.

**J3.** Lost in the middle is like reading a long ____ and best remembering the start and the end.

**J4.** A stateless API call is like a ____ that has no memory of your last visit.

**J5.** Routing across Haiku, Sonnet, and Opus is like assigning work to a ____, a ____, and a ____ by difficulty.

---

## Section K: True or false, then fix

*Guidance: mark T or F. For each F, write the one-line correction.*

**K1.** Foundation Models are a subset of LLMs.

**K2.** `temperature 0` is bit-exact deterministic.

**K3.** Output tokens usually cost more than input tokens.

**K4.** A 1M context window guarantees uniform recall.

**K5.** Open-weight models let you self-host for data sovereignty.

**K6.** Every parameter in an MoE model fires on every token.

---

## Section L: Compare and rank

*Guidance: relative order only, no numbers needed.*

**L1.** Rank by speed, fastest first: Opus · Haiku · Sonnet.

**L2.** Rank by cost per output token, cheapest first: Opus · Sonnet · Haiku.

**L3.** For the same meaning, rank token count low to high: an English sentence · the Hindi sentence.

**L4.** Rank by hallucination risk when ungrounded, lowest first:
- summarise a paragraph I pasted
- cite three papers from memory
- give today's flight status from memory

*Breadcrumb: which task already hands the model the facts it needs?*

---

## Section M: Say it to a PM in one line

*Guidance: plain business English, no jargon. One sentence each.*

**M1.** Why can't we just trust the model for live flight status?

**M2.** Why does our agent cost more than a single chat call?

**M3.** Why did the same prompt give two different taglines?

**M4.** Why use Haiku for classification instead of Opus?

**M5.** Why does the Hindi version of our bot cost more per message?

---

# Recap: the systems view

Read this after attempting the bank. It connects every concept into one model.

## The one-paragraph mental model

An LLM turns your prompt into tokens, predicts the next token from all the prior ones, samples it, appends it, and repeats. Output is probabilistic, bounded by a context window, frozen at a training cutoff, and stateless across calls. It completes plausible patterns, so it can sound certain and still be wrong. Every weakness has a named fix.

## How the pieces connect

```
INPUT:  prompt text  =  a sequence of tokens
            |
            v
MODEL:  tokenize -> embed -> transformer blocks -> output head
            |
            v
        sample one token (probabilistic) -> append -> loop
            |
            v
OUTPUT: tokens out   (you pay per token, longer = slower)


WHAT BITES                         WHAT YOU REACH FOR
- context window ceiling     ->    retrieval, chunking, summarise
- stale knowledge            ->    tools, live data
- no native memory           ->    resend history, memory store
- hallucination              ->    grounding + guardrails
- probabilistic variance     ->    temperature + evals / QA
```

The whole game is a trade among four forces: capability, cost, latency, and control. Model class sets capability and cost. Token count sets cost and latency. Knobs and grounding set control. Pick deliberately on every task, since no single model or setting wins everywhere.

## Decision heuristics

- High-volume classification or routing → Haiku class, low temperature.
- Balanced production quality → Sonnet class.
- Hard multi-step reasoning, low volume, high stakes → Opus class.
- The answer must be a fact → ground it with retrieval or a tool, never trust memory.
- Numeric or policy output → low temperature.
- Creative wording → moderate temperature.
- Continuity across turns → your app resends the history.
- Agent cost exploding → check token amplification from thinking, tools, retrieval, summarising.
- Data sovereignty required → open-weight, self-host or Bedrock with full control.

## Key terms in one line

- **Token:** the atomic unit of text, roughly 4 English characters, the thing you pay for.
- **Tokenizer:** turns text into integer token IDs.
- **Embedding layer:** turns token IDs into vectors.
- **Transformer block:** attention plus feed-forward, stacked many times, holds most parameters.
- **Output head:** produces a probability over the next possible tokens.
- **Autoregressive:** each token is generated using all the tokens before it.
- **Parameters:** the learned weights, "70B" is their count, not a quality guarantee.
- **Mixture-of-Experts:** huge total parameters but only a slice active per token, looks huge, runs cheap.
- **Context window:** how much text the model can hold at once, measured in tokens.
- **Lost in the middle:** weaker recall for the middle of a long context.
- **Temperature:** the randomness dial on sampling.
- **top_p:** nucleus sampling, the smallest top set of tokens whose probability mass clears a threshold.
- **max_tokens:** the hard cap on output length.
- **Hallucination:** confident, plausible, possibly false output, structural not a bug.
- **Guardrail:** a filter for content, PII, and denied topics around the model.
- **Foundation model:** a large pre-trained model adaptable to many tasks, the umbrella above LLMs.

---

# Answer key

## Section A
A1 b · A2 c · A3 b · A4 c · A5 b · A6 b · A7 c · A8 b · A9 b · A10 b · A11 c · A12 c · A13 b · A14 b · A15 b.

Traps: A5 is greedy, not bit-exact. A15 is a ceiling, recall stays uneven.

## Section B
- B1: a, b, c.
- B2: a, b, c.
- B3: a, b, c.
- B4: a, b, d.
- B5: a, b, d.
- B6: a, b, d.
- B7: a, b, c.
- B8: a, b, c.
- B9: a, b, c (parameter count is fixed at training, not a request knob).
- B10: a, b, c.

## Section C
- C1: BLANK 1 = tokenizer. BLANK 2 = sample a token from the probability distribution. The loop exists because generation is autoregressive, the new token becomes part of the input for the next forward pass.
- C2: the image generator is misplaced. LLMs are text models, an image generator is a sibling under Generative AI (its own foundation model for images), not a child of LLM.
- C3: Tokenizer → Embedding layer → Transformer blocks → Output head → Probabilities.
- C4: trim chat history and retrieved chunks first, they are usually largest and most compressible. The system prompt is the hardest to drop, it defines behaviour and tools. Reserve room for output or the answer truncates.

## Section D
- D1: greedy decoding, close to deterministic but not bit-exact.
- D2: data, training, and alignment matter more than size, a well-trained smaller model can beat a poorly trained larger one.
- D3: recall is uneven, often 30 to 50 percent of the advertised window for hard tasks.
- D4: each call is stateless, your application must resend the history.
- D5: output costs 3 to 5 times input, long replies are the expensive direction.
- D6: hallucination is structural, you mitigate with grounding and guardrails, you do not patch it out.
- D7: non-Latin scripts fragment into more tokens, Hindi usually costs more for the same meaning.
- D8: reverse it, an LLM is a kind of Generative AI.
- D9: numeric and policy tasks want low temperature, near 0.
- D10: route by task, Haiku class for high-volume classification, reserve Opus class for hard reasoning, or cost explodes.

## Section E
- E1: Haiku class, low temperature, high volume and a tight deterministic task.
- E2: Sonnet class, moderate temperature, balanced quality with warmth in the wording.
- E3: hallucination. Fix 1: ground answers in a knowledge base with retrieval. Fix 2: add a guardrail that blocks unverified policy claims.
- E4: agent token amplification, thinking, tool calls, retrieval, and summarising each consume tokens on top of the visible answer.
- E5: Llama 4 Scout is an open-weight Mixture-of-Experts model, looks huge and runs cheap. Bedrock is AWS's managed multi-provider foundation-model service that keeps data in your account. A guardrail filters content, PII, and denied topics. Low temperature means steadier, less random output. 200K context is how much text the model can hold at once, in tokens.

## Section F
F-a → 8 · F-b → 9 · F-c → 5 · F-d → 10 · F-e → 1 · F-f → 7 · F-g → 2 · F-h → 3 · F-i → 4 · F-j → 6.

## Section G
- G1: Tokenizer → Embedding layer → Transformer blocks → Output head → Sample token.
- G2: Generative AI → Foundation Models → LLMs → Reasoning LLMs.
- G3: Haiku class → Sonnet class → Opus class.

## Section H
H1 tokenizer · H2 tokens · H3 top_p (nucleus) · H4 active · H5 hallucination · H6 autoregressive · H7 application · H8 guardrail.

## Section I
- I1: Tokenizer, the rest are model size classes.
- I2: parameter count, the rest are request-time sampling knobs.
- I3: GPU overheating, the rest are real LLM limitations.
- I4: raising temperature, the rest reduce hallucination risk.
- I5: GPT, the rest are open-weight families.

## Section J (one good fit, accept reasonable variants)
- J1: units (kilowatt-hours).
- J2: a hospital with on-call specialists.
- J3: book or long report.
- J4: a receptionist who never met you.
- J5: a junior, a mid-level, and a senior.

## Section K
- K1: F. Reverse, LLMs are a subset of Foundation Models.
- K2: F. Greedy, close to deterministic, not bit-exact.
- K3: T.
- K4: F. Recall is uneven, lost in the middle.
- K5: T.
- K6: F. Only a slice of experts fires per token.

## Section L
- L1: Haiku, Sonnet, Opus.
- L2: Haiku, Sonnet, Opus.
- L3: English lower, Hindi higher.
- L4: summarise a pasted paragraph (lowest, facts are provided), then the two from-memory tasks are both high risk (fabricated citations, stale flight status).

## Section M (model one-liners)
- M1: its knowledge is frozen at a training cutoff, so live status must come from a tool, not memory.
- M2: an agent thinks, calls tools, retrieves, and summarises, and every step spends tokens on top of the visible reply.
- M3: the model samples from a probability distribution, so open-ended prompts vary run to run.
- M4: classification is a tight, high-volume task, Haiku is fast and cheap enough to run it at scale.
- M5: the tokenizer fragments non-Latin scripts into more tokens, so the same meaning costs more.
