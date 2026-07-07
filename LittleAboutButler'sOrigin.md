# Butler — A Biography

<img width="358" height="205" alt="image" src="https://github.com/user-attachments/assets/e2e31271-fff2-49e6-aca4-eae03fa616c0" />

---

### What Butler Could Do

A translator yes, of course Butler could translate languages yes.

With the `!B` command, it could scrape DuckDuckGo, Yahoo, and Bing in real time, then hand everything off to Gemini to analyze and turn into an actual answer — pulling from among 2,500 search results.

It could post images, GIFs, and videos.

With `!B-V`, it could look at whatever image someone sent, along with the question that came with it, and answer directly. I used to run this through a local vision model *(mmproj)*; by the end, I'd handed that job to Gemini too, reading the image and the question straight off the message.

If someone went back and edited their message, Butler noticed. It would resync and re-translate to match whatever they'd changed, so nothing stale was left sitting in the chat.

### The Voice Pipeline

And the final piece: real-time voice translation.

I started this whole journey trying to run everything offline — GGUF models, hand-patched for a GPU nobody supported anymore. By the end, translation and voice ran almost entirely through APIs instead — Gemini, Groq — while image and video generation stayed the one piece that remained stubbornly local, still squeezed onto that same old GPU.

But "API-based" didn't mean the phone did nothing. Deciding when someone was speaking and cutting that audio into processable pieces — voice activity detection and chunking — all happened on the phone itself. From there, Groq's Whisper model handled transcription, for voice messages and live audio both. Gemini or Groq translated the text. A TTS model turned the translation back into audio. And Butler played that audio back through the mic automatically, so whoever was listening just heard the translation, live. Everything would run smoothly on RAM and caching 50 newest mesages for message-edit so that way Butler could works 24/7 without being worried to hit that OOM-WALL!

Keeping all of that running on a phone without it running out of memory or quietly dying mid-sentence was never the API's job to solve. That part was mine, and it took five months. By getting chunking and VAD to finally work together seamlessly, I built the feature I'd been struggling with since the start of the year.

### The Key System

Underneath all of it sat a system I was probably more proud of than anything user-facing: how Butler managed its own API keys.

Six Gemini keys rotated automatically, each one scored, with Butler always picking whichever was best at that moment. If Gemini failed completely, everything fell back to Groq, spread across three separate models.

But the part I actually cared about was how it handled failure. Butler isn't just doing blacklist a key the moment anything goes wrong — a 423, a 404, whatever — and never touch it again, even when the error was temporary and meant nothing. Butler didn't guess. If a key ran out of quota, Butler knew exactly how long until that quota reset — five hours, two hours, nine, whatever it actually was — and blocked the key for precisely that long, not a second more. Every other kind of failure — a request that wouldn't send, a rate limit, anything else — got its own penalty and its own delay, worked out separately for every key and every model. Nothing was ever blocked on a guess. Everything was blocked exactly as long as it deserved, with extra of a few minutes just incase the quota's reset time delay.

---

## Why Logic, First

I've never been able to leave a closed box alone. If something works, I need to know *why* it works — open it up, trace every wire, find the exact seam where cause turns into effect. That's just how I'm built. It has always been easier for me to trust a system I can take apart than a feeling I can't.

So when love handed me a problem that couldn't be reasoned with, I did the only thing I knew how to do with it: I turned it into something I could debug.

I didn't start learning to code because I loved technology.

I started because of a girl — Korean — and between us stood a wall of language that no dictionary or Google Translate could tear down.

I wanted to build a bridge. Not hire someone to build it — build it myself, with my own hands.

A friend told me: *"Just pay for a service, it's only a few bucks."* I heard him. I almost did it.

Then I didn't.

Because I didn't want to say *"I paid for this, just for you"* — I wanted to say *"I made this myself, just for you."* And that sentence became the foundation of everything that happened after.

---

## The Things That Refused to Run
*the first weeks*

I started from zero. Didn't know how to code. Didn't know what AI was. Didn't know how outdated my machine already was.

I fumbled through piecing tools together: Google Translate, Papago, Whisper for speech recognition. I thought that would be enough. But the translations came out wrong and stiff, sounding like a robot reading from a dictionary, with none of the warmth of a real conversation.

And my computer — an old GPU no longer supported by anyone — kept refusing everything I tried to install. Every guide online was written for newer machines. Every tool demanded something my machine didn't have.

Nobody built ready-made tools for hardware like mine anymore. It was like searching for spare parts for a car they'd stopped manufacturing long ago.

So I improvised. I built from source myself — diving straight into `ggml.cu` and `CMakeLists` to hand-patch what old hardware couldn't support. After countless failures, I got a tool running that nobody made for my machine anymore. For the first time, I'd built something instead of just installing it.

---

## When the Machine Gave Out Mid-Way
*soon after*

I wanted to run a real AI translator — not Google Translate. I wanted something that understood context, that understood how two young people actually talk to each other, not the way textbooks write it.

