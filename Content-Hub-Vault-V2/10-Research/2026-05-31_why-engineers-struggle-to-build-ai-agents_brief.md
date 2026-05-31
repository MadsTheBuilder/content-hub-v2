---
date: 2026-05-31
niche: Why Engineers Struggle to Build AI Agents
repos_researched: 1
primary_sources_found: 1
notebook_ids:
  - cd7d480d-c8a4-42da-ae59-4b5392dbbacd
---

# Research Brief — Why Engineers Struggle to Build AI Agents
*2026-05-31 — 1 repos, each in its own notebook*

## youtube-3_gYbhABcAE
Source: https://www.youtube.com/watch?v=3_gYbhABcAE  
notebook_id: cd7d480d-c8a4-42da-ae59-4b5392dbbacd  

[Synthesis failed]

## Sources

- **Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind**


## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**How does agent development differ from traditional software engineering?**

### Briefing Document: Paradigm Shifts in AI Agent Development

This document outlines the fundamental differences between traditional software engineering and building AI agents, based on insights from Philipp Schmid (Google DeepMind). The core transition is defined as moving from a "traffic controller" mindset—where every step is controlled—to a "dispatcher" mindset, where the developer defines the goal and the agent determines the path [1].

---

#### 1. Development Lifecycle: From Specifications to Iterative Observation
In traditional software, developers follow a linear path: creating a specification/PRD, writing code, creating tests, and deploying [2]. Agent development is fundamentally iterative and observation-based.
*   **The Agent Loop:** Development involves defining instructions, running the agent, observing behavior, and then adjusting prompts or tools in a continuous loop to improve reliability [2].

#### 2. State Management: From Data Structures to Semantic Meaning
Traditional software relies on rigid data structures, booleans, and flags to manage state [1, 3]. In contrast, agents treat text and context as the primary state.
*   **Semantic Understanding:** Unlike traditional code that might only understand "accept" or "deny" for a plan, agents can capture semantic meaning. For example, a research agent can process a request to "approve the plan but focus on the US market and ignore California" in a single step [3].
*   **Dynamic Personalization:** Preferences like unit systems (Celsius vs. Fahrenheit) no longer need to be hard-coded flags; agents can dynamically adjust based on user context provided in natural language [4].

#### 3. Control Flow: Handing Over the "Steering Wheel"
A major pitfall for senior engineers is trying to force agents into deterministic, predefined workflows. 
*   **Dynamic Intent:** Traditional customer support might use classification models to trigger rigid workflows. Agents, however, must "trust into the LLM" to handle shifting intents dynamically [4, 5].
*   **"Stop Fighting the Model":** Developers are encouraged to stop trying to force specific step-by-step sequences. As Schmid notes, "we should start handing over control... we are no longer working in those purely deterministic environments" [4, 6].

#### 4. Error Handling: From Retries to Recovery
In traditional systems, HTTP requests are "cheap," and a failure usually results in simply rerunning the request [5]. For agents, errors must be treated as standard inputs.
*   **Preserving Context:** Because agent flows can take 5 to 15 minutes and consume significant compute, starting over upon failure is inefficient. 
*   **Forward Progress:** Developers must "design for recovery," treating a function call error similarly to a user input so the agent can understand the failure and keep moving forward in the flow [5-7].

#### 5. Quality Assurance: From Unit Tests to Evals
The non-deterministic nature of LLMs renders traditional unit testing (where Input A always equals Output C) insufficient [7].
*   **Probabilistic Reliability:** Agents must be measured through "evals" to determine how often they succeed over many runs. "We need to move from unit tests to eval... because agents are only successful if they are really reliable" [7, 8].
*   **Subjective Success:** Outcomes are often qualitative. Success might be measured by an "LLM as a judge" or human experts, focusing on whether the final result was achieved regardless of the specific steps taken [6, 8].

#### 6. Tooling & APIs: Building for Machine Consumers
Traditional APIs are built for developers who possess background context. Agent-ready tools require a different design philosophy.
*   **Semantic Interfaces:** Agents do not see the underlying code; they only see function schemas, tool definitions, and docstrings [9]. 
*   **Self-Documentation:** Tools must be "agent ready" and "self-documenting." For instance, an endpoint like `delete_item` needs an explicit docstring explaining its parameters and failure states, as the agent lacks the "years of experience" a human developer has with that specific API [6, 9].

