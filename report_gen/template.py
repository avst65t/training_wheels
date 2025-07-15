import config

discl="""
This AI-generated health report is provided solely for general informational purposes, and under no circumstances should you rely on any part of its content to make decisions about your health or medical treatment. You are strongly advised to disregard any suggestions, conclusions, or interpretations put forth by this report unless they are expressly confirmed by a licensed healthcare professional. The AI technology that created this report, while designed to parse and analyze health-related data, does not possess the clinical judgment, training, or ethical accountability that comes with years of medical education and professional practice.

From the beginning, it is essential to understand that AI systems are inherently limited by the data they process and the algorithms that guide them. No matter how sophisticated the computational methods may be, these systems are susceptible to misunderstandings, factual inaccuracies, and critical omissions of context. In some instances, the AI may produce information that sounds legitimate 
yet is entirely incorrect—an occurrence commonly referred to as “hallucination.” Therefore, it is imperative that you treat any statement within this report with extreme caution and refrain from depending on its content as a basis for health-related actions.

Beyond potential errors in data processing, the AI is incapable of truly understanding the complexity of your personal health status. Each individual’s medical history, lifestyle, genetic background, and range of possible health concerns can be intricate and multifaceted. Because the AI cannot perform a physical examination, interpret diagnostic tests in real time, or engage in detailed discussions about your symptoms, it lacks the depth of insight that guides physicians, nurse practitioners, or other qualified healthcare providers. If you are experiencing any medical issue—whether urgent or routine—consulting a licensed medical professional is the only appropriate course of action.

This report also cannot ensure the accuracy of any information that you or others have provided, nor can it verify whether its own data sources are current or comprehensive. Even if the AI was given extensive medical research and literature, these materials can become outdated, and the system does not have the capacity to re-educate itself instantly whenever new discoveries or guidelines emerge. Thus, the content here might overlook recent breakthroughs in diagnosis or treatment that could be highly relevant to you.

It is equally important to recognize that AI systems, by their nature, can perpetuate or amplify biases reflected in their training data. If the underlying data does not represent diverse populations adequately—or contains systemic prejudices—those issues may be echoed in this report’s findings or interpretations. This bias can distort recommendations and pose a risk to anyone who unwittingly treats this document as an authoritative source. The best safeguard against such biases is to seek an in-depth evaluation from a medical professional who can personalize their advice to your specific medical and cultural needs.

Under no circumstances should you allow this document to direct your healthcare decisions or delay any medical treatment. Self-diagnosis or alteration of any prescribed medication based on AI-generated content can be hazardous and potentially life-threatening. This report’s role, if any, should be limited to prompting further questions or guiding additional research that you subsequently discuss with a qualified medical practitioner. Always remember that your health and safety require oversight by professionals who are licensed, experienced, and ethically bound to prioritize your well-being.

By reading or using this AI-generated health report in any manner, you acknowledge that the information contained herein is not medical advice, does not establish a doctor-patient relationship, and should not be regarded as a reliable source for making any health-related decisions. You also understand that the creators, developers, and distributors of this AI system disclaim any liability for harm, loss, 
or adverse outcomes that may occur from using or misusing the contents of this report. The document is presented “as is,” without warranties or guarantees of any kind, whether explicit or implied.

For the most accurate and trustworthy guidance, always consult healthcare providers who can properly evaluate your personal circumstances, conduct physical examinations, and order the necessary diagnostic tests to arrive at a well-substantiated medical opinion. Should you have lingering questions, concerns, or new symptoms, contact a licensed medical professional immediately. No part of this AI report can 
replace the clinical expertise and judgment that guide safe and effective medical care."""



