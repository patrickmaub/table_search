# TableSearch: Automated Data Table Completion with Precision

TableSearch is a groundbreaking solution that automates the filling of data tables by intelligently sourcing information and accurately inputting it into each cell. It harnesses the capabilities of OpenAI's GPT-3.5-turbo to generate synthetic strings that simulate potential content from the web. These strings are used in semantic comparisons with actual web data, ensuring a targeted and precise search process.

## System Workflow

1. **Initialization:**
   - Users begin by selecting from preset test tables or defining their own with specific rows, columns, and a guiding prompt. TableSearch identifies the empty cells in the table and prepares the `SearchQueryQueue` with these details.

2. **Adaptive Query Formation:**
   - The `QueryGenerator` utilizes GPT-3.5-turbo to craft context-aware search queries tailored to the specific requirements of each cell, row, column, or the entire table. These refined queries enhance the probability of retrieving relevant information.
   - The `SearchQueryQueue` efficiently manages the lifecycle of these queries, prioritizing and handling retries based on predefined logic.

3. **Semantic Matching:**
   - Here, the `SemanticsHandler` steps in, using GPT-3.5-turbo to create a synthetic string for each cell, indicative of expected online content. This string is then compared with actual web content fetched through the queries, ranking these sources based on their semantic similarity.

4. **Information Extraction and Validation:**
   - The `QuestionAnswerer` module analyzes the top-ranked web content to determine if it contains information that matches the context and requirements of the empty cells. This step is crucial in ensuring the accuracy and relevance of the information extracted.

5. **Table Population:**
   - Verified information is used to fill the data table. Each entry includes a citation with the source website and relevant content excerpt. This procedure continues until all cells are filled or all query options are exhausted.

## Key Components

- `SearchQueryQueue`: Coordinates the query process, enhancing search efficiency.
- `QueryGenerator`: Uses GPT-3.5-turbo to develop context-sensitive queries.
- `SemanticsHandler`: Produces synthetic strings and conducts semantic comparisons to pinpoint the most relevant content sources.
- `QuestionAnswerer`: Validates and extracts suitable information from the chosen content to populate the data table.

## External Integrations

- **OpenAI API**: Essential for generating synthetic strings, conducting semantic analysis, and providing embeddings, all through GPT-3.5-turbo.
- **Google Search**: Acts as the primary source for information retrieval.

## Usage and Output

- The completed data table, along with citations, is saved in a markdown (.md) file, ensuring easy readability and review.
- Users have the flexibility to choose from ready-made test tables or create their own, enhancing the system's applicability across various scenarios.

TableSearch is indispensable in environments where filling extensive data tables accurately is crucial. It significantly reduces the time and effort involved, providing reliable, consistent, and precise data entries.

## Running TableSearch

Follow these steps to set up and run TableSearch:

1. **Dependency Installation:**
   - Ensure Python is installed on your system.
   - In the project's root directory, install the necessary packages with:
     ```
     pip install -r requirements.txt
     ```

2. **Script Permission:**
   - Grant the main script execution rights using:
     ```
     chmod +x main.py
     ```

3. **Script Execution:**
   - Run TableSearch with the following command:
     ```
     ./main.py
     ```
   - You will receive prompts to either choose a predefined test table or specify your own parameters.

Enjoy the power of automated, intelligent data table completion with TableSearch!