#### 7. Summary of Principles for Engineers
*   **Build to Delete:** Acknowledge the "bitter lesson" that software is now disposable. Systems will be rebuilt frequently as better models and agentic patterns emerge [6, 10].
*   **Preserve Meaning:** Treat everything as context rather than trying to map every interaction to a database schema [6].
*   **Trust but Verify:** Give the agent the autonomy to reach the goal, but use rigorous evaluation frameworks to measure the success of the outcome [6].

**Follow-up: Control Flow — Conditions for Trusting vs. Constraining the LLM**

Philipp Schmid argues that engineers must shift from being "traffic controllers"—who dictate every street light and speed limit—to being "dispatchers" who define a goal but allow the agent to determine the specific steps to achieve it [1].

### When to Hand Over Control
Engineers should hand over control to the LLM when the desired outcome is complex or requires dynamic adjustments that are difficult to capture in a traditional, stateful workflow [2, 3]. Schmid emphasizes that engineers should "stop fighting the model" by trying to force it into a rigid, deterministic "step one, step two" structure [4]. Instead, they should trust the LLM's ability to understand semantic meaning and intent, allowing it to navigate the process non-deterministically [3, 5, 6].

### Failure Modes of Over-Constraining Agents
Schmid identifies several concrete failure modes that occur when engineers attempt to maintain too much deterministic control:

*   **Inability to Handle Dynamic Intent:** In a traditional customer support flow (e.g., subscription cancellation), a system might use a classification model to trigger a "predefined workflow" [2]. If the user changes their mind or introduces a new intent mid-flow, a rigid system cannot react dynamically to that shift in context [2, 3].
*   **Loss of Semantic Nuance:** In a "deep research" scenario, a deterministic system might only offer a binary "accept" or "deny" for a research plan [5]. This failure mode prevents the agent from processing nuanced human feedback, such as a user wanting to approve a plan while adding a specific constraint like "focus on the US market and ignore California" [5]. 
*   **Brittleness in Long-Running Tasks:** Traditional software assumes that if a sub-task (like an HTTP request) fails, the entire process can simply be restarted because compute is "cheap" [3]. However, if an agent is 15 minutes into a complex flow and the engineer has not designed for recovery or "handing over" the error back to the LLM as input, the system will fail by wasting massive amounts of compute to start from scratch [3, 6].
*   **Semantic Misalignment in APIs:** Engineers often build APIs assuming "developer expertise," such as a simple `delete item` endpoint [7]. Because agents do not have the context of years of backend development, an over-constrained tool definition that lacks a clear "semantic interface" or docstring will cause the agent to fail because it cannot "see" the logic behind the code [7].

**Follow-up: Evidence Basis for the Dispatcher Mindset**

Based on the provided transcript, Philipp Schmid does **not provide empirical evidence**, such as specific benchmarks or quantitative production metrics, to demonstrate that the dispatcher approach produces measurably better outcomes than predefined workflows.

Instead, he offers a conceptual and qualitative argument for why the dispatcher mindset is necessary when working with LLMs. His reasoning includes:

*   **Handling Complexity and Nuance:** Schmid argues that traditional "traffic controller" workflows (predefined steps and data structures) struggle to capture semantic meaning. For instance, in a "deep research" scenario, a dispatcher approach allows a user to provide additional context or refine a plan mid-stream, whereas traditional software would likely be limited to binary "accept" or "deny" flags [1].
*   **Dynamic Adaptation:** He points out that it is "very hard to model" all the unique differences and intents in stateful workflows, such as a customer support agent handling a subscription cancellation where the user might change their mind or provide a different intent mid-flow [2, 3].
*   **Non-deterministic Nature:** Schmid acknowledges that agents are not 100% reliable and can be "flaky" [4, 5]. Because they are non-deterministic, he argues that the goal is not to force the model into a rigid, deterministic workflow ("fighting the model") but to move toward **evals** to measure success rates and reliability [4, 5].

While he mentions that he sees these struggles "every day internally at Google," he frames the dispatcher approach as a necessary shift in engineering philosophy rather than a method proven by specific cited datasets or benchmarks [6, 7].

