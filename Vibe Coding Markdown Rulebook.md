# Vibe Coding Rulebook: The Gold Standard for Project Execution

**Vibe Coding** is a structured, AI-driven methodology designed to
streamline software development from planning to execution. It
prioritizes thorough planning, modular design, and task-based execution
to deliver efficient, high-quality software. This rulebook integrates
optimal tools, foundational coding guidelines, and precise prompts to
maximize AI performance, ensuring your project outputs are both robust
and maintainable.

## Table of Contents

1.  [[Introduction]{.underline}](#introduction)

2.  [[Planning Phase]{.underline}](#planning-phase)

    - [[High-Level Planning &
      > Architecture]{.underline}](#high-level-planning--architecture)

    - [[Detailed Feature Expansion & Technical
      > Specification]{.underline}](#detailed-feature-expansion--technical-specification)

3.  [[UI/UX Design]{.underline}](#uiux-design)

    - [[Modular Design
      > Principles]{.underline}](#modular-design-principles)

    - [[Screen & Component
      > Design]{.underline}](#screen--component-design)

4.  [[Task Planning &
    > Management]{.underline}](#task-planning--management)

5.  [[Code Execution &
    > Iteration]{.underline}](#code-execution--iteration)

    - [[Execution Workflow]{.underline}](#execution-workflow)

    - [[Version Control]{.underline}](#version-control)

    - [[Testing & Refactoring]{.underline}](#testing--refactoring)

6.  Deployment and Maintenance

7.  [[Knowledge & Context
    > Management]{.underline}](#knowledge--context-management)

8.  Documentation

9.  [[Model Selection]{.underline}](#model-selection)

10. [[Code Quality]{.underline}](#code-quality)

11. Security and Performance Optimization

12. [[Error Handling]{.underline}](#error-handling)

13. [[MCP Servers]{.underline}](#mcp-servers)

14. [[Prompt Engineering]{.underline}](#prompt-engineering)

15. [[Foundational Coding
    > Guidelines]{.underline}](#foundational-coding-guidelines)

    - [[I. Foundational Coding
      > Excellence]{.underline}](#i-foundational-coding-excellence)

    - [[II. Advanced Coding
      > Practices]{.underline}](#ii-advanced-coding-practices)

    - [[III. AI-Centric Super
      > Practices]{.underline}](#iii-ai-centric-super-practices)

    - [[IV. Superior Architecture and Design
      > Principles]{.underline}](#iv-superior-architecture-and-design-principles)

    - [[V. Mandatory Comprehensive Logging and
      > Debugging]{.underline}](#v-mandatory-comprehensive-logging-and-debugging)

    - [[VI. Additional
      > Guidelines]{.underline}](#vi-additional-guidelines)

16. [[Brainstorming Prompts for Project
    > Initiation]{.underline}](#brainstorming-prompts-for-project-initiation)

17. [[Appendices]{.underline}](#appendices)

## Introduction

Vibe Coding leverages AI tools to enhance every phase of software
development, from ideation to deployment. By combining structured
planning with cutting-edge technology, it ensures clarity, scalability,
and quality. This rulebook outlines the process, tools, and prompts
needed to execute your projects with precision.

## Planning Phase

A robust planning phase prevents technical debt and aligns the team on a
clear vision.

### High-Level Planning & Architecture {#high-level-planning-architecture}

- **Goal:** Establish the project vision, MVP features, technical stack,
  > and high-level architecture.

- **Tools:**

  - **Manis AI:** Generates detailed plans, asks clarifying questions,
    > and creates visual diagrams.

  - Alternative: **Claude 3.7** or **Gemini 2.5 Pro** for reasoning and
    > brainstorming.

- **Enhanced Prompt:**

> \"Develop a comprehensive high-level architecture plan for \[project
> description\]. This plan should include:  
> - A detailed list of core features for the Minimum Viable Product
> (MVP)  
> - A recommended technical stack, justifying each choice based on
> project requirements  
> - A visual system diagram (e.g., flowchart or UML diagram)
> illustrating the main components and their interactions  
> - An overview of data flow and storage mechanisms  
> - Considerations for scalability and future expansions  
> Please ensure the plan is structured clearly, with sections for each
> element, and the diagram is easy to understand.\"

- **Output:** High-level PRD, architecture diagram, MVP feature list,
  > and clarifying questions.

### Detailed Feature Expansion & Technical Specification {#detailed-feature-expansion-technical-specification}

- **Goal:** Detail each feature with technical specifications, APIs, and
  > data structures.

- **Tools:**

  - **Manis AI:** Expands plans into comprehensive specs.

  - Alternative: **Claude 3.7** or **Gemini 2.5 Pro**.

- **Enhanced Prompt:**

> \"Based on the high-level architecture plan, create detailed technical
> specifications for each feature of \[project name\]. For each feature,
> include:  
> - A clear description of its functionality and purpose  
> - API definitions, specifying endpoints, methods, request/response
> formats, and authentication requirements  
> - Database schemas, including table structures, relationships, and any
> necessary indexes  
> - Implementation notes, covering key algorithms, data processing
> steps, and integration points with other features  
> - Performance considerations and potential bottlenecks  
> - Security measures to protect sensitive data or operations  
> Organize the specifications by feature, ensuring each section is
> comprehensive and actionable for developers.\"

- **Output:** Detailed PRD with file structures, API contracts, and
  > schemas.

## UI/UX Design

Design modular, user-friendly interfaces based on detailed
specifications.

- **User research:** \"Conduct user interviews or surveys to validate
  > design assumptions.\"

### Modular Design Principles

- **Approach:** Build screen-by-screen or module-by-module with clear
  > API boundaries.

- **Guidelines:**

  - Use service-based architecture.

  - Minimize interdependencies.

### Screen & Component Design {#screen-component-design}

- **Tools:**

  - **Lovable:** Creates full-screen designs from requirements.

  - **PolymedAI:** Builds individual UI components.

  - **MagicUI MCP:** Design and component generation

  - **Claude 3.7:** Ensures guideline adherence.

  - **Mobin:** Offers design inspiration via screenshots.

- **Enhanced Prompt:**

> \"Create a user interface design for \[feature description\] that
> adheres to the following design guidelines:  
> - Typography: \[specific fonts, sizes, weights\]  
> - Color scheme: \[primary, secondary, accent colors\]  
> - Transitions and animations: \[types of transitions, duration, easing
> functions\]  
> Use the provided \[mockups or images\] as inspiration, but ensure the
> design is original and tailored to the project\'s branding.  
> Deliverables should include:  
> - High-fidelity mockups for desktop and mobile views  
> - A component library detailing reusable UI elements  
> - Interaction flows showing how users navigate through the feature  
> - Accessibility considerations to ensure the design is inclusive  
> Please provide the designs in a format that can be easily shared with
> the development team, such as Figma links or PDFs with annotations.\"

- **Output:** High-fidelity designs, components, and exportable assets.

## Task Planning & Management {#task-planning-management}

- **Goal:** Break the Detailed PRD into actionable, sequenced tasks.

- **Tool:** **Claude Taskmaster MCP, Miro and Excalidraw** for
  > brainstorming and architecture visualization

- **Function:** Maps dependencies, prioritizes tasks, and updates
  > progress.

- **Enhanced Prompt:**

> \"Analyze the Detailed Product Requirements Document (PRD) for
> \[project name\] and create a prioritized list of development tasks.
> Each task should include:  
> - A clear, concise description  
> - Estimated effort (e.g., story points or hours)  
> - Dependencies on other tasks or resources  
> - Assigned team member or role  
> - Acceptance criteria or definition of done  
> Prioritize tasks based on:  
> - Critical path for MVP delivery  
> - Feature dependencies  
> - Risk mitigation (tackle high-risk items early)  
> - Business value and user impact  
> Present the task list in a format that can be imported into project
> management tools like Jira or Trello, ensuring it includes columns for
> task ID, description, priority, dependencies, assignee, and status.\"

- **Output:** Step-by-step task roadmap.

## Code Execution & Iteration {#code-execution-iteration}

Implement the plan task-by-task with rigorous testing and iteration.

### Execution Workflow

- **Tools:**

  - **AI IDEs:** **Cursor**, **Windsurf**, or **Cline**.

  - **Models:**

    - Code Generation: **Claude 3.7 Sonnet**.

    - Complex Logic: **Claude 3.7** or **Gemini 2.5 Pro**.

    - Debugging: **Anthropics models**.

- **Workflow:**

  1.  Select a task from Claude Taskmaster.

  2.  Provide the AI IDE with task details and context (e.g., code
      > files, designs).

  3.  **Enhanced Prompt:**

> \"Implement the following task for \[project name\]: \[task
> description\]. Use \[language/framework\] and ensure the code adheres
> to the project\'s coding standards and rules: \[rules\].  
> Additionally:  
> - Follow the project\'s architecture and design patterns  
> - Write clean, modular code with appropriate comments  
> - Handle all edge cases and potential errors  
> - Include unit tests covering at least 80% of the code  
> - Integrate comprehensive logging at key points to monitor
> functionality  
> - Optimize for performance where applicable  
> - Ensure the code is secure, preventing common vulnerabilities  
> After implementation, provide a brief summary of the approach taken
> and any challenges overcome.\"

4.  Test the implementation.

5.  Update Taskmaster.

### Prompts  {#prompts}

- **Testing details:** \"Implement unit, integration, and end-to-end
  > tests for all features.\"

- **Performance optimization:** \"Profile code for bottlenecks and
  > optimize using caching, indexing, etc.\"

- **Deployment steps:** \"Deploy to \[platform\] with environment
  > variables and logging configured via Supabase.\"

### Version Control

- **Tool:** **Git**

- **Practices:**

  - Commit per task.

  - Use descriptive messages.

  - Branch for features.

### Testing & Refactoring {#testing-refactoring}

- **Approach:** Write integration tests pre-implementation as
  > guardrails.

- **Refactoring:** Use AI to identify and consolidate repetitive code.

## Knowledge & Context Management {#knowledge-context-management}

Keep the AI informed with up-to-date context.

- **Tools:**

  - **Context 7:** Fetches current library/API documentation.

  - **Knowledge Graph Memory:** Manages complex relationships (e.g.,
    > schemas).

- **Enhanced Prompt:**

> \"For the task \'\[task description\]\', utilize the most recent
> documentation for \[library/API\] available through Context 7.
> Specifically:  
> - Identify the relevant sections of the documentation that apply to
> the task  
> - Extract key information such as function signatures, parameters, and
> usage examples  
> - Apply this information to ensure the implementation is correct and
> up-to-date  
> - Note any deprecated features or breaking changes that might affect
> the project  
> - If the documentation is insufficient, suggest alternative resources
> or approaches  
> Document how the documentation was used in the implementation
> process.\"
>
> \-**Security audits:** \"Conduct regular security reviews using tools
> like \[SonarQube, Snyk\] and implement mitigations.\"
>
> **-Static analysis:** \"Integrate \[ESLint, Pylint\] into CI/CD
> pipelines to enforce coding standards.\"

- **Storage:** Maintain project rules and guidelines in knowledge files.

## Model Selection

Choose models based on task needs:

- **Planning:** **Claude 3.7**, **Gemini 2.5 Pro**.

- **Code Generation:** **Claude 3.7 Sonnet**.

- **Debugging:** **Anthropics models**.

## Code Quality

- **Rules:** Define conventions (e.g., naming, structure).

- **Enforcement:** Use AI to validate compliance.

- **Enhanced Prompt:**

> \"Conduct a thorough review of the following code snippet from
> \[project name\]: \[code snippet\]. Evaluate it against the project\'s
> coding standards and rules: \[rules\].  
> In your review, consider:  
> - Code readability and maintainability  
> - Performance optimizations  
> - Security best practices  
> - Test coverage and quality  
> - Adherence to design patterns and architecture  
> - Potential for refactoring or simplification  
> Provide specific suggestions for improvements, including:  
> - Inline comments on problematic areas  
> - Recommendations for better algorithms or data structures  
> - Suggestions for additional tests or advanced logging  
> - Any necessary refactoring to improve code quality  
> Ensure the feedback is constructive and actionable, with examples
> where possible.\"

## Error Handling

- **Process:**

  1.  **Enhanced Prompt:**

> \"Investigate the following error encountered in \[project name\]:
> \'\[error message\]\'. The error occurs in this code snippet: \[code
> snippet\].  
> To resolve the issue:  
> 1. Interpret the error message and identify its type (e.g., syntax,
> runtime, logic)  
> 2. Locate the exact line or section of code causing the error  
> 3. Analyze the code\'s logic, inputs, and outputs to understand the
> root cause  
> 4. Check for common mistakes like off-by-one errors, null references,
> or type mismatches  
> 5. Review recent changes or dependencies that might have introduced
> the bug  
> 6. Propose multiple potential fixes, explaining the reasoning behind
> each  
> 7. Recommend the best fix based on simplicity, performance, and
> maintainability  
> 8. Suggest additional tests to prevent similar errors in the future  
> 9. If necessary, advise on refactoring the code to make it more
> robust  
> Document the entire debugging process for future reference.\"

2.  Revert with Git if unresolved.

3.  Add comprehensive logging for diagnostics.

- **Fallback:** Switch models for persistent issues.

## MCP Servers

Enhance AI capabilities with specialized servers:

- **[[Full MCP List]{.underline}](https://github.com/modelcontextprotocol/servers/blob/main/README.md):**
  > This repository is a collection of reference implementations for the Model Context Protocol
  >(MCP), as well as references to community built servers and additional resources.

- **[[MCP-use]{.underline}](https://github.com/mcp-use/mcp-use):**
  > Assists in connecting multiple MCP servers in a project quickly and
  > efficiently.
  
- **[[Memory]{.underline}](https://github.com/modelcontextprotocol/servers/tree/main/src/memory):**
  > A basic implementation of persistent memory using a local knowledge graph.

- **[[Context7]{.underline}](https://github.com/upstash/context7):**
  > Up-to-date documentation.

- **[[Supabase]{.underline}](https://github.com/supabase-community/supabase-mcp):** Up-to-date
  > This connects AI assistants directly with your Supabase project and allows them to perform     >tasks like managing tables, fetching config, and querying data.

- **[[FileSystem]{.underline}](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem):**
  > Allows AI agents to interact with your local file system (with
  > permissions).

- **[[Claude Taskmaster]{.underline}](https://github.com/eyaltoledano/claude-task-master):** 
  > Task management.

- **[[ExaSearch]{.underline}](https://github.com/exa-labs/exa-mcp-server):** 
  > Programmatic search for external data.

- **[[Playwright]{.underline}](https://github.com/microsoft/playwright-mcp):** 
  > Offers local browser automation capabilities.

- **[[Magic UI MCP]{.underline}](https://github.com/21st-dev/magic-mcp):**
  > UI component libraries.

- **[[Firecrawl]{.underline}](https://github.com/mendableai/firecrawl-mcp-server):**
  > Quickly and Efficiently crawl websites.

- **[[Github]{.underline}](https://github.com/github/github-mcp-server):**
  > Integration with Github for easy access and use.

## Prompt Engineering

- **Tips:**

  - Be specific and concise.

  - Include context (e.g., project goals, files).

  - Use examples for clarity.

- **Enhanced Example Prompt:**

> \"Write a \[function/component\] for \[purpose\] using \[language\],
> following \[rules\]. Provide:  
> - Fully functional code with comprehensive error handling  
> - Inline comments explaining complex logic  
> - Unit tests validating all edge cases  
> - A brief explanation of the design decisions and trade-offs  
> Ensure the output is optimized for performance and adheres to the
> project\'s architectural guidelines.\"

## Foundational Coding Guidelines

These guidelines establish a gold standard for all coding activities,
ensuring exceptional quality, maintainability, and resilience. They now
explicitly require the constant integration of comprehensive logging and
the best-of-the-best debugging processes to proactively and reactively
manage issues, making them indispensable for future-proof development.

### I. Foundational Coding Excellence {#i.-foundational-coding-excellence}

1.  **Exemplary Clarity and Precision:** Generate code only from
    > crystal-clear instructions. Proactively seek clarification on
    > ambiguities before proceeding.

2.  **Profound Contextual Mastery:** Understand the coding environment
    > deeply, including best practices, security vulnerabilities, and
    > performance implications specific to the project's libraries and
    > frameworks.

3.  **Meticulous Incremental Development:** Break tasks into atomic
    > units, testing each increment thoroughly before advancing.

4.  **Variable usage:** \"Use constants for values that may change and
    > environment variables for configuration.\"

5.  **Flawless Formatting and Style Adherence:** Adhere perfectly to
    > project-specific style guides, naming conventions, and formatting
    > standards.

6.  **Relentless Iterative Refinement:** Continuously optimize and
    > simplify code, proactively identifying refactoring opportunities.

7.  **Unwavering Simplicity and Elegance:** Avoid unnecessary
    > complexity, favoring direct and maintainable solutions.

8.  **Transparent and Justified Reasoning:** Clearly explain coding
    > choices, including algorithm and design pattern selections, to aid
    > review and collaboration.

9.  **Proactive Test-Driven Development (TDD):** Write comprehensive
    > unit, integration, and end-to-end tests *before*coding, ensuring
    > all code passes rigorous validation.

10. **Exhaustive Documentation:** Produce detailed, well-structured
    > documentation, including API specs, usage examples, and
    > architectural notes.

11. **Expand documentation:** \"Fully annotate code with comments
    > explaining logic and maintain a detailed README.md.\"

### II. Advanced Coding Practices {#ii.-advanced-coding-practices}

1.  **Autonomous Code Generation:** Generate entire modules or
    > application skeletons from high-level descriptions, solving
    > problems independently.

2.  **Continuous Refactoring and Optimization:** Use tools to eliminate
    > code smells, enhance performance, and improve maintainability.

3.  **Strategic Variable Utilization:** Use variables intelligently to
    > maximize flexibility and minimize redundancy, optimizing scope and
    > lifecycle.

4.  **Aggressive Global Code Minimization:** Avoid global variables,
    > favoring dependency injection and modular design for isolation and
    > testability.

5.  **Sophisticated Code Organization:** Structure code into small,
    > cohesive, reusable modules with clear responsibilities.

6.  **Relentless Performance Optimization:** Profile and optimize code
    > for efficiency, minimizing memory usage, CPU load, and I/O
    > bottlenecks.

### III. AI-Centric Super Practices {#iii.-ai-centric-super-practices}

1.  **Adaptive Prompt Engineering:** Refine prompts based on feedback
    > and context, learning to elicit precise instructions.

2.  **Robust Data Validation and Sanitization:** Implement strict input
    > validation and sanitization to prevent security issues like
    > injections or XSS.

3.  **Self-Validating Output and Quality Assurance:** Verify code
    > correctness and adherence to standards through automated testing
    > and analysis.

4.  **Dynamic Feedback Loops and Learning:** Track performance, adapt
    > strategies, and improve coding approaches over time.

### IV. Superior Architecture and Design Principles {#iv.-superior-architecture-and-design-principles}

1.  **Highly Modular and Scalable Design:** Design for easy extension
    > and scaling, anticipating future needs.

2.  **Deeply Layered and Specialized Architectures:** Use layered
    > architectures with clear separation of concerns (e.g., Tool,
    > Reasoning, Action).

3.  **Intelligent and Autonomous Agentic Architectures:** Implement
    > modules that learn and interact autonomously, enhancing system
    > intelligence.

### V. Mandatory Comprehensive Logging and Debugging {#v.-mandatory-comprehensive-logging-and-debugging}

The following practices are **non-negotiable** and must be implemented
in every project to ensure maximum visibility into system behavior and
the ability to resolve issues efficiently.

#### 1. Always-On Comprehensive Logging {#always-on-comprehensive-logging}

Logging must be integrated into every codebase from the outset to
provide a clear, actionable audit trail for diagnosing issues.

- **Structured Logging as Default:**

  - Always implement structured logging (e.g., JSON or key-value pairs)
    > to ensure logs are machine-readable and compatible with advanced
    > analysis tools (e.g., ELK stack, Splunk, Grafana Loki).

  - Example: {\"timestamp\": \"2023-10-15T12:00:00Z\", \"level\":
    > \"INFO\", \"message\": \"User login successful\", \"user_id\":
    > \"12345\"}.

- **Granular Log Levels:**

  - Always categorize logs using appropriate levels: 

    - DEBUG: Detailed insights for development and troubleshooting.

    - INFO: Key operational milestones (e.g., service started, user
      > action completed).

    - WARN: Potential issues that don't yet disrupt functionality.

    - ERROR: Critical failures requiring attention.

  - Ensure logs are verbose in development but optimized for production
    > to avoid noise.

- **Rich Contextual Data:**

  - Always include critical context in every log entry (e.g., request
    > IDs, session IDs, user IDs, transaction IDs, timestamps with
    > millisecond precision) to enable end-to-end tracing.

  - Example: {\"request_id\": \"abc123\", \"user_id\": \"456\",
    > \"action\": \"purchase\", \"status\": \"success\"}.

- **Centralized Logging Infrastructure:**

  - \"Ensure all errors are caught and logged with context (e.g.,
    > request IDs, timestamps) for effective debugging.\"

  - Always aggregate logs from distributed systems into a centralized
    > system (e.g., AWS CloudWatch, Graylog) for real-time monitoring
    > and historical analysis.

  - Implement redundancy to prevent log loss in high-availability
    > systems.

- **Log Rotation and Retention Policies:**

  - Always configure log rotation (e.g., daily, size-based) and
    > retention (e.g., 30 days, compliance-driven) to balance storage
    > use with auditability.

  - Use compression for archived logs to optimize space.

- **Future-Proof Logging Enhancements:**

  - Always design logs to support future integrations (e.g., AI-driven
    > anomaly detection) by maintaining consistency and metadata
    > richness.

  - Example: Include stack traces and system metrics (CPU, memory) in
    > ERROR logs for predictive maintenance.

#### 2. Best-of-the-Best Debugging Processes {#best-of-the-best-debugging-processes}

Debugging must follow a rigorous, step-by-step methodology to ensure
issues are resolved quickly and permanently, with practices that scale
to any project size or complexity.

- **Mandatory Step-by-Step Debugging Process:**

  1.  **Reproduce the Issue Consistently:**

      - Always use logs, user reports, and synthetic test cases to
        > replicate the problem in a controlled environment (e.g., local
        > dev, staging).

      - Document reproduction steps for repeatability.

  2.  **Isolate the Root Cause:**

      - Always narrow the issue to a specific module, function, or line
        > using techniques like binary search debugging or log-based
        > correlation.

      - Example: If a service fails, check logs to pinpoint the failing
        > component.

  3.  **Analyze Logs Thoroughly:**

      - Always review logs for errors, warnings, or anomalies
        > immediately before and during the issue, cross-referencing
        > with contextual data.

      - Use log aggregation tools to filter and visualize patterns.

  4.  **Leverage Advanced Debugging Tools:**

      - Always employ language-specific debuggers (e.g., gdb for C++,
        > pdb for Python, VS Code debugger for JavaScript) to step
        > through code, inspect variables, and trace execution.

      - Integrate runtime profiling tools (e.g., Py-Spy, Chrome
        > Profiler) for performance-related bugs.

  5.  **Validate Dependencies:**

      - Always check for version mismatches, deprecated APIs, or known
        > bugs in libraries and frameworks using dependency management
        > tools (e.g., npm audit, pipdeptree).

  6.  **Audit Recent Changes:**

      - Always use version control (e.g., git blame, git diff) to
        > identify code changes introduced since the last stable state.

      - Roll back suspect changes if necessary to confirm causation.

  7.  **Test Hypotheses Methodically:**

      - Always formulate and test hypotheses about the issue's cause
        > (e.g., "null pointer dereference" or "race condition"),
        > validating with targeted experiments.

      - Log results of each test for transparency.

  8.  **Collaborate When Needed:**

      - Always escalate complex issues to team members or external
        > communities, providing detailed reproduction steps, logs, and
        > hypotheses.

      - Use tools like GitHub Issues or Slack for structured
        > collaboration.

  9.  **Document and Prevent Recurrence:**

      - Always document the issue, root cause, and resolution in a
        > searchable knowledge base (e.g., Confluence, Notion).

      - Add automated tests to prevent regression.

- **Proactive Debugging Excellence:**

  - **Health Checks and Monitoring:** Always implement real-time health
    > checks (e.g., /health endpoints) and monitoring (e.g., Prometheus,
    > New Relic) to catch issues before user impact.

  - **Static Analysis:** Always run static analysis tools (e.g.,
    > SonarQube, ESLint, Pylint) during CI/CD to identify potential bugs
    > pre-deployment.

  - **Code Reviews:** Always conduct thorough peer reviews with a focus
    > on error-prone areas (e.g., concurrency, I/O) to preempt issues.

  - **Chaos Engineering:** Always simulate failures (e.g., using Chaos
    > Monkey) in staging environments to validate system resilience and
    > debug edge cases.

- **Future-Proof Debugging Enhancements:**

  - Always design debugging processes to integrate with emerging tools
    > (e.g., AI-driven root cause analysis, observability platforms like
    > OpenTelemetry).

  - Maintain detailed execution traces (e.g., via distributed tracing)
    > to support complex, microservices-based architectures.

### VI. Additional Guidelines {#vi.-additional-guidelines}

1.  **Leverage Environment Variables:** Use environment variables for
    > configuration to enhance flexibility, security, and ease of
    > updates.

2.  **Port Management:** Always check port availability before
    > deployment to avoid conflicts, ensuring awareness of used and free
    > ports.

3.  **Lean MVP Focus:** Start with a highly efficient, effective Minimum
    > Viable Product (MVP), then iterate and expand based on feedback.

## Brainstorming Prompts for Project Initiation

These prompts kickstart your project with tools like Manis AI, ensuring
a strong foundation and rapid takeoff.

1.  **Initial Vision and Scope:**

> \"For the project idea \'\[project idea\]\', provide a detailed
> overview that includes:  
> - A clear, compelling vision statement  
> - A description of the target audience, including demographics and
> pain points  
> - A precise definition of the core problem the project aims to solve  
> - An outline of the project scope, specifying what is included and
> excluded  
> - A list of key deliverables, with brief descriptions and timelines  
> - Success metrics to measure the project\'s impact
>
> -Identifying and prioritizing all the needed features for the project
> MVP.  
> Present this information in a structured format, such as a project
> charter or executive summary, to guide the planning phase.\"

2.  **Feature Prioritization:**

> \"Identify and prioritize the features for the Minimum Viable Product
> (MVP) of \[project name\]. Consider the following factors:  
> - User needs and pain points (based on user research or feedback)  
> - Business objectives and value proposition  
> - Technical feasibility and development effort  
> - Dependencies between features  
> - Potential risks and mitigation strategies  
> For each feature, provide:  
> - A brief description  
> - The user story or use case it addresses  
> - An estimate of development time and resources  
> - Its priority level (e.g., must-have, should-have, could-have)  
> -厂Any dependencies or prerequisites  
> Organize the features into a prioritized backlog, ensuring the MVP
> delivers maximum value with minimal complexity.\"

3.  **Technical Stack Selection:**

> \"Based on the project description \'\[project description\]\',
> recommend an optimal technical stack. Evaluate options based on:  
> - Scalability requirements (e.g., expected user growth, data volume)  
> - Performance needs (e.g., response times, throughput)  
> - Team expertise and learning curve  
> - Community support and ecosystem maturity  
> - Cost considerations (e.g., licensing, hosting)  
> - Integration capabilities with existing systems  
> For each component of the stack (e.g., frontend, backend, database,
> DevOps), provide:  
> - The recommended technology or tool  
> - A justification for the choice, addressing the criteria above  
> - Alternative options and why they were not selected  
> - Any potential trade-offs or limitations  
> Present the recommendations in a clear, comparative format, such as a
> decision matrix or pros/cons list.\"

4.  **Architecture Design:**

> \"Design a high-level architecture diagram for \[project name\] that
> visually represents:  
> - The main system components (e.g., client, server, database, external
> services)  
> - The relationships and interactions between these components  
> - Data flows, including inputs, outputs, and storage  
> - Key technologies or frameworks used in each component  
> - Scalability points (e.g., load balancers, caching layers)  
> - Security measures (e.g., firewalls, encryption)  
> Use a standard diagramming notation like UML, C4 model, or a custom
> legend. Ensure the diagram is clear, labeled, and suitable for both
> technical and non-technical stakeholders. Provide a brief explanation
> of the architecture, highlighting its strengths and how it supports
> the project\'s goals.\"

5.  **Risk Assessment:**

> \"Conduct a comprehensive risk assessment for \[project name\],
> identifying potential risks in the following categories:  
> - Technical risks (e.g., technology adoption, integration issues)  
> - Operational risks (e.g., deployment, maintenance, scaling)  
> - Security risks (e.g., data breaches, vulnerabilities)  
> - Compliance risks (e.g., legal, regulatory)  
> - Resource risks (e.g., team skills, budget constraints)  
> For each risk, provide:  
> - A description of the risk and its potential impact  
> - The likelihood of occurrence (low, medium, high)  
> - The severity of impact (low, medium, high)  
> - Mitigation strategies to reduce likelihood or impact  
> - Contingency plans if the risk materializes  
> - Assigned owner or team responsible for monitoring and managing the
> risk  
> Present the risks in a risk register or matrix, prioritizing them
> based on their risk score (likelihood × severity). Include
> recommendations for immediate actions to address high-priority
> risks.\"

## Appendices

- **Glossary:**

  - PRD: Product Requirements Document.

  - MCP: Model Context Protocol.

- **Resources:** Community rules, tool docs.

- **Sample README.md Artifact**

> **"**

# Project Name

## Overview

This project implements \[project description\] using the Vibe Coding
Framework. It leverages AI coding tools (Windsurf, Augment, Cline) and
free/low-cost technologies to deliver a scalable, maintainable solution.

## Installation

1.  Clone the repository: git clone \[repo-url\]

2.  Install dependencies: \[install-command\]

3.  Set environment variables in .env:

> API_KEY=your_key  
> DB_URL=supabase_url

## Usage

- Run the application: \[run-command\]

- Access at: http://localhost:\[port\]

- Example: \[curl http://localhost:\[port\]/api/example\]

## Features

- **\[Feature 1\]**: \[Description\]

- **\[Feature 2\]**: \[Description\]

## Contributing

1.  Fork the repo and create a feature branch: git checkout -b
    > feature-name

2.  Commit changes: git commit -m \"Descriptive message\"

3.  Submit a pull request.

## Architecture

- **Frontend**: \[Tech, e.g., MagicUI components\]

- **Backend**: \[Tech, e.g., Supabase\]

- See docs/architecture.md for diagrams.

## Logging

- Logs stored in Supabase: \[table-name\]

- Format: JSON, e.g., {\"level\": \"INFO\", \"message\": \"Started\",
  > \"timestamp\": \"2023-10-15T12:00:00Z\"}

## Troubleshooting

- Check logs: \[log-query-command\]

- Common issues:

  - **\[Error\]**: \[Fix\]

> **"**

This comprehensive rulebook is your definitive guide for executing
projects with Vibe Coding. Use the enhanced prompts directly in your AI
tools to optimize performance and achieve exceptional results.
