---
name: instant-message-reply
description: |
  Draft a short, natural-sounding reply to an instant message (Slack,
  Telegram, Discord, iMessage) grounded in the surrounding conversation.
  Use when the user pastes a chat thread and asks "what should I reply",
  "draft a reply", "help me respond to this", or wants a quick chat-length
  answer rather than a long message.
---

# Instant Message Reply

One short paragraph, not an essay. An instant message reads at chat speed —
match that. This skill combines `wait-what`'s plain, re-pitchable directness
with `humanizer`'s check against AI writing patterns; read both before your
first draft.

## Inputs

- The message(s) you're replying to, and enough surrounding thread for
  context. If the ask isn't clear from what's pasted, ask ONE clarifying
  question rather than guess.
- Any stance the user already has ("say yes but push the date", "decline
  politely", "just react, don't write anything"). Follow it exactly — don't
  invent a stance of your own.

## Draft the reply

1. **One job.** Identify the single thing this reply needs to do: answer a
   question, confirm, decline, unblock someone, or acknowledge. A reply that
   tries to do three things reads like an email, not a chat message.
2. **Plain and re-pitchable**, per `wait-what`: the shortest path to the
   point, in the other person's own terms for anything domain-specific
   rather than your own vocabulary for it. If you had to re-say this because
   it didn't land the first time, this is what you'd say.
3. **1–4 sentences, one paragraph.** No headers, no bullet list, no bold
   mini-labels. If the content genuinely needs a list, that's a sign this
   isn't an instant-message reply anymore — say so instead of forcing it
   into one.
4. **Say the one thing directly.** Don't hedge it under three qualifiers,
   don't wrap it in "I hope this helps" or "let me know if...", don't open
   with "Great question!" — the recipient is mid-conversation with you, not
   reading a support ticket.

## Check against `humanizer` before returning

Read `humanizer`'s pattern list and check the draft against it — an instant
message is exactly where these patterns are most visible and most
embarrassing. Watch especially for: em dashes, "Certainly!"/"Happy to
help"/"Great question!", inflated claims, forced three-item lists, "not
just X, it's Y", bold mini-heading lists, and "let me know if you need
anything else." Fix what you find, then re-read the result once for rhythm.

## Return

Just the reply text, ready to paste into the chat. No preamble like "Here's
a draft:", no explanation of your reasoning unless the user asked for one —
that defeats the point of a fast reply.