**Follow-up: Brittleness in Long-Running Tasks — Completion**

Philipp Schmid explains that for long-running agent tasks (which can take 5 to 15 minutes), engineers must stop treating failures as reasons to restart the process and instead treat **errors as normal inputs** [1], [2].

Regarding specific patterns for mid-flow recovery, Schmid provides the following guidance:

*   **The "Go" Analogy:** He points to the programming language Go as a conceptual model, where a function call can return either an error or a value, and both are treated with equal importance by the logic [1].
*   **Providing Errors to the LLM:** Instead of throwing an exception and restarting—which wastes significant compute and loses the existing context—engineers should provide the error information directly back to the model [2]. This allows the agent to understand what went wrong and attempt to keep going forward in the flow [2].
*   **Additional Checks and Workarounds:** He suggests implementing "other workarounds" or "additional checks" within the flow so the agent can recover dynamically rather than reverting to the beginning [2].
*   **Design for Recovery:** Because agents and models are not perfect, Schmid emphasizes that systems must be "designed for recovery" from the outset, acknowledging that "very weird things" will inevitably happen during longer tasks [3].

Schmid summarizes this approach as moving away from deterministic, stateful workflows where every failure is a hard stop, and instead trusting the LLM to handle the "semantic meaning" of a failure to find an alternative path to the goal [4], [5], [3].

**Follow-up: When to Keep Steps Deterministic**

Philipp Schmid does not articulate specific criteria or heuristics for which steps should remain deterministic; rather, his presentation focuses on why engineers should move away from deterministic frameworks when building agents [1, 2]. He argues that the primary struggle for senior engineers is the tendency to act as a "traffic controller" who defines every exact step, rather than a "dispatcher" who defines a goal and allows the LLM to determine the path to achieve it [1].

Regarding the failure modes of delegation, the sources provide the following insights:

*   **No Example of Over-Delegation Failure:** Schmid does not provide a concrete example where "over-delegating" to an LLM causes a failure. Instead, he frames the "trap" as the opposite: using traditional "predefined workflows" or "classification models" that cannot react dynamically to changing user intents [2].
*   **The Failure of Over-Control:** He cites a customer support scenario where a user wants to cancel a subscription. A traditional, deterministic workflow might use a classification model to trigger a rigid "churn" flow. However, if the agent fails to understand the semantic meaning or cannot adjust when a user changes their mind mid-stream, it fails to provide a good experience [2, 3].
*   **Reliability as the Primary Constraint:** While he doesn't warn against over-delegation, he does acknowledge that agents are non-deterministic and can be "flaky" [4, 5]. He notes that if a customer agent only works "one out of 10 times," it is not suitable for production [5]. 
*   **Recovery Over Determinism:** Rather than suggesting a return to deterministic steps to solve reliability issues, Schmid advocates for "designing for recovery" [6]. He suggests treating errors as normal inputs and providing them back to the model so the agent can attempt to keep going forward rather than starting the entire 5-to-15-minute process over from the beginning [3, 4].

In summary, Schmid’s stance is that engineers should "stop fighting the model" and avoid forcing it into specific "step one, step two" workflows, as software is increasingly becoming "disposable" in the face of better models [6, 7].

**Follow-up: What Evals Does Schmid Propose?**

Philipp Schmid describes evals as a shift from deterministic testing to probabilistic measurement, necessitated by the non-deterministic nature of AI agents where the same input does not guaranteed the same steps or results [1, 2].

Based on the source, here is how Schmid defines and structures evals:

### **What an Eval "Looks Like"**
Schmid defines an eval as a test of **reliability over multiple runs** rather than a binary pass/fail unit test [2]. Because agent results are often "subjective" (such as a research report or customer feedback scenario), evals move away from simple assertions to qualifying the output [2].

### **Metrics and Eval Structures**
Schmid mentions several specific metrics and methodologies for structuring these evaluations:
*   **Pass Rates:** Measuring "how often something works" or "how many times it passes" across a series of attempts [2].
*   **LLM as a Judge:** Using another model to evaluate the quality of the agent's output [2].
*   **Human Expert Review:** Utilizing human specialists to qualify subjective results [2].
*   **Tracing:** Monitoring the specific steps an agent takes. Schmid notes that an agent might take "four more steps" for one user than another, consuming more tokens, but the success should be measured by the final **outcome** rather than the specific path taken [2].
*   **Recovery Design:** Evaluating how well an agent recovers from errors, as agents are "not perfect" and will inevitably encounter "very weird things" in long-running flows [3].

