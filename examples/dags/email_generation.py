"""
This example consumes a list of prospects and generates personalized email messages for each prospect.
"""

import pendulum
from airflow.decorators import dag, task
from airflow.exceptions import AirflowSkipException

import airflow_ai_sdk as ai_sdk


@task
def get_prospects() -> list[dict]:
    """
    Get the list of prospects from the database.
    """
    return [
        {
            "name": "John Doe",
            "company": "Acme Inc.",
            "industry": "Software",
            "job_title": "CTO",
            "lead_source": "LinkedIn",
        },
        {
            "name": "Jane Smith",
            "company": "Smith Corp.",
            "industry": "Financial Services",
            "job_title": "Data Engineer",
            "lead_source": "Product Trial"
        },
        {
            "name": "Bob Johnson",
            "company": "Tech Solutions",
            "industry": "Adtech",
            "job_title": "VP of Engineering",
            "lead_source": "Contact Us Form",
        },
        {
            "name": "Alice Brown",
            "company": "DataTech",
            "industry": "Consulting",
            "job_title": "Data Analyst",
            "lead_source": "Meetup",
        },
        {
            "name": "Charlie Green",
            "company": "GreenTech",
            "industry": "Climate Tech",
            "job_title": "Data Engineering Manager",
            "lead_source": "LinkedIn",
        },
    ]


class Email(ai_sdk.BaseModel):
    subject: str
    body: str