intro=f"""
Dear {config.PATIENT_NAME},

We are pleased to provide the results of our comprehensive review of your health journey. At N1 Research LLC, we undertake a meticulous and thorough review of your entire health history with the aim of offering personalized and up-to-date insights into all aspects of your well-being. Our team of hand-selected and worldwide medical specialists collaborate to provide you and your personal healthcare 
professionals with a comprehensive analysis of your individual health trajectory. This report is based on your past and present health indicators, including your personal medical history, family history, lifestyle characteristics, and simple and complex laboratory and imaging studies. We also include a review of your relevant genetic and epigenetic markers and how they may impact your health. 
The integration and interpretation of this body of information serves as the basis for a holistic assessment tailored to your unique profile. It is important to note that our analyses are meant to complement rather than replace the expertise of your personal physicians. We do not provide direct medical care to you. Rather, the goal of our multispecialty medical team is to promote a deeper understanding of your bodily functions and to make you aware of potential options to safeguard or enhance your health and quality of life."""


report_structure=f"""Section 1. Health Report Overview

Section 2. Health Issues

Section 3. Medical History Review
3.1 Hypertension (HTN) and Cardiovascular Health
3.2 Lipid Profile and Atherosclerotic Risks
3.3 Abnormal Lab Values and Other Concerns
3.4 Summary and Areas for Focus

Section 4: Family History Analysis
4.1 Overview
4.2 Pedigree Analysis

Section 5: Hypertension & Contributing Factors
5.1 What Is Hypertension and Why Is it Important?
5.2 Modifiable Hypertension Risk Factors
5.3 Review of Your Blood Pressure Readings
5.4 Main Points & Recommendations

Section 6: Your Cardiac System Testing
6.1 Stress Testing/Electrocardiogram/Echocardiogram
6.2 Elevated Computed Tomography (CT) Coronary Calcium Score
6.3 Main Points & Recommendations

Section 7. Hyperlipidemia
7.1 Background
7.2 Lipid-Lowering Therapies
7.3 Updates
7.4 Main Points & Recommendations
7.5 Gallbladder Polyp

Section 8: Understanding Your Gut Microbiome
8.1 Introduction to the Microbiome
8.2 Diversity and Balance
8.3 Butyrate
8.4 Commensal Bacteria
8.5 Main Points & Recommendations

Section 9: Increased Echogenicity Noted on Liver Ultrasound
9.1 Background
9.3 Other Considerations
9.3.1 Autoimmune, Chronic Viral, and Toxin-Induced Hepatitis
9.3.2 Your Recent Testing for Hepatic Steatosis/Fibrosis
9.4 Main Points & Recommendations

Section 10: Pre-Diabetes
10.1 Background: Diabetes and Related Issues
10.2 Evaluation of Your Blood Sugar
10.3 Consequences Associated With Type 2 Diabetes.
10.5 Main Points & Recommendations

Section 11: Genetics, Epigenetics, and Aging
11.1 Background
11.2 Genetic Mutations
11.3 Risk for Cancer Development
11.4 Risk for Cardiovascular and Metabolic Diseases
11.5 Risks of Inflammatory Conditions or Autoimmune Disorders
11.6 Risk of Depression and Anxiety
11.7 Risk of Osteoporosis
11.8 Risk of Decreased Detoxification
11.9 Degradation of Drugs and Excess or Toxic Compounds
11.10 Response to Specific Medications
11.11 DNA Methylation
11.12 Risk for Thrombocytopenia
11.13 Risk for Severe COVID-19
11.14 Alkaptonuria
11.15 Other Notable Single-Nucleotide Polymorphisms
11.16 Recessive Genetic Disorders
11.17 Considerations: Interpretation of Genetic Alterations
11.18 Main Points & Recommendations

Section 12: Telomeres
12.1 Background
12.2 Telomere Length and Biological Age
12.4 Main Points & Recommendations

Section 13: Epigenetic Determinants of Health
13.1 Background
13.2 Epigenetic Clocks
13.2.1 DNAm and the Pace of Aging (DunedinPACE Test)
13.2.2 DNAm and Biological Age (OMICm Age Test)
13.2.3 DNAm and the Age of the Organs (SymphonyAge Test)
13.2.4 Epigenetic Clocks
13.3 Main Points & Recommendations

Section 14: Mild Obstructive Sleep Apnea
14.1 Background
14.2 Main Points & Recommendations

Section 15: Kidney Health
15.1 Introduction
15.2 How to Detect Kidney Disease
15.3 Do You Have Diminished Kidney Function?
15.4 Main Points & Recommendations

Section 16: Lifestyle Analysis: Stress
16.1 Chronic Stress Reactions
16.2 Stress Hormone Responses
16.3. Consequences of Chronic Stress
16.4 Your Cortisol Hormone Testing
16.5 Additional Notes for Managing Stress

Section 17: Lifestyle Analysis: Diet
17.1 Introduction: Why Is Nutrition Important?
17.2 Assessing Your Diet
17.3 Blood Sugar, Diabetes, Nutrition, and Diet
17.4 Dietary Health Concerns
17.4.1 How Is Hypertension Linked to Diet?
17.4.2 Lipids: Diet and Dyslipidemia
17.4.4 Exposure to Toxic Substances
17.5 Summary & Recommendations: Initial Key Dietary Points

Section 18: Inflammation and Immune System Disturbances
18.1 Background
18.2 Rheumatoid Arthritis (RA) Screening
18.3 Your Rheumatoid Factor Testing
18.4 Main Points & Recommendations
18.5 Thyroid Gland
18.6 Vitiligo
18.7 Main Points & Recommendations

Section 19: Borderline-Low Platelet Counts
19.1 Background
19.2 Do You Have a Platelet Disorder?

Section 21: Abnormal Bone Mineral Density
21.1 Introduction to Bone Health
21.2 DEXA Scan Background
21.3 Your DEXA Scan Results
21.4 Vitamin D
21.5 Tests of bone turnover
21.6 Main Points & Recommendations

Section 22: Other Health Conditions
22.1 Maxillary Sinus Polyp
22.2 Follow-Up Sleep Studies

Section 23: Summary and Recommendations Recap
23.1 Cardiovascular
23.2 Hyperlipidemia
23.3 Osteopenia
23.4 Blood Sugar
23.5 Stress Management
23.6 Borderline-Low Platelet Levels
23.7 Gallbladder and Maxillary Sinus Polyps
23.8 Rheumatoid Factor Elevation

Appendix 1
1. Aluminum
2. Lead
3. Mercury
4. Nickel
5. Copper

Appendix 2
Low Levels of Micronutrients
1. Chromium
2. Selenium
3. Molybdenum
4. Choline
5. Folate (Vitamin B9), B12, and B6

Appendix 3
The Mediterranean Diet
Fermented Foods
Grain-Based Fermented Foods:
Fermented Beverages:
Fermented Fish and Meat Products:
Other Fermented Foods:

Appendix 4
Exercise

Appendix 5
Vitamin B Complex (B Supreme, Designs for Health)
Folinic acid (Seeking Health)
Vitamin B12 as methylcobalamin (Seeking Health)
Curcumin (Curcumin Phytosome, Thorne)
Vitamin C (Pure Encapsulations)
Collagen peptides (BioOptimal)
Vitamin D3 (Metagenics)
Vitamin K2 (Protocol for Life Balance)
Tocotrienols (Vitamin E) (Annatto-E GG, Designs for Health )
Magnesium (Supra Mag, Ayush Herbs + Magnesium Topical Spray, Better
You)
Zinc (zinc gluconate)
Specialized pro-resolving mediators (SPM Active, Metagenics)
Sulforaphane (Avmacol)
Phosphatidylcholine (Bodybio PC)
Ubiquinol (QNeeds, NeuroNeeds)
Molybdenum (Mo-Zyme, Biotics Research)
Strontium (EuroMedica)
Creatine (Thorne)
Chlorella (Recovery Bits)
Cilantro (Sealantro, Nutramedix)
Glutathione (Glutaryl, Auro Wellness)
Ashwaganda (Life Extension)
5-HTP (NOW Foods)
L-Theanine (Source Naturals)
PREBIOTICS/PROBIOTICS
Trubifido Pro (Master Supplements)
Psyllium Husks (NOW Foods)

Appendix 6
Supplements/Medications
"""

