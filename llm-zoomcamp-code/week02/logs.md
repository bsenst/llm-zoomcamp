# Homework 3: Orchestration

## 2. The non-RAG response about Kestra 1.1 features is best described as

2026-07-05T13:54:14.515830Z INFO ❌ Response WITHOUT RAG (no retrieved context):
Kestra 1.1 introduced several exciting features that significantly enhanced its capabilities. Here are 5 major features with brief descriptions:

1.  **Worker Groups:** This was a highly anticipated feature allowing users to define and assign specific "groups" to workers and then configure tasks to run only on workers belonging to a particular group. This is crucial for:
    *   **Resource Isolation:** Running resource-intensive tasks on dedicated machines.
    *   **Security:** Restricting sensitive tasks to specific, secure environments.
    *   **Heterogeneous Environments:** Managing workflows across different types of infrastructure (e.g., GPU machines, specific OS versions).

2.  **Plugin Management UI:** Kestra 1.1 brought a dedicated section in the UI for managing plugins. Users could now easily browse, install, update, and uninstall plugins directly from the Kestra interface. This greatly simplified the process of extending Kestra's functionality, making it more accessible to users without deep technical knowledge of the backend.

3.  **Namespace-Level Defaults and Inputs:** This feature allowed users to define default values and input parameters at the namespace level. Instead of repeating common configurations in every flow within a namespace, they could now set them once at the parent level. This promoted:
    *   **DRY (Don't Repeat Yourself) Principle:** Reducing redundancy and making flows more concise.
    *   **Consistency:** Ensuring common parameters are uniform across flows in a namespace.
    *   **Easier Management:** Centralizing configuration for groups of related flows.

4.  **Flow-Level Labels:** Similar to worker groups, Kestra 1.1 introduced the ability to assign labels to flows. These labels could then be used for:
    *   **Filtering and Organization:** Easily finding and categorizing flows in the UI and through API.
    *   **Advanced Scheduling:** Potentially enabling more complex scheduling rules based on labels (though the immediate use was primarily for organization).
    *   **Policy Enforcement:** Allowing external systems or future Kestra features to act upon flows based on their labels.

5.  **New Secret Providers (AWS Secrets Manager & GCP Secret Manager):** Expanding on Kestra's secure credential management, version 1.1 added native support for popular cloud secret management services. This meant users could now directly integrate with:
    *   **AWS Secrets Manager:** Securely retrieve secrets stored in AWS.
    *   **GCP Secret Manager:** Securely retrieve secrets stored in Google Cloud Platform.
    This significantly improved the security posture and ease of use for Kestra deployments in AWS and GCP environments, allowing sensitive information to be managed by dedicated, enterprise-grade solutions.

🤔 Did you notice that this response seems to be:
- Incorrect?
- Vague/generic?
- Listing features that haven't been added in exactly this version but rather a long time ago?

👉 This is why context matters! Run `2_chat_with_rag.yaml` to see the accurate, context-grounded response.

## 3. What is the approximate output token count for multilingual_agent when running with summary_length = short?

2026-07-05T13:56:17.463049Z INFO ✅ RAG Response (with retrieved context):
Kestra 1.1 introduced several major features. Here are at least 5 of them:

1.  **New Filters**: The UI filters across Kestra were completely redesigned based on user feedback. The new design is cleaner, more intuitive, and more powerful, allowing users to choose from explicit options, reset filters with a single click, save frequently used combinations, and customize table columns.

2.  **No-Code Dashboard Editor**: Kestra 1.1 extended the No-Code Multi-Panel Editor to custom dashboards. Users can now build and customize dashboards directly from the UI without writing YAML, creating data sources, visualizations, and charts using form-based tabs.

3.  **Multi-Agent AI Systems**: AI agents in Kestra can now use other AI agents as tools, enabling sophisticated multi-agent orchestration workflows. This allows a primary agent to delegate subtasks to specialized expert agents.

4.  **Fix with AI**: When task runs fail, Kestra 1.1 can now provide AI-powered suggestions to help users quickly diagnose and resolve issues. This feature analyzes failed task runs and offers intelligent recommendations for fixing the problem.

5.  **Human Task**: For Enterprise Edition users, the new `HumanTask` allows for manual approval steps in workflows. When an execution reaches a human task, it pauses until designated users or group members approve and resume it, enabling human-in-the-loop workflows.

🎉 Note that this response is detailed, accurate, and grounded in the actual release documentation. Compare this with the output from 1_chat_without_rag.yaml!

## Token usage — medium summary

2026-07-05T13:58:12.523478Z INFO 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 135
- Total tokens: 417

English Brevity Agent:
- Input tokens: 150
- Output tokens: 41
- Total tokens: 191

💡 Tip: Monitor token usage to understand costs and optimize prompts!

## Question 3: Token usage — short summary

2026-07-05T13:59:49.055834Z INFO 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 91
- Total tokens: 373

English Brevity Agent:
- Input tokens: 106
- Output tokens: 49
- Total tokens: 155

💡 Tip: Monitor token usage to understand costs and optimize prompts!

## Question 4: Token usage — long summary

INFO 2026-07-05T14:00:36.700879Z 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 194
- Total tokens: 476

English Brevity Agent:
- Input tokens: 209
- Output tokens: 44
- Total tokens: 253

💡 Tip: Monitor token usage to understand costs and optimize prompts!

## Question 5: Modifying a flow

2026-07-05T14:02:36.432931Z INFO 📊 Token Usage Summary:

Multilingual Agent:
- Input tokens: 282
- Output tokens: 186
- Total tokens: 468

English Brevity Agent:
- Input tokens: 201
- Output tokens: 92
- Total tokens: 293

💡 Tip: Monitor token usage to understand costs and optimize prompts!