### **Success-Rate Thresholds**
Schmid does not provide a universal "gold standard" percentage for success, but he offers a benchmark for failure:
*   **Failure Example:** He states that if a customer agent prompt "only works one out of 10 times," it is too "flaky" for production [2].
*   **Production Goal:** Engineers must "find the right balance" of success runs required to feel comfortable providing the tool to a user, emphasizing that agents are never "100% reliable" [3].

### **Concrete Before/After Improvements**
The source **does not show a concrete before/after improvement** (e.g., a specific case study where evals raised a success rate from X% to Y%). Schmid presents these concepts as high-level engineering principles and refers the audience to his blog for "deeper" content including "code examples" [4].

**Follow-up: Concrete Mechanism for Passing Errors Back to the LLM**

Philipp Schmid does not specify a concrete data format or provide a code-level call-site pattern in the provided transcript. While he discusses the mechanics of error handling conceptually, he focuses on the architectural shift rather than a specific implementation like a structured error object or system prompt injection [1, 2].

Based on the sources, the mechanical approach is described as follows:

*   **Treatment as Input:** Schmid states that errors should be treated as "normal input," very similar to how user input is handled [1]. Instead of letting an error crash the agentic flow or starting the process over—which would waste significant compute and context—the error should be "provided back to the model" [2].
*   **The Go Analogy:** Schmid references the Go programming language, noting that a function call can return either an error or a value and that developers "treat them kind of equally" [1]. He argues that agents should operate similarly: if something in the flow breaks, that failure becomes a piece of information for the model to use to determine the next step [1, 2].
*   **Recovery-Driven Design:** The goal is to design for "recovery" rather than deterministic success [3]. This involves implementing "additional checks" to ensure the agent keeps "going forward in the flow" rather than reverting to the beginning [2].
*   **Documentation vs. Code:** While he does not show a call-site pattern, he emphasizes that agents interact with tools through "function schemas and the dock strings" [4]. He suggests that these tools must be "agent ready" and "self-documenting" so the agent can understand how to use them and, presumably, how to handle their failures [3, 4].

Schmid mentions that deeper "code examples" are available on his blog, but they are not included in this source [5].

**Follow-up: What Are the 'Additional Checks and Workarounds'?**

Based on the sources, Philipp Schmid primarily discusses the concept of recovery and "additional checks" at the level of **principle**, rather than providing a granular, step-by-step example of a specific check [1-3].

The transcript highlights the following regarding his approach to these workarounds:

*   **Treating Errors as Input:** The most concrete technical strategy he offers is to treat an error from a function call or a step in the flow as a standard input, much like user input [1]. Instead of crashing or restarting the entire 15-minute process—which is compute-expensive and loses context—the error should be "provided back to the model" so the agent can attempt to understand the failure and move forward [2].
*   **The Go Analogy:** He references the programming language **Go**, noting that in that environment, a function call can return either an error or a value and they are treated "kind of equally" [1]. He argues that agent developers must adopt this same mindset [1].
*   **Designing for Recovery:** He emphasizes that "agents are not perfect" and "weird things" will happen in long-running flows, making it necessary to "design for recovery" rather than asserting for 100% reliability [3].

Schmid acknowledges the high-level nature of his talk, stating that while he provides the five examples of how building agents differs from traditional software, he directs developers to his **blog** for "deeper look with some code examples" [4, 5].

**Follow-up: LLM-as-a-Judge Implementation**

Based on the provided source, Philipp Schmid mentions "LLM as a judge" as a method for evaluating agents, but he does not provide specific technical details regarding its implementation or failure mitigation.

### Criteria and Prompt Structure
Schmid notes that because agent outputs—such as research reports or customer feedback—are "very subjective," traditional unit tests (where input A must equal output C) are insufficient [1, 2]. He suggests that an "LLM as a judge or human expert" can provide the necessary "qualifying feedback" to measure success [2]. However, the source **does not specify** the following:
*   **Criteria:** There are no defined rubrics or scoring metrics provided for the judge model [2].
*   **Prompt Structure:** He does not outline how to structure the prompt for the judge model [2].

