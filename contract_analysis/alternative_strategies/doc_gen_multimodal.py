from docx import Document
from docx.shared import Inches, Pt

# Initialize Document
doc = Document()

PAGE_1_TEXT="""
CONTRACTOR NON-DISCLOSURE AGREEMENT

This contract serves as an agreement in accordance with the below mentioned obligations during
and after the time I worked with or for Apple, Inc. (“AAPL”) while employed by [Vendor Name].

In consideration of the opportunity to perform services during my deployment at Apple, Inc.
(“AAPL”) and intending to be legally bound hereby, I agree as follows:

1. Interpretation. The following definitions apply for purposes of this Agreement:

    a. “Apple, Inc.” means AAPL, together with any and all of its direct and indirect subsidiaries,
       entities and affiliates.

    b. “Confidential Information” means any and all AAPL information of a special and unique
       nature and value to AAPL and/or its clients (“Confidential Information”). Confidential Information
       includes, by way of illustration and not limitation, all information (whether or not patentable and
       whether or not copyrightable) owned, possessed or used by AAPL which is denoted confidential
       or is understood to be of confidential their respective nature by AAPL or recipient, or which under the
       circumstances surrounding the disclosure, development, or treatment by AAPL, or recipient, reasonably
       ought to be treated as confidential, including without limitation any of AAPL’s business plans, 
       product, invention, formula, vendor information, customer information, trade secret, process,
       research, report, technical data, know-how; computer programs, software, code, technologies,
       marketing or business plan, forecast, unpublished financials or other sensitive or proprietary 
       employee list that is communicated to, learned of, developed or otherwise acquired by me during
       the course of my service to AAPL. I further acknowledge that any information and materials
       received by AAPL from third parties in confidence shall be included in the definition of Confidential
       Information.

2. Confidential Information. I recognize that I am employed by [Vendor Name]. Since
   I will be performing services for AAPL, I agree that my relationship with AAPL is a relationship of
   high trust and confidence. As a result of this relationship, I may have access to AAPL Confidential 
   Information, along with access to proprietary information technology systems and tools of AAPL
   used to store and access Confidential Information, and passwords, keys, log-ins, files and other
   tools for accessing and using these systems and such Confidential Information (collectively, “Proprietary
   Information and Systems”).

I will preserve the confidentiality and secrecy of any Proprietary Information and Systems, will
not at any time, either during my assignment with AAPL or thereafter, disclose or provide any
Proprietary Information and Systems to any person or entity other than to persons who are properly
"""
PAGE_2_TEXT="""
authorized by AAPL or as authorized by the services agreement between AAPL and [Vendor Name].
I will not use for my own benefit or for the benefit of any other entity or person, any Proprietary
Information and System. Except as explicitly authorized in advance for the proper performance of 
my duties for AAPL, I will not copy or transmit any Proprietary Information and Systems or remove
them from AAPL’s premises by any media containing Proprietary Information and Systems.

My undertakings and obligations under this section will not apply, however, to any Confidential
Information which (i) becomes publicly known through lawful means; (ii) was rightfully in
my possession or part of my general knowledge prior to receipt from or on behalf of AAPL; (iii)
is disclosed to me without confidential or proprietary restriction by a third party unaffiliated with
AAPL who rightfully possesses the information (without obligation to maintain confidentiality); or
(iv) is required by law to be disclosed. In the case of (iv), I will promptly notify AAPL and cooperate
with AAPL, as permissible under the law, in resisting disclosure.

Upon termination or expiration of my assignment with AAPL, or at any other time upon AAPL’s
request, I will promptly return to AAPL all Proprietary Information and Systems in my possession
or under my control, including all notebooks, drawings, documents, records, reports, keys, key cards,
passwords, log-ins, files and other materials in my possession or under my control, in electronic form
and otherwise, whether prepared by me or others. I will also delete and destroy any copies of such
material that may remain in my possession, including digital copies that may exist in information
technology controlled by me. All Proprietary Information and Systems are and will remain the sole
property of AAPL.

3. Ownership.

3.1 Materials Provided by AAPL. All Proprietary Information and Systems that is/are pro-
vided to me by AAPL, or that I gain access to through AAPL, is/are and shall remain the sole and
exclusive property of AAPL.
"""
PAGE_3_TEXT="""
3.2 Materials Developed or Delivered by Me. Except as otherwise provided in the services
agreement between AAPL and [Vendor Name], I covenant and agree that all right, title and interest
in any findings, reports, inventions, writings, disclosures, discoveries, original works of authorship, 
or developments whether invented, made or conceived (whether or not patentable and whether or 
not copyrightable) by me solely or jointly with others and whether during normal business hours 
or otherwise in the course of or arising out my service relationship with AAPL (collectively called 
“Work Product”) shall be and remain the sole and exclusive property of AAPL, are hereby assigned 
to AAPL, and shall be a work made for hire. I HEREBY EXPRESSLY AGREE NOT TO CLAIM ANY 
RIGHT TITLE OR INTEREST OR TO TAKE ANY POSITION ADVERSE RESPECTING AAPL’S OWNERSHIP OF 
ALL RIGHT TITLE AND INTEREST IN AND TO ANY WORK PRODUCT. I further agree that I will not 
waive in favor of AAPL any Moral Rights I may have. I also agree to assist AAPL in obtaining 
all right title or interest which may vest with me. I shall promptly and fully disclose all Work Product 
and to maintain adequate and current written records (in the form of notes, sketches, drawings, 
as may be specified by AAPL) to document the conception and/or first actual reduction to practice of 
any Work Product. Such written records shall be available and remain the sole property of AAPL 
at all times.

3.3 Perfection and Cooperation. I shall execute any instruments and to do all other acts as 
reasonably requested by AAPL (both during and after my engagement by AAPL) in order to vest 
more fully in AAPL all ownership rights in Work Product.

3.4 Prior Knowledge. Notwithstanding the foregoing, Works Made For Hire do not include 
my pre-existing, pre-owned tools, procedures, know-how or methodologies (“Prior Knowledge”). To 
the extent that any Works Made For Hire incorporate or depend on Prior Knowledge, I hereby grant 
to AAPL an irrevocable, perpetual, royalty free, fully paid up, non-transferable, non-sublicensable, 
wide, non-exclusive license to use, copy, modify and exploit in any other manner all Prior Knowledge 
incorporated in or necessary to the use of all Works Made For Hire.

3.5 Avoidance of Third Party Materials and Rights. Except as otherwise provided in the ser-
vices agreement between AAPL and [Vendor Name], I will not incorporate into or use in any work 
for AAPL, nor will I otherwise induce AAPL to reproduce, make, use or sell, any confidential infor-
mation, inventions, software, or other proprietary information or materials of any third party unless 
party, unless I have obtained advance written authorization from AAPL to do so. I understand that 
blies incorporating any third party materials or that are subject to the proprietary rights of any third 
party will also include copies of any releases, consents, license agreements or other permissions 
for use of such materials.

4. Access and Security. I will abide by all safety and security instructions provided to me by 
AAPL, including instructions relating to access to and use of Proprietary Information and Systems. I
"""
PAGE_4_TEXT="""
will not disable, circumvent, or otherwise work around any security device or system, or system fea-
conforming identification and authorized use or access. After the end of my assignment with AAPL, 
will not use or access, without authorization, any of the systems or facilities of AAPL, whether on 
space or business premises, computer system, hardware, software or documentation.

5. Authority and Goodwill. I recognize that I do not speak for AAPL and that I am not autho-
ized to bind AAPL to any contractual obligation, and I will not attempt to do so. I further agree that I 
will not at any time speak or act in any manner that is intended to, or does in fact, damage the repu-
will or the business of AAPL, or the business or personal reputations of its directors, officers, em-
ployees, clients or suppliers, and I will not engage in any of the other deceptive conduct or 
communications with respect to AAPL.

6. Compliance and Records. I will comply with all AAPL processes and procedures to ensure 
legal compliance and ethical conduct in my delivery of services and Works Made For Hire. This 
includes (without limitation) procedures and guidelines applicable to the development of softwa 
and other materials.

7. Miscellaneous. This Agreement will be effective as of the date of my execution below and 
will remain in effect for the entire term of my assignment with AAPL, and will survive thereafter as reasonably 
necessary to accomplish its purposes. For example, Section 2 of this Agreement (Confidential Infor-
mation) will survive for so long as Proprietary Information and Systems accessed by me continue 
to be maintained confidentially by AAPL, and Section 3 of this Agreement (Ownership) will survive 
perpetually.

The invalidity or unenforceability of any provision of this Agreement will not affect the validi 
or enforceability of any other provision of this Agreement. This Agreement sets forth the entire 
agreement of the parties regarding the subject matter hereof, and supersedes all other agreements, 
ments, written or oral, between AAPL and me relating to the subject matter of this Agreement. 
This Agreement may not be modified, superseded, or discharged in whole or in part, except by 
an agreement in writing signed by AAPL and me which expressly states in writing an intent to 
modify, supersede or discharge this Agreement.

This Agreement will inure to the benefit of AAPL and its successors and assigns. No delay or 
by AAPL in exercising any right under this Agreement shall operate as a waiver of that or any 
other right. A waiver or consent given by AAPL on any one occasion is effective only in that instance 
and will not be construed as a bar to or waiver of any right on any other occasion.

I represent that I have and will independently create and develop all of my Works Made For 
and other deliverables to AAPL, and that my delivery of such materials to AAPL and AAPL’s 
"""

