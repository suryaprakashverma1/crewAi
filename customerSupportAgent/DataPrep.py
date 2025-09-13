import os

# 1️⃣ Create the instructions directory if it doesn't exist
os.makedirs('./instructions', exist_ok=True)

# 2️⃣ Define file contents
files = {
    "tech_startups_outreach.md": """Personalized Outreach Instructions for Tech Startups

Introduction
When engaging with tech startups, it's crucial to emphasize innovation, scalability, and how your solutions can aid in their growth and technological advancement. Startups are often looking for partners who understand their unique challenges and can offer flexible, cutting-edge solutions.

Key Points to Address
Innovation: Highlight how your products or services are at the forefront of technology.
Scalability: Discuss how your solutions can grow with their business.
Support: Emphasize the support and resources you provide, which are critical for startups.

Template Message
Dear [Name],

Congratulations on [Recent Achievement/News]! At [Your Company], we're excited about the innovative work you're doing at [Startup Name]. Our [Product/Service] is designed with tech startups like yours in mind, offering [Key Feature] to help you [Benefit].

We understand the importance of scalability and flexibility in your journey. [Insert how your solution can be tailored to their current and future needs].

Let's explore how we can support [Startup Name]'s growth together.

Best,
[Your Name]
""",

    "enterprise_solutions_framework.md": """Personalized Outreach Instructions for Enterprise Solutions

Introduction
Engaging enterprise clients requires a strategic approach that demonstrates ROI, reliability, and alignment with their business goals. Enterprises look for partners that understand their scale, compliance needs, and industry-specific challenges.

Key Points to Address
ROI & Value: Highlight measurable benefits and cost-effectiveness.
Reliability: Emphasize track record, security, and compliance.
Customization: Show how your solutions can integrate seamlessly with their existing systems.

Template Message
Dear [Name],

We at [Your Company] are excited about the opportunity to collaborate with [Enterprise Name]. Our [Product/Service] offers [Key Feature], designed to help your organization achieve [Benefit].

With a focus on reliability, compliance, and scalability, we tailor our solutions to meet the unique demands of enterprise clients like [Enterprise Name].

Looking forward to discussing how we can drive value together.

Best,
[Your Name]
""",

    "small_business_engagement.md": """Personalized Outreach Instructions for Small Businesses

Introduction
Small businesses value solutions that are affordable, practical, and easy to implement. Personalized messaging should emphasize support, simplicity, and growth potential.

Key Points to Address
Affordability: Demonstrate cost-effectiveness.
Ease of Use: Show how your solution is simple to adopt.
Growth Support: Explain how your offerings can help small businesses scale.

Template Message
Dear [Name],

Congratulations on the progress [Small Business Name] has made! At [Your Company], we provide [Product/Service] that is designed to help businesses like yours achieve [Benefit].

Our solutions are simple to implement and come with the support you need to grow and succeed.

We would love to discuss how we can support [Small Business Name]'s journey to growth.

Best,
[Your Name]
"""
}

# 3️⃣ Write files to the instructions directory
for filename, content in files.items():
    with open(os.path.join('./instructions', filename), 'w') as f:
        f.write(content)

print("Directory './instructions' created with 3 markdown files.")


print(os.path.exists('./instructions'))
