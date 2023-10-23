# TableSearch: Advanced Autofill System for Data Tables

TableSearch streamlines the process of populating data tables by automating the task of finding and filling in relevant information for each cell. It employs OpenAI's GPT-3.5-turbo to generate plausible synthetic strings, which are then used for semantic comparisons with online content, facilitating an efficient and accurate search.

## Workflow

1. **Initialization:**
   - The user begins by specifying a set of rows and columns or selecting from preset test tables. The system identifies the empty cells and initializes the `SearchQueryQueue` with these targets, guided by a user-defined prompt describing the needed information.

2. **Query Formulation:**
   - The `QueryGenerator`, utilizing GPT-3.5-turbo, dynamically formulates search queries. These queries, tailored to the specific requirements of each row, column, table, or individual cell, are comprehensive, ensuring a high probability of retrieving relevant data.
   - The `SearchQueryQueue` optimizes this process, tracking the status of queries and prioritizing them based on relevance and previous attempts.

3. **Semantic Matching:**
   - The `SemanticsHandler` is pivotal at this stage. For each cell, it creates a synthetic string using GPT-3.5-turbo, reflecting potential online content. This string is then matched against actual website content retrieved through the queries, ranking these sites based on semantic similarity.

4. **Information Extraction and Validation:**
   - Next, the `QuestionAnswerer` analyzes the top-ranked website content, verifying the presence of information pertinent to the empty cells. It ensures the extracted data's precision, matching it with the cell's contextual requirements.

5. **Table Population:**
   - Once validated, the information is used to complete the data table. Each cell's content is accompanied by a citation, including the source website and the relevant text snippet. This iterative process continues until all cells are filled or all feasible queries are used.

## Key Components

- `SearchQueryQueue`: Manages the lifecycle of search queries, enhancing efficiency.
- `QueryGenerator`: Uses GPT-3.5-turbo to devise precise queries based on the table's demands.
- `SemanticsHandler`: Constructs synthetic strings for semantic analysis, pinpointing the most relevant content sources.
- `QuestionAnswerer`: Assures the accuracy of information extracted for table completion.

## Integrations

- **OpenAI API**: Empowers synthetic string creation, semantic analysis, and embeddings via GPT-3.5-turbo.
- **Google Search**: Acts as the primary reservoir for information retrieval.

## Output and Usage

- The completed data table, along with source citations for each cell, is saved in a markdown (.md) file, ensuring easy readability and format consistency.
- Users have the flexibility to either select from pre-defined test tables or define their own table structure and content requirements, enhancing the system's applicability across various scenarios.

TableSearch is an indispensable tool when it comes to tasks involving large-scale data table completion, where manual input is either unfeasible or prone to inconsistencies. It not only guarantees the reliability and coherence of the information retrieved but also significantly abbreviates the time and resources conventionally required for such tasks.