PAGE_5_TEXT="""
of such materials in the intended manner will not breach or violate any contractual agreement, 
proprietary interest, or applicable law, order or regulation.

I understand that this Agreement does not create any obligation on AAPL to continue my 
engagement.

As the obligations under this Agreement are special, unique and extraordinary, my breach of the 
terms of Section 2 of this Agreement (Confidential Information) will be deemed material, and will 
be deemed to cause irreparable injury not properly compensable by damages in an action at law, 
and the rights and remedies of AAPL hereunder may therefore be enforced at law or in equity, by 
injunction or otherwise.


Signature ___________________________


Name ___________________________


Date ___________________________

"""


# Set page margins for all sections
for section in doc.sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.3)
    section.right_margin = Inches(0.3)

# Define font style
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(10)

# Add page content with placeholder variables
pages = [
    f"{PAGE_1_TEXT}",
    f"{PAGE_2_TEXT}",
    f"{PAGE_3_TEXT}",
    f"{PAGE_4_TEXT}",
    f"{PAGE_5_TEXT}",
]

# Add content to document, one page per section
for i, page_text in enumerate(pages):
    doc.add_paragraph(page_text)
    if i < len(pages) - 1:
        doc.add_page_break()

# Save file
output_path = "ACME_Data_Amendment_Template.docx"
doc.save(output_path)
output_path