But my machine only had 8GB of VRAM. Speech recognition alone ate 2.5GB — I couldn't go smaller without the quality falling off a cliff. Add the translation model on top and the machine shut off immediately. Out of memory.

I tried every combination I could think of to squeeze both in. Nothing worked.

Eventually I gave up on running AI locally and accepted calling it over the internet instead of running it on my own machine. It hurt, but it was the reality.

And from that decision, a new idea surfaced: if I had to use the internet anyway, why not push the whole bot up to the cloud and let it run 24/7 without needing my machine on at all?

Thought it. Did it. The bot went up to the cloud. It ran. I was happy.

---

## The Bus Ride Home
*a few weeks later*

Then one day I went back to my hometown with my family.

On the road, the bot kept crashing — the RAM on the cloud server wasn't enough, and it would go down every few hours. I sat in the back seat watching error notifications roll in on my phone, one after another.

Instead of getting frustrated and letting it go, I opened my phone and asked an AI: what programming language is the most stable, the lightest on RAM for running on a server?

The answer: Rust. The hardest one. But the most stable, the most lightweight.

I nodded and started converting the code right there on the bus — on my phone, moving and building at the same time.

When I got home, I sat down and tested it. Errors, constant errors. I debugged until morning. No sleep.

But within just one or two days, the bot was running in Rust — deployed on Discloud, completely stable, using only **8MB of RAM**. A number the old Python version never came close to.

Later, when I brought the same bot home and ran it directly on my J3 Pro through Termux, it did even better: **0MB idle**, and never more than **11MB**, even under load.

---

## Never Satisfied
*the following weeks*

If the story had stopped there, it would already have been more than enough. But I didn't stop.

I wanted the bot to generate images — like the AIs everyone was posting online. To send to each other. So the bridge between us wasn't just words.

I started over again in completely unfamiliar territory: image-generating AI. Same old machine. Same old limitations.

This time there was another wall — the video-generation model I wanted to run was built for machines with double, triple the memory I had. In theory, impossible.

I found a way to use the hard drive as temporary memory — a technique almost nobody uses because it's too slow, but at least it worked *(disk offload via the Accelerate library)*. When the model file couldn't be read because of a format mismatch, I manually remapped it so the machine could understand it — using two different AIs arguing with each other to figure out the correct mapping *(key remapping for safetensors -> Diffusers)*.

It ran — but it took over four hours for a single generation. Completely unusable.

I gave up. Then I came back to it.

This time I discovered something even the GPU manufacturer hadn't documented clearly: my card processes a specific type of computation *(bfloat16)* more slowly than normal because it lacks a dedicated circuit for it — but precisely because there's no dedicated circuit, the computation routes directly into the main processing core instead of through a bottleneck. I exploited that.

Combined with a memory optimization technique *(SDPA — scaled dot-product attention)*, generation time dropped from over 1,000 seconds down to **153 seconds** for 81 frames — on a machine that, in theory, was never supposed to do any of this.

---

## The Name Butler
*after a month*

After more than a month, after dozens of versions, after sleepless nights and moments where I nearly walked away — the bot got a name.

**Butler.**

Not because the name sounds good, but because I wanted it to serve — quietly, reliably, always there — like a real butler standing between two worlds of language.

And even then, I didn't feel like it was done.

---

## The Voice That Wouldn't Come Easy
*months of failed attempts, then May 2026*

Somewhere in the middle of all this, a friend showed me a bot he used on Telegram. One feature stuck with me: it could translate voice messages. I was already deep into my own attempt at real-time voice translation around then, and his bot became a quiet kind of proof — proof that what I wanted wasn't impossible, just unbuilt by me yet. That conversation became the seed for everything voice-related I built afterward. Everything that grew from it, though, ended up living on Discord, not Telegram — Discord was already Butler's home, so that's where the voice became real.

I failed at it more than a hundred times in a row. Then I walked away for three months.

**May 14th, 2026.** Yun said she wanted a voice-translator. I frantically dove back into researching the steps to build one — the same project I had failed at over and over. The next day, **May 15th, 2026**, after testing it more than 30 times, it finally worked. Not perfect. But it worked. It felt like I was slowly conquering the very thing I'd walked away from three months earlier.

---

## The Sudden Stop — July 8, 2026
**Butler's shutdown**

After months of relentless effort, Butler finally ran flawlessly. And it did all of it — search, images, voice, the key-juggling underneath all of it — from Termux, on an old Samsung J3 Pro.

.....And it has been five days since Butler was last online.

I wanted to build a bridge to connect our hearts, to tear down the language barrier. I willingly pushed past limits I had never even approached before — not for money, not for a career, but for someone I ultimately could not keep. This project, and all the smaller ones around it, was just me trying to perfect a gift for the person I held so dear.

Butler was born because I wanted to bridge the gap with Yun. It is with both gladness and profound sorrow that I say Butler has completed its mission beautifully. It is time for Butler to rest after a long service.

I hope that one day I will cheer up and proudly say: *"Butler may have been born because of Yun, but it doesn't have to die because of Yun."*

But for now... thank you for your service, Butler. You did well.

---