### Prevention of Inherited Failure Modes
The source **does not address** how to prevent a judge model from inheriting the same failure modes as the agent it is evaluating. Schmid focuses instead on the high-level shift from deterministic testing to statistical evaluation (evals), emphasizing that:
*   We must measure how often a prompt works (e.g., 1 out of 10 times is not production-ready) [2].
*   The final "outcome" is the primary metric for success, even if the agent's internal steps vary [2].
*   Developers should "design for recovery" because neither models nor agents are perfect [3].

While he recommends using an LLM as a judge to handle the non-deterministic nature of agents, the source does not explore the meta-evaluation risks or technical safeguards for the judge itself [2, 3].

**Follow-up: Recovery Design Eval Structure**

Philipp Schmid discusses the necessity of "designing for recovery" and moving from unit tests to evaluations (evals), but he does not provide a detailed, step-by-step practical framework for a "recovery eval" in this specific talk [1, 2]. 

Based on the source, here is how Schmid addresses your specific points:

*   **Failure Conditions:** Schmid mentions failures such as an **HTTP request** or a **product search** breaking during an agent's flow [1, 3]. He notes that in traditional software, these are handled by simple retries, but for agents—which may run for 5 to 15 minutes—starting over is too expensive in terms of compute and loss of context [1].
*   **What Counts as Successful Recovery:** Success is defined as the agent's ability to "keep going forward in the flow" rather than "starting over from the beginning" [1]. He argues that errors should be treated as "normal input," similar to how the Go programming language treats errors as values, allowing the model to receive the error as context and find a workaround or additional check to proceed [1, 3].
*   **Recovery Quality vs. Task Completion Scoring:** Schmid does not explicitly state whether recovery quality should be scored separately from task completion. Instead, he emphasizes that we must measure the final **outcome** and **reliability** [4, 5]. He suggests using "qualifying feedback" through an **LLM as a judge** or a human expert to evaluate these subjective results, focusing on how many times a run is successful out of a total number of attempts (e.g., 1 out of 10 vs. a production-ready standard) [2, 4].

Schmid's core message regarding evals is to "evaluate and then don't only assert," recognizing that because agents are non-deterministic, we cannot simply assume input A will always lead to result C [1, 2]. While he advocates for designing for these "very weird things happening," the talk focuses more on the philosophical shift in engineering rather than the specific metrics of a recovery-specific score [2].

**Follow-up: Blog Code Examples for Recovery Checks**

The sources provided do not contain the blog post mentioned by Philipp Schmid, nor do they include any concrete code examples [1]. The source consists solely of a transcript from Schmid's talk at the "AI Engineer" event [2].

While the source does not provide code, Schmid describes the conceptual framework for treating errors as model input:

*   **Errors as Normal Input:** Schmid argues that if an agent's flow fails, the error should be treated similarly to a standard user input [3]. He compares this to how the Go programming language handles function calls, where a result can be either a value or an error, and both are treated with equal importance in the logic [3].
*   **Feeding Errors Back to the Model:** Instead of restarting a long-running agent process (which could take 5–15 minutes and waste significant compute), developers should "provide [the errors] back to the model" [4]. This allows the model to understand what went wrong and attempt to find a workaround or additional check to keep the flow moving forward rather than starting over [4].
*   **Design for Recovery:** Schmid emphasizes that because agents and models are not perfect, developers must "design for recovery" by ensuring the system can preserve context and meaning even when unexpected issues occur [5].

**Follow-up: 'Design for Recovery' — Concrete Mechanisms**

In the source, Philipp Schmid emphasizes that because agents are non-deterministic and imperfect, developers must **design for recovery** rather than assuming a perfect execution flow [1]. While he doesn't use the specific term "checkpoint-and-resume," his recommendations align closely with that concept and the idea of "error-as-input" [2, 3].

Schmid highlights the following specific patterns and considerations for recovery:

