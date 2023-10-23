PRESET_TABLES = {
    1: {
        "prompt": "Compile a comprehensive dataset on leading technology innovators, detailing the founder's full name, year of establishment, headquarters, industry focus, key innovations, market capitalization, number of employees, operational reach, recent achievements, and upcoming projects.",
        "rows": ["Tesla", "SpaceX", "Neuralink", "Boring Company", "OpenAI", "Waymo", "Blue Origin", "Virgin Galactic", "DeepMind", "Boston Dynamics"],
        "columns": ["Founder", "Established", "Headquarters", "Industry", "Key Innovations", "Market Cap (USD Billion)", "Employees", "Countries Operated", "Recent Achievements", "Upcoming Projects"]
    },
    2: {
        "prompt": "Gather detailed environmental data on the world's major cities, including population, population density, green space coverage, average temperature, yearly rainfall, public transport usage, recycling rate, air quality, CO2 emissions, and environmental policy ratings.",
        "rows": ["New York", "London", "Shanghai", "Tokyo", "Delhi", "Sydney", "Cape Town", "Rio de Janeiro", "Paris", "Berlin"],
        "columns": ["Population", "Density (per sq km)", "Green Spaces (%)", "Annual Temp (°C)", "Yearly Rainfall (mm)", "Public Transport (%)", "Recycling Rate (%)", "Air Quality Index", "CO2 Emissions (per capita)", "Environmental Rating"]
    },
    3: {
        "prompt": "Source information on top medical research institutions, focusing on establishment dates, locations, research specializations, publication count, H-index scores, funding received, patent counts, affiliated Nobel laureates, known breakthroughs, and current major projects.",
        "rows": ["Johns Hopkins", "Harvard Medical", "UCL", "Mayo Clinic", "Karolinska", "Max Planck", "Pasteur Institute", "Cleveland Clinic", "Mass General", "Stanford Medicine"],
        "columns": ["Established", "Location", "Specialization", "Publications", "H-index", "Funding (USD Million)", "Patents", "Nobel Laureates", "Breakthroughs", "Current Projects"]
    }, 4: {
        "prompt": "Investigate and compile detailed policies of major US airlines concerning passenger compensation and benefits during travel disruptions. Focus on the specifics of reimbursement criteria, delay handling, lost baggage compensation, and provisions for accommodations in case of significant delays or cancellations.",
        "rows": ["Delta Airlines", "American Airlines", "Southwest Airlines", "United Airlines", "JetBlue Airways"],
        "columns": ["Reimbursement Criteria", "Delay Compensation (USD)", "Lost Baggage Compensation (USD)", "Accommodation Provisions", "Cancellation Benefits", "Customer Service Contact"]
    },
    5: {
        "prompt": "Compile a detailed dataset on the annual water levels of the Potomac River, focusing on measurements taken at different times of the year. Include data on the river's highest and lowest levels, average water temperature, rate of water flow, instances of flooding, implemented water management practices, and any notable changes in local flora and fauna. First, look for data on the University of Marylands site. If that doesn't work, do more broad and open searches.",
        "rows": ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
        "columns": ["Highest Level (feet)", "Lowest Level (feet)", "Average Temp (°C)", "Water Flow (cfs)", "Instances of Flooding", "Water Management Practices", "Flora Changes", "Fauna Changes"]
    },
    6: {
        "prompt": "Compile real-time statistics on the startup ecosystem in major global cities as of 2023. Include data on the number of startups founded in 2023, total funding received in 2023, highest-funded startups and their projects in 2023, new key investors emerged in 2023, and changes in startup density per 1,000 people compared to 2022.",
        "rows": ["Silicon Valley", "London", "Berlin", "Bangalore", "Tel Aviv", "Singapore", "Sao Paulo"],
        "columns": ["Startups Founded in 2023", "Total Funding 2023 (USD Billion)", "Highest-Funded Startups 2023", "New Key Investors 2023", "Change in Startup Density"]
    },
    7: {
        "prompt": "Conduct a real-time competitive analysis of key players in the automobile industry as of 2023. Analyze aspects such as market share in 2023, revenue for the fiscal year 2023, new areas of investment or divestment in 2023, R&D spending allocated for 2024, and key product launches announced for 2024.",
        "rows": ["Toyota", "Volkswagen", "Ford", "Honda", "General Motors", "Nissan", "Hyundai", "BMW", "Mercedes-Benz", "Tesla"],
        "columns": ["Market Share 2023 (%)", "Revenue FY 2023 (USD Billion)", "New Investments/Divestments 2023", "R&D Spending for 2024 (USD Billion)", "Announced Product Launches 2024"]
    },
    8: {
        "prompt": "Create a report on the latest advancements in renewable energy technologies as of 2023. Detail recent breakthroughs achieved in 2023, new projects initiated in 2023, government policies and subsidies introduced in 2023, and forecasted trends for 2024.",
        "rows": ["Solar Energy", "Wind Energy", "Hydroelectric Power", "Geothermal Energy", "Biomass Energy"],
        "columns": ["Breakthroughs 2023", "New Projects 2023", "Policies/Subsidies 2023", "Forecasted Trends 2024"]
    },
    9: {
        "prompt": "Analyze the current academic performance metrics of major universities as of 2023. Include acceptance rates for 2023, changes in international student enrollment in 2023 compared to 2022, major awards or recognitions received in 2023, new courses or programs introduced in 2023, and planned campus developments for 2024.",
        "rows": ["Harvard University", "MIT", "University of Cambridge", "University of Oxford", "Stanford University", "Yale University", "Princeton University", "Imperial College London", "University of Chicago", "California Institute of Technology"],
        "columns": ["Acceptance Rate 2023 (%)", "Change in International Students", "Awards/Recognitions 2023", "New Courses/Programs 2023", "Planned Developments 2024"]
    },
    10: {
        "prompt": "Find the highest-grossing movie globally in 2023.",
        "rows": ["Highest Grossing Movie"],
        "columns": ["Global Box Office (USD Billion)"]
    },
    11: {
        "prompt": "Identify the book that won the Man Booker Prize in 2023.",
        "rows": ["Man Booker Prize Winner"],
        "columns": ["Book Title"]
    },
    12: {
        "prompt": "Determine the city with the highest cost of living in 2023.",
        "rows": ["City with Highest Cost of Living"],
        "columns": ["City Name"]
    },
    13: {
        "prompt": "Discover the most subscribed-to YouTube channel as of 2023.",
        "rows": ["Most Subscribed YouTube Channel"],
        "columns": ["Channel Name"]
    },
    14: {
        "prompt": "Identify the person who was awarded the Nobel Peace Prize in 2023.",
        "rows": ["Nobel Peace Prize"],
        "columns": ["Winner's Name"]
    },
    15: {
        "prompt": "Find the fastest production car in the world in 2023.",
        "rows": ["Fastest Production Car"],
        "columns": ["Car Model"]
    },
    16: {
        "prompt": "Determine the best-selling video game globally in 2023.",
        "rows": ["Best-selling Video Game"],
        "columns": ["Game Title"]
    },
    17: {
        "prompt": "Find the tallest building in the world as of 2023.",
        "rows": ["Tallest Building"],
        "columns": ["Building Name"]
    },
    18: {
        "prompt": "Identify the most valuable publicly traded company in 2023.",
        "rows": ["Most Valuable Company"],
        "columns": ["Company Name"]
    },
    19: {
        "prompt": "Discover the most visited tourist attraction in the world in 2023.",
        "rows": ["Most Visited Tourist Attraction"],
        "columns": ["Attraction Name"]
    }






}