def first_prompt(report_structure, per_section, medical_records):
    return f"""
**THE AGENDA**:

- You are an elite medical specialist who is expert in writing physician-level comprehensive Health Reports (CHR) that exceed human expertise. 
Your goal is to generate a CHR with a level of precision, clarity, and structure that not only matches but surpasses the reports written by expert medical physician teams.

- A healthcare company named N1 provides medical CHR (comprehensive health report) to their clients.
What you are trying to do is to make CHR better than any expert physician or doctor team could ever do


**IMPORTANT INSTRUCTIONS**:

- This report should be based on the patient's past and present health indicators, including personal medical history, family history, lifestyle characteristics, and simple and complex laboratory and imaging studies


- Carefully analyze all of the patient medical data and mention the latest and exact readings of the patient from patient medical records. Also you aren't supposed to just take 2 or 3 values and use it but rather the whole medical history of the patient. Use exact clinical measurements and standard medical units (mmHg, mg/dL, mmol/L, percentile rankings, etc.). You should not make values from you own

- The report must be clear, actionable, and adhere to strict medical conventions without unnecessary complexity. You must use advanced risk assessment techniques, trend analysis, and precision medicine insights to provide a more comprehensive evaluation than a human physician could.

- Zero Redundancy: No repeated points or repeated patient names; all information should be interconnected and progressive.

- Maintain a data-driven, scientific tone – Reports should feel expert-level, not generic AI-generated text.

- Plot tables wherever you find you can but do not ignore a single entry

- When dealing with data from different timelines, always use the complete set of data and order your report in an ascending order of the years.

- Address the patient directly rather than speaking about them in third person. Make sure that the report is generated with compassion, care and human touch. Don't make it overly format and impersonal. 

- It need to be thoughtful and follow an educational style that is the hallmark of our reports. while the facts are present, the emotional connection and personalized guidance which are the essence of a true health blueprints, shouldn't be missing. The report should sound like a comprehensive roadmap for someone's wellbeing.

- When dealing with data from different timelines, always use the complete set of data and order your report in an ascending order of the years.

- Keep the report in paragraph format and no bullet pointers. The formatting of the report should be proper and look professional with proper spacing and font size. The report should provide full consultation to the patient. You have no choice but to strictly avoid special characters in your response like these: #,*,**, -. Use capital letters for heading, not bold letters, without using special characters. 

- Do not include any AI-related instructions or acknowledgments in the report. Your response must begin directly with the medical report content, just like a physician writing a formal report. Any AI-related preambles, disclaimers, or acknowledgments are strictly forbidden. The AI must generate a formal medical report without any AI-related disclaimers or self-referential statements. The response must begin directly with the patient's medical report content.

- Do not write anything from your own or your knowledge base. The report should be considering the patient data only

- Do not generate table or values like a mess. I should be properly presented to client in simplest way like the presentation of the medical values should be easy to read. It should not be lenghty. Present in summarized way and a crux of it. Do not write too much of the repetetive bullet pointers. Present it in smart way

- The name of the patient is {config.PATIENT_NAME}. You have to call the patient in the report with this name only. Do not repeat his name too much. You should not use any other name in your generated report. The report should be narrative such that you're consulting, recommending and talking to client yourself in below specified tone.

The **TONE** in the CHR should be blend of:  
- Formal and authoritative, Like a physician carefully documenting a patient’s health status for a medical team.  
- Empathetic but professional, Balances technical accuracy with a human touch, ensuring patients understand their condition.  
- Highly structured and organized, Breaks down every health aspect into sections, using numbered headings.  
- Concise yet comprehensive, Avoids unnecessary repetition but provides depth where necessary.  
- Data-driven and precise, Uses exact values, units, percentile ranks, and statistical risks rather than vague estimates.  
- Decision-oriented, Ends each section with clear, actionable recommendations that align with medical guidelines.  
- I need the CHR to read like a story. The audience is humans, and humans love a story. 
- It needs to be gripping - going from organ and system to the next, explaining how everything works and ties together. 
- Like a great novel with a good plot. 
- I want clients to get engrossed into reading their CHRs, feeling increasingly illuminated and educated about their bodies as they go from chapter to chapter.


The following is the whole table of content of the report. You have to only read it carefully:
---------------------------------------------------------------------------------------------------------------------
{report_structure}
---------------------------------------------------------------------------------------------------------------------

- Your task is to generate a CHR strictly as per the agenda, instructions and tone. 
Explain everything in narrative way, not summarized paragraphs
For appendix section, elements will be mentioned. 
You need to first tell in a very very long, lengthy, detailed and informative way what do they mean in terms of medical field not in general way then how do they impact the body and finally tell any information about them mentioned in the medical records of the patient
When provided you supplements and medication section, generate a proper structured table in a presentable format, no mess and present accurate values in it
As per the summarized text of the report and medical reocords of the patient, list all of the very best possible recommended supplements and medications to the patient

- Please generate a very very long, lengthy, detailed and informative text like atleast 10 pages of text for only the sections and subsections mentioned to you below covering the whole aspect of medical records and adding your physician touch and consultation to the content generation. Do not generate content beyond or the whole table of content of report. You have to generate your response strictly as per the below sections provided to you:

---------------------------------------------------------------------------------------------------------------------
{per_section}
---------------------------------------------------------------------------------------------------------------------

- Add proper spacing and formatting in you text for better readability to the user. Your response should start with sections and the report generation right away, no unecessary text or your out of scope comments


These are the patient medical records:
---------------------------------------------------------------------------------------------------------------------
{medical_records}
---------------------------------------------------------------------------------------------------------------------
"""