*   **Treating Errors as Inputs:** Schmid suggests that when a part of the agent flow fails (such as a function call), the error should be treated as a normal input, similar to a user input [2]. Instead of crashing or restarting, this error information should be **provided back to the model** so it can understand what went wrong and attempt to keep the flow moving forward [3].
*   **Avoiding "Start Over" Loops:** He specifically advises against traditional retry patterns that involve rerunning the entire process from the beginning [3]. He notes that for long-running agents (taking 5–15 minutes), starting over is too expensive in terms of compute and results in the loss of existing context [3].
*   **Maintaining Forward Momentum:** The goal of recovery design should be to ensure the agent continues "going forward in the flow" [3]. This might involve:
    *   **Additional checks:** Implementing validation steps to catch issues early [3].
    *   **Workarounds:** Creating paths that allow the agent to bypass a specific failure point rather than failing the entire task [3].
*   **Semantic Recovery:** Because agents can understand semantic meaning, recovery can involve the agent dynamically adjusting its plan based on feedback or errors, rather than following a rigid, predefined stateful workflow [4, 5].

Schmid contrasts this with traditional software where HTTP requests are cheap and simple retries are often the default; for agents, the complexity and cost of the "context" make simple retries an "anti-pattern" in long-running scenarios [2, 3].

**Follow-up: LLM Judge vs. Human Expert — Decision Criteria**

Philipp Schmid presents "LLM as a judge" and "human expert" as parallel examples of ways to provide "qualifying feedback" for subjective agent outcomes, but he does not provide specific guidance on when to choose one over the other [1].

In his presentation, Schmid highlights that evaluating agents is fundamentally different from traditional software because results—such as research reports or customer feedback scenarios—are "very subjective" [1]. To address this, he suggests that developers must move from rigid unit tests to evaluations ("evals") that measure how often an agent is successful [1, 2]. He lists "LLM as a judge" and "human expert" together as "a good way" to obtain the necessary qualifying feedback for these non-deterministic results, treating them as valid options for measuring success without explicitly discussing their relative trade-offs or selection criteria [1].

**Follow-up: LLM-as-Judge Rubric for Recovery Evals**

Based on the sources provided, Philipp Schmid **does not describe a specific rubric or set of criteria** for the LLM judge to use when evaluating recovery. 

While he advocates for using an "LLM as a judge" to provide "qualifying feedback" for subjective agent outcomes, he does not detail the specific prompts or scoring parameters the judge should follow [1]. The details of the judge prompt appear to be left to the implementer, though Schmid mentions that more in-depth information and code examples are available on his blog [2].

However, the sources do outline the **principles** of recovery that would likely inform such a rubric:

*   **Treating Errors as Input:** Agents should treat a failure (like a failed function call) as a normal input, similar to a user message, rather than a system crash [3].
*   **Maintaining Context:** A key goal of recovery is to avoid starting the entire process over, which wastes compute and loses existing context. Instead, the agent should "keep going forward in the flow" [4].
*   **Finding Workarounds:** Recovery involves providing error information back to the model so it can attempt "other workarounds" or "additional checks" to achieve the goal [4].
*   **Measuring Outcomes over Steps:** Schmid emphasizes that because agents are non-deterministic, the judge should focus on whether the final "outcome" was successful, even if the agent took different steps to get there [1].

**Follow-up: Production-Ready Reliability Threshold**

Philipp Schmid does not specify a specific numerical threshold for a "production-ready" standard in the sources [1], [2]. 

While he uses the example of a prompt only working **"1 out of 10 times"** as a rate that is clearly not suitable for production, he does not provide a corresponding target number (e.g., 9 out of 10) for success [1]. Instead, he frames the requirement as a qualitative "balance" that developers must find:

*   **No Fixed Number:** He states that developers "need to find the right balance between how many times our run need to be successful to provide it to the user" rather than citing a specific percentage [2].
*   **Basis of Assertion:** Schmid’s insights appear to be his own assertions derived from his professional experience at Google DeepMind. He notes at the beginning of the talk that he observes these challenges "every day internally at Google but also externally" [3].
*   **Shift in Methodology:** Rather than hitting a benchmark, he emphasizes a shift in testing methodology—moving from deterministic unit tests (where input A must always lead to output C) to "evals" that measure reliability over multiple runs because agents are inherently non-deterministic [4], [1].

He concludes that because agents are not 100% reliable, the goal of evals is to qualify the output through methods like "LLM as a judge" or human experts to determine if the outcome meets the specific needs of the use case [1], [2].

### Angle Battery

</details>