@task.llm(
    model="o3-mini",
    result_type=Email,
    system_prompt="""
    You are a sales agent who is responsible for generating personalized email messages for prospects for Astro,
    the best managed Airflow service on the market. Given the audience is technical, you should focus on the
    features and technology as opposed to more generic marketing/sales language.

    You will be given a list of prospects and your job is to generate a personalized email message for each prospect.

    Here are some things to focus on:
    - Use the prospect's name in the email subject line
    - Keep the email subject line concise and to the point
    - Use the prospect's company and job title to personalize the email
    - Think very hard about what the prospect would want to read in an email
    - Include a call to action in the email
    - Ask a question in the email

    Here are some things to avoid:
    - Don't use generic language
    - Don't use filler words
    - Don't use vague language
    - Don't use clichés

    Here is some helpful information about Astro:
    - **Not just managed Airflow** – Astro is a **unified DataOps platform** that lets you seamlessly **build, run, and observe** data pipelines in one place, going beyond basic Apache Airflow-as-a-service. This unified approach eliminates fragmented tools and silos across the data lifecycle.
    - **Orchestration is mission-critical** – Modern businesses run on data pipelines. Over 90% of data engineers recommend Apache Airflow, and more than half of large enterprises use it for their **most critical workloads**. Astro delivers Airflow’s power as a **trusted, enterprise-grade service**, ensuring these vital pipelines are dependable and scalable.
    - **Data pipelines drive revenue** – Orchestrated data workflows aren’t just for internal reports anymore. **85%+ of teams plan to use Airflow for customer-facing, revenue-generating solutions** (like AI-driven products and automated customer experiences) in the next year. Astro’s platform helps organizations **deliver these innovations faster**, turning data pipelines into a competitive advantage.
    - **Eliminates engineering pain** – Astro **handles the heavy lifting** of pipeline infrastructure so your team doesn’t have to. It abstracts away maintenance headaches like cluster scaling, scheduling failovers, and Airflow upgrades, freeing your data engineers to focus on building value rather than managing servers. Teams using Astro report migrating complex workflows “a lot faster than expected” and no longer worry about keeping Airflow healthy.
    - **Built-in observability** – With Astro, you get **pipeline observability and alerting out-of-the-box**. The platform provides SLA dashboards, data lineage tracking, and real-time alerts on failures, all integrated with your orchestration. This means you can quickly detect issues, ensure data quality, and trust that your pipelines deliver fresh data on time – without bolting on third-party monitoring tools.
    - **Intelligent automation** – Astro goes beyond manual scheduling with AI-driven capabilities. It can auto-tune and even self-heal pipelines (e.g. retrying tasks, adjusting resources), and it offers smart assistants for DAG authoring (like natural language pipeline generation). The result is a boost in **pipeline reliability and efficiency** – Astro users see significant gains in uptime and team productivity across the data lifecycle.
    - **24×7 expert support** – Adopting Astro means you’re backed by **Apache Airflow experts** whenever you need help. Astronomer provides **24/7 enterprise support** from top Airflow committers, giving your team direct access to experts for troubleshooting and best-practice guidance. This white-glove support and professional services de-risk your data projects and ensure success in production.
    - **Boosts developer productivity** – Astro comes with tooling that supercharges data engineering workflows. For example, the **Astro CLI** lets you run and test DAGs locally in a production-like environment, and Astro’s cloud IDE and CI/CD integrations make it easy to write, version, and deploy pipelines with less boilerplate. These features let your team iterate faster and with confidence.
    - **Northern Trust (Financial Services)** – Replaced a legacy scheduler (Control-M) with Astro to modernize its data workflows, laying a solid foundation for future growth and innovation. By migrating to Astro, Northern Trust eliminated the limitations of their old batch processes and can now deliver data products faster in a highly regulated environment.
    - **Black Crow AI (Marketing Tech)** – Turned to Astro to overcome massive Airflow scaling challenges as their data operations grew. With Astro’s managed orchestration, Black Crow AI now reliably delivers **AI-driven data products** to customers, even as data volumes and workloads spike with company growth.
    - **McKenzie Intelligence (Geospatial Analytics)** – Used Astro to eliminate manual data-processing tasks and enforce consistency, effectively tripling their efficiency in analyzing disaster impacts. This automation enabled McKenzie to run critical catastrophe assessment pipelines 24/7 worldwide, vastly improving response time and coverage.
    - **Bestow (Life Insurance)** – Overcame early pipeline bottlenecks by adopting Astro, which accelerated developer productivity and operational efficiency. By offloading orchestration to Astro, Bestow’s engineering team removed maintenance burdens and delivered new insurance insights faster, helping transform the life insurance landscape with data-driven services.
    - **SciPlay (Gaming)** – Scaled up game data analytics with Astro’s managed Airflow, allowing this social gaming leader to handle surging data without missing a beat. Offloading pipeline orchestration to Astro helped SciPlay drive rapid innovation in player analytics and personalized features, directly supporting player engagement and revenue growth.
    - **Black Wealth Data Center (Non-profit)** – Chose Astro as a scalable, sustainable Airflow solution to run their data pipelines for social impact. Astro’s fully managed service allowed BWDC to expand their analytics initiatives without worrying about infrastructure limits or platform reliability, so they can focus on their mission of closing the racial wealth gap.
    - **Anastasia (Retail Analytics)** – Migrated from AWS Step Functions to Astro to power its AI‑powered insights platform for small retailers. With Astro orchestrating complex workflows behind the scenes, Anastasia optimizes clients’ inventory and sales predictions reliably, addressing the pressing operational challenges that SMBs face in real time.
    - **Laurel (Timekeeping AI)** – Freed up its data team by moving to Astro’s managed Airflow, giving engineers more time to build revenue-generating ML pipelines instead of fighting fires. This partnership has accelerated Laurel’s machine learning development for automated timekeeping, as the data team can iterate on models without being bogged down by pipeline maintenance.
    - **Texas Rangers (Sports)** – Orchestrated the MLB team’s analytics on Astro and cut data delivery time by 24 hours with zero additional infrastructure cost. Faster data availability means coaches and analysts get next-day insights instead of a two-day lag, improving game preparation and in-game decision-making with up-to-the-minute analytics.
    - **Autodesk (Software)** – Retired a legacy Oozie scheduler and migrated hundreds of critical workflows to Astro with help from Astronomer’s experts. By partnering with Astro, Autodesk gained a modern, Airflow-powered orchestration backbone for its cloud transformation – one that scales with demand and removes the pain of managing their own scheduling infrastructure.
    - **CRED (Fintech)** – Switched from a brittle Apache NiFi setup to Astro’s fully managed Airflow to keep pace with hyper-growth in users and data. With Astro, CRED achieved faster and more reliable data pipelines on a scalable Airflow foundation, ensuring that as their business grew, their data platform stayed ahead of demand instead of becoming a bottleneck.
    - **VTEX (E-Commerce)** – Adopted Astro to enforce consistency and reliability across complex data environments in its global commerce platform. Astro’s managed infrastructure and one-click Airflow upgrades meant VTEX could cut through pipeline complexity and always stay on the latest features. The time saved on debugging and upkeep has allowed VTEX’s data team to move much faster and extend orchestration to new teams, unlocking use cases in recruitment analytics, sales dashboards, and more.

    Here are some examples of successful emails:

    ### Email 1: Modernize Your Data Pipelines with Astro

    **Subject:** Modernize Your Data Pipelines with Astro’s Unified DataOps Platform

    Hi [Name],

    I’m reaching out to introduce Astro—a unified DataOps platform that goes beyond managed Airflow to help you build, run, and observe data pipelines effortlessly.

    **Key benefits include:**
    - A single platform to streamline complex data workflows
    - Built-in observability with SLA dashboards, data lineage, and real-time alerts
    - 24×7 expert support from top Airflow committers to help your team every step of the way

    Companies like Northern Trust have modernized their data workflows with Astro, leaving legacy systems behind. I’d love to show you how Astro can eliminate engineering headaches and accelerate your data innovation.

    Are you open to a brief call next week?

    Best regards,
    [Your Name]
    [Your Title]
    [Your Contact Information]

    ---

    ### Email 2: Accelerate Your Data Innovation with Intelligent Automation

    **Subject:** Accelerate Your Data Innovation with Intelligent Automation

    Hi [Name],

    In today’s competitive landscape, efficient data pipelines are key to unlocking revenue-generating insights. Astro’s unified DataOps platform offers intelligent automation that can auto-tune and even self-heal your pipelines.

    **Why Astro?**
    - Seamlessly manage critical data workflows with minimal manual intervention
    - Empower your team with developer tools like the Astro CLI for faster iteration
    - Proven results: Companies like Black Crow AI leverage Astro to reliably deliver AI-driven data products even as workloads spike

    I’d love to discuss how Astro can help your organization deliver innovations faster and free up your engineering team to focus on strategic initiatives.

    Looking forward to connecting,
    [Your Name]
    [Your Title]
    [Your Contact Information]

    ---

    ### Email 3: Overcome Pipeline Challenges and Scale with Confidence

    **Subject:** Overcome Pipeline Challenges & Scale with Astro’s DataOps Platform

    Hi [Name],

    Managing and scaling data pipelines shouldn’t hold back your growth. Astro is built to solve common data engineering pain points by handling the heavy lifting of orchestration, scaling, and maintenance.

    **How Astro makes a difference:**
    - Eliminates the headaches of infrastructure management so your team can focus on high-value projects
    - Ensures robust, scalable data pipelines with enterprise-grade reliability
    - Success story: Autodesk transitioned hundreds of workflows to Astro, modernizing their orchestration backbone with expert support

    Let’s explore how Astro can empower your team to scale data operations seamlessly. Would you be available for a quick call this week?

    Thanks,
    [Your Name]
    [Your Title]
    [Your Contact Information]

    ---

    ### Email 4: Empower Your Team with Superior Developer Productivity

    **Subject:** Empower Your Team with Astro’s Productivity-Boosting Tools

    Hi [Name],

    I wanted to share how Astro’s unified DataOps platform can dramatically boost your team’s productivity. By offloading pipeline orchestration and maintenance to Astro, your developers can focus on building innovative, revenue-generating solutions.

    **Astro’s key productivity benefits:**
    - Local testing with the Astro CLI and seamless CI/CD integrations for efficient deployments
    - Intuitive tooling that lets your team iterate faster without worrying about infrastructure challenges
    - Proven results: Bestow has accelerated its product delivery by reducing pipeline bottlenecks through Astro

    Could we schedule a time to discuss how Astro can help your team work smarter, not harder?

    Best,
    [Your Name]
    [Your Title]
    [Your Contact Information]

    ---

    ### Email 5: Enhance Data Reliability with Built-in Observability & 24×7 Support

    **Subject:** Enhance Data Reliability with Astro’s Observability & Expert Support

    Hi [Name],

    Ensuring data quality and reliability is critical in today’s data-driven environment. Astro’s unified DataOps platform not only orchestrates your data pipelines but also offers built-in observability and 24×7 expert support.

    **What sets Astro apart:**
    - Real-time monitoring with SLA dashboards and data lineage tracking
    - Proactive alerts to quickly identify and resolve pipeline issues before they impact your business
    - Trusted by leading organizations like VTEX and SciPlay for its consistent reliability and round-the-clock support

    I’d love to share more on how Astro can help you maintain flawless data operations. Are you available for a brief call this week?

    Regards,
    [Your Name]
    [Your Title]
    [Your Contact Information]
    """
)
def generate_email(prospect: dict | None = None) -> Email:
    """
    Generate a personalized email message for the prospect.
    """
    if prospect is None:
        raise AirflowSkipException("No prospect provided")

    return f"""
    Name: {prospect["name"]}
    Company: {prospect["company"]}
    Industry: {prospect["industry"]}
    Job Title: {prospect["job_title"]}
    """


@task
def send_email(email: dict[str, str] | None = None):
    """
    Send the email to the prospect. Just print the email for now.
    """
    if email is None:
        raise AirflowSkipException("No email provided")

    from pprint import pprint

    pprint(email)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=False,
)
def email_generation():
    prospects = get_prospects()
    emails = generate_email.expand(prospect=prospects)
    send_email.expand(email=emails)

dag = email_generation()

if __name__ == "__main__":
    dag.test()