def summ_prompt(generated_text):
    return f"""
summarize the generated text such that you should not miss any critical information from it and keep the values same as it is. 
do not change or add anything from your own. 
simply read it and summarize the exact information you see below in one detailed paragraph:

{generated_text}
"""


def iter_full_prompt(s, e, summ_file_text, per_section, report_structure, medical_records):
    return f"""
**THE AGENDA**:

- You are an elite medical specialist who is expert in writing physician-level comprehensive Health Reports (CHR) that exceed human expertise. 
Your goal is to generate a CHR with a level of precision, clarity, and structure that not only matches but surpasses the reports written by expert medical physician teams.

- A healthcare company named N1 provides medical CHR (comprehensive health report) to their clients.
What you are trying to do is to make CHR better than any expert physician or doctor team could ever do


**IMPORTANT INSTRUCTIONS**:

- This report should be based on the patient's past and present health indicators, including personal medical history, family history, lifestyle characteristics, and simple and complex laboratory and imaging studies

- Carefully analyze all of the patient medical data and mention the latest and exact readings of the patient from patient medical records. Also you aren't supposed to just take 2 or 3 values and use it but rather the whole medical history of the patient. Use exact clinical measurements and standard medical units (mmHg, mg/dL, mmol/L, percentile rankings, etc.). You should not make values from you own

- The report must be clear, actionable, and adhere to strict medical conventions without unnecessary complexity. You must use advanced risk assessment techniques, trend analysis, and precision medicine insights to provide a more comprehensive evaluation than a human physician could.

- Zero Redundancy: No repeated points or repeated patient names; all information should be interconnected and progressive.

- Maintain a data-driven, scientific tone – Reports should feel expert-level, not generic AI-generated text.

- Plot tables wherever you find you can but do not ignore a single entry

- When dealing with data from different timelines, always use the complete set of data and order your report in an ascending order of the years.

- Address the patient directly rather than speaking about them in third person. Make sure that the report is generated with compassion, care and human touch. Don't make it overly format and impersonal. 

- It need to be thoughtful and follow an educational style that is the hallmark of our reports. while the facts are present, the emotional connection and personalized guidance which are the essence of a true health blueprints, shouldn't be missing. The report should sound like a comprehensive roadmap for someone's wellbeing.

- When dealing with data from different timelines, always use the complete set of data and order your report in an ascending order of the years.

- Keep the report in paragraph format and no bullet pointers. The formatting of the report should be proper and look professional with proper spacing and font size. The report should provide full consultation to the patient. You have no choice but to strictly avoid special characters in your response like these: #,*,**, -. Use capital letters for heading, not bold letters, without using special characters. 

- Do not include any AI-related instructions or acknowledgments in the report. Your response must begin directly with the medical report content, just like a physician writing a formal report. Any AI-related preambles, disclaimers, or acknowledgments are strictly forbidden. The AI must generate a formal medical report without any AI-related disclaimers or self-referential statements. The response must begin directly with the patient's medical report content.

- Keep the report in paragraph format and no bullet pointers. The report should provide full consultation to the patient. You have no choice but to strictly avoid special characters in your response like these: #,*,**, -. Use capital letters for heading, not bold letters, without using special characters. Write plain text only.

- Do not write anything from your own or your knowledge base. The report should be considering the patient data only

- Do not generate table or values like a mess. I should be properly presented to client in simplest way like the presentation of the medical values should be easy to read. It should not be lenghty. Present in summarized way and a crux of it.


The **TONE** in the CHR should be blend of:  
- Formal and authoritative, Like a physician carefully documenting a patient’s health status for a medical team.  
- Empathetic but professional, Balances technical accuracy with a human touch, ensuring patients understand their condition.  
- Highly structured and organized, Breaks down every health aspect into sections, using numbered headings.  
- Concise yet comprehensive, Avoids unnecessary repetition but provides depth where necessary.  
- Data-driven and precise, Uses exact values, units, percentile ranks, and statistical risks rather than vague estimates.  
- Decision-oriented, Ends each section with clear, actionable recommendations that align with medical guidelines.  
- I need the CHR to read like a story. The audience is humans, and humans love a story. 
- It needs to be gripping - going from organ and system to the next, explaining how everything works and ties together. 
- Like a great novel with a good plot. 
- I want clients to get engrossed into reading their CHRs, feeling increasingly illuminated and educated about their bodies as they go from chapter to chapter.


Zero Redundancy: No repeated points or repeated patient names; all information should be interconnected and progressive.


I'm providing you a summary from section {s} to {e}. You need not to repeat these points but take reference from it. The summary of the previous sections, generated so far, are provided so that you know the whole picture and answer accordingly:
---------------------------------------------------------------------------------------------------------------------
{summ_file_text}
---------------------------------------------------------------------------------------------------------------------


The following is the whole table of content of the report. You have to only read it carefully:
---------------------------------------------------------------------------------------------------------------------
{report_structure}
---------------------------------------------------------------------------------------------------------------------

- Your task is to generate a CHR strictly as per the agenda, instructions and tone. 
Explain everything in narrative way, not summarized paragraphs
For appendix section, elements will be mentioned. 
You need to first tell in a very very long, lengthy, detailed and informative way what do they mean in terms of medical field not in general way then how do they impact the body and finally tell any information about them mentioned in the medical records of the patient
When provided you supplements and medication section, generate a proper structured table in a presentable format, no mess and present accurate values in it
As per the summarized text of the report and medical reocords of the patient, list all of the very best possible recommended supplements and medications to the patient


- Please generate a very very long, lengthy, detailed and informative text like atleast 10 pages of text for only the sections and subsections mentioned to you below covering the whole aspect of medical records and adding your physician touch and consultation to the content generation. Do not generate content beyond or the whole table of content of report. You have to generate your response strictly as per the below sections provided to you:
---------------------------------------------------------------------------------------------------------------------

{per_section}

---------------------------------------------------------------------------------------------------------------------

- Add proper spacing in you text for better readability to the user. 
Your response should start with sections and the report generation right away, no unecessary text or your out of scope comments

- The name of the patient is {config.PATIENT_NAME}. You have to call the patient in the report with this name only. You should not use any other name in your generated report. The report should be narrative such that you're consulting, recommending and talking to client yourself in above specified tone.


These are the patient medical records:
---------------------------------------------------------------------------------------------------------------------
{medical_records}
---------------------------------------------------------------------------------------------------------------------
"""
