# Butler — A Biography

---

I didn't start learning to code because I loved technology.

I started because of a girl — Korean — and between us stood a wall of language that no dictionary or Google Translate could tear down.

I wanted to build a bridge. Not hire someone to build it — **build it myself, with my own hands.**

A friend told me: *"Just pay for a service, it's only a few bucks."* I heard him. I almost did it.

Then I didn't.

Because I didn't want to say *"I paid for this, just for you"* — I wanted to say *"I built this myself, just for you."* And that sentence became the foundation of everything that happened after.

---

## The Things That Refused to Run

I started from zero. Didn't know how to code. Didn't know what AI was. Didn't know how outdated my machine already was.

I fumbled through piecing tools together: Google Translate, Papago, Whisper — the speech recognition one. Thought that would be enough. But the translations came out wrong and stiff, sounding like a robot reading from a dictionary, with none of the warmth of a real conversation.

And my computer — an old GPU no longer supported by anyone — kept refusing everything I tried to install. Every guide online was written for newer machines. Every tool demanded something my machine didn't have.

Nobody built ready-made tools for hardware like mine anymore. It was like searching for spare parts for a car they stopped manufacturing long ago.

So I improvised. Built from source code myself — diving straight into `ggml.cu` and `CMakeLists` to hard-patch the things old hardware couldn't support — and after countless failures, I successfully built a tool that nobody made for my machine anymore, for the first time.

---

## When the Machine Gave Out Mid-Way

I wanted to run a real AI translator — not Google Translate. I wanted AI that understood context, understood how two young people actually talk to each other, not the way textbooks write it.

But my machine only had 8GB of VRAM. The speech recognition alone ate 2.5GB — I couldn't go smaller without the quality falling off a cliff. Add the translation AI on top: the machine shut off immediately. Out of memory.

I tried every combination I could think of to squeeze both in. Nothing worked.

Eventually I gave up on running AI locally — accepted calling it over the internet instead of running it on my own machine. It hurt, but it was the reality.

And from that decision, a new idea surfaced: *if I have to use the internet anyway, why not push the whole bot up to the cloud — let it run 24/7 without needing my machine on?*

Thought it, did it. Bot went up to the cloud. It ran. I was happy.

---

## On the Bus Ride Home

Then one day I went back to my hometown with my family.

On the road, the bot kept crashing — the RAM on the cloud server wasn't enough, it would go down every few hours. I sat in the back seat watching error notifications roll in on my phone, one after another.

Instead of getting frustrated and letting it go, I opened my phone and asked an AI: *what programming language is the most stable, the lightest on RAM for running on a server?*

The AI said: Rust. The hardest one. But the most stable, the most lightweight.

I nodded and started converting the code right there on the bus — on my phone, moving and building at the same time.

When I got home, I sat down and tested it. Errors, constant errors. Debugged until morning. No sleep.

But within just one or two days — **the bot was running in Rust.** Up on the server, completely stable, using only 8MB of RAM. A number the old Python version never came close to.

---

## Never Satisfied

If the story had stopped there, it would have already been more than enough. But I didn't stop.

I wanted the bot to generate images — like the AIs you see online. To send to each other. So the bridge between us wasn't just words.

So I started over again in completely unfamiliar territory: image-generating AI. Same old machine. Same old limitations.

This time there was another wall — the video-generation AI model I wanted to run was designed for machines with double, triple the memory I had. In theory: impossible.

I found a way to use the hard drive as temporary memory — a technique nobody uses for this because it's too slow, but at least it *worked* *(disk offload via the Accelerate library)*. When the AI file couldn't be read because of a format mismatch, I manually redrew the map so the machine could understand it — using two different AIs arguing with each other to figure out the correct mapping *(key remapping for safetensors → Diffusers)*.

It ran — but it took over four hours for a single generation. Completely unusable.

I gave up. Then came back to it.

This time I discovered something even the GPU manufacturer hadn't made clear in their documentation: my card processes a specific type of computation *(bfloat16)* more slowly than normal because it lacks a dedicated circuit — but precisely because there's no dedicated circuit, it routes directly into the main processing core without going through any middleman. I exploited that.

Combined with a memory optimization technique *(SDPA — scaled dot-product attention)* — and the generation time dropped from over 1,000 seconds down to **153 seconds** for 81 frames, on a machine that, in theory, was never supposed to do any of this.

---

## The Name Butler

After more than a month, after dozens of versions, after sleepless nights and moments where I nearly walked away — the bot got a name.

**Butler.**

Not because the name sounds good. But because I wanted it to serve — quietly, reliably, always there — like a real butler standing between two worlds of language.

And even now, I still don't feel like it's quite done.
