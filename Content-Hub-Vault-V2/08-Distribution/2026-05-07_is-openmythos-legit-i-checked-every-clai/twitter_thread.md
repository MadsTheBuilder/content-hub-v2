# Twitter Thread

**Tweet 1:** OpenMythos: The idea of a 770M parameter model matching a 1.3B giant with 'recurrent depth' is compelling. But digging into the claims reveals a deep controversy. Is it true innovation or "credential laundering"? ðŸ§µ

**Tweet 2:** OpenMythos focuses on recurrent depth: looping the same calculation block multiple times instead of adding more layers. The goal is for models to "think deeper" with fewer parameters.

**Tweet 3:** The architecture has three stages. A "Prelude" encodes input, a "Recurrent Block" loops with shared weights, and a "KOD" projects the final state. It uses an update rule to prevent "drift" during loops.

**Tweet 4:** It performs "silent reasoning" in latent space, not generating visible chain-of-thought tokens. This could cut token costs and boost speed. Plus, it uses fine-grained Mixture of Experts (MoE) and Multi-Latent Attention (MLA) for memory efficiency.

**Tweet 5:** The big claim: a 770M parameter OpenMythos model matches a 1.3B parameter model's performance. This specific metric is where the controversy explodes.

**Tweet 6:** Critics allege "credential laundering." They claim the touted performance metric wasn't achieved by OpenMythos, but comes from a legitimate research paper called "Parse" published days *before* OpenMythos appeared.

**Tweet 7:** The repository has no trained weights, no benchmarks, no reproductions of claimed results. It's called a "PyTorch scaffold" or "fanfiction with a requirements.txt". Even worse: 21% of its *own* test suite fails on the main branch.

**Tweet 8:** OpenMythos is a credible architectural experiment, a "research playground" for recurrent depth. But it's not a finished model stack with "production confidence." It raises questions about validating open-source claims.

**Tweet 9:** Is OpenMythos legit? It's a fascinating look at next-gen model architectures, but the devil is in the details and the data. My full breakdown on what's real and what's not: [VIDEO_LINK]
