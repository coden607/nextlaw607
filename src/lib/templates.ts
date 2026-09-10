import type { ContractTemplate } from "./types";

export const TEMPLATES: ContractTemplate[] = [
  {
    id: "ica",
    name: "Independent Contractor Agreement",
    practice: "employment",
    summary:
      "NY-governed services agreement with misclassification guardrails, IP assignment, and a BDO Seidman-compliant restrictive-covenant option.",
    requiredStatutes: ["gol-5-701", "gol-5-1401", "gol-15-301", "lab-190"],
    requiredCases: ["bdo-seidman", "hooper", "www-assoc", "wood-lucy"],
    skeleton: `INDEPENDENT CONTRACTOR AGREEMENT

This Independent Contractor Agreement (the "Agreement") is entered into as of {{effectiveDate}} (the "Effective Date"), by and between {{partyA}} ("Company") and {{partyB}} ("Contractor").

RECITALS
A. Company desires to engage Contractor to perform the services described herein, and Contractor represents that Contractor is an independently established business.
B. The parties intend that this engagement not create an employment relationship under the New York Labor Law, the NYCRR, or federal wage-and-hour law.

ARTICLE 1. ENGAGEMENT AND SERVICES
1.1 Services. Contractor shall perform: {{services}}.
1.2 Standard of Care. Contractor shall perform the Services in a professional manner consistent with the skill and care ordinarily exercised by similarly situated independent professionals in New York.
1.3 No Exclusivity. Unless Exhibit A states otherwise, this engagement is non-exclusive. An exclusive arrangement carries an implied obligation to use reasonable efforts. Wood v. Lucy, Lady Duff-Gordon, 222 N.Y. 88 (1917).

ARTICLE 2. INDEPENDENT CONTRACTOR STATUS
2.1 Status. Contractor is and shall remain an independent contractor. Contractor controls the manner and means of performance, may accept other engagements, furnishes Contractor's own tools, and is not eligible for employee benefits.
2.2 Taxes. Contractor shall be solely responsible for all taxes, including self-employment taxes. Company will issue Form 1099-NEC as required.
2.3 Recitals Are Not Controlling. The parties acknowledge that New York looks to the economic reality of the relationship, not labels. Labor Law § 190 et seq.

ARTICLE 3. FEES AND EXPENSES
3.1 Fees. {{fees}}
3.2 Invoices; Payment. Net 30 days from a proper invoice. Overdue amounts accrue interest at 1% per month or the maximum permitted by law, whichever is less.
3.3 No Wage Claim. Contractor waives any claim to wages, overtime, spread-of-hours, or paid sick leave arising from a reclassification, to the maximum extent permitted by law; provided that this waiver does not extend to claims that cannot be waived.

ARTICLE 4. INTELLECTUAL PROPERTY
4.1 Work Product. All work product created in the performance of the Services is a work made for hire to the extent permitted by law. To the extent not a work made for hire, Contractor hereby irrevocably assigns to Company all right, title and interest therein.
4.2 Moral Rights. Contractor waives any moral rights to the extent waivable.

ARTICLE 5. CONFIDENTIALITY
5.1 Contractor shall hold in confidence all non-public information of Company for a period of three (3) years after termination, or indefinitely as to trade secrets.

ARTICLE 6. RESTRICTIVE COVENANTS (OPTIONAL)
6.1 If Exhibit B is attached, any non-solicitation or non-compete shall be limited in time, geography and scope to the protection of legitimate interests as required by BDO Seidman v. Hirshberg, 93 N.Y.2d 382 (1999). Overbroad restraints shall be modified to the minimum extent necessary to be enforceable (partial enforcement).

ARTICLE 7. INDEMNITY AND LIMITATION
7.1 Indemnity. Contractor shall indemnify, defend and hold harmless Company from third-party claims arising out of Contractor's negligence, willful misconduct, or misclassification as an employee, including reasonably incurred attorneys' fees. A promise to indemnify for attorneys' fees must be unmistakably clear. Hooper Associates, Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989).
7.2 Limitation. Except for confidentiality, IP, and indemnity obligations, each party's aggregate liability shall not exceed the fees paid in the twelve (12) months preceding the claim. No consequential damages.

ARTICLE 8. TERM AND TERMINATION
8.1 Term. {{term}}
8.2 Termination. Either party may terminate for convenience on fourteen (14) days' written notice, or immediately for material breach uncured after ten (10) days' written notice.

ARTICLE 9. GOVERNING LAW, FORUM, AND INTERPRETATION
9.1 Governing Law. This Agreement shall be governed by the laws of the State of New York, without regard to conflict-of-law principles. Where the aggregate transaction is not less than $250,000, the parties elect General Obligations Law § 5-1401.
9.2 Forum. The state courts sitting in {{county}} County, New York, shall have exclusive jurisdiction. Each party consents to personal jurisdiction and waives forum non conveniens. Where the transaction is not less than $1,000,000, the parties elect General Obligations Law § 5-1402.
9.3 Interpretation. This writing is complete, clear and unambiguous and shall be enforced according to its terms. W.W.W. Associates, Inc. v. Giancontieri, 77 N.Y.2d 157 (1990); Greenfield v. Philles Records, Inc., 98 N.Y.2d 562 (2002). Headings are for convenience only.

ARTICLE 10. GENERAL
10.1 Entire Agreement; No Oral Modification. This Agreement, including Exhibits, constitutes the entire agreement and supersedes all prior negotiations. It may not be modified except by a writing signed by the party to be charged. General Obligations Law §§ 5-1103, 15-301. Course of performance shall not constitute a waiver. Rose v. Spa Realty Associates, 42 N.Y.2d 338 (1977).
10.2 Statute of Frauds. To the extent any promise is not to be performed within one year, this subscribed writing satisfies General Obligations Law § 5-701.
10.3 Severability; Counterparts; Notices; Assignment. Invalid provisions are severed. Counterparts (including electronic) are one instrument. Notices to the addresses below. Neither party may assign without consent, except to an affiliate or successor.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.

{{signatureBlock}}`,
  },
  {
    id: "nda",
    name: "Mutual NDA",
    practice: "contracts",
    summary: "Two-way confidentiality with NY governing law, residual-knowledge carve-out, and Hooper-clear fee language.",
    requiredStatutes: ["gol-5-701", "gol-5-1401", "gol-15-301"],
    requiredCases: ["www-assoc", "hooper"],
    skeleton: `MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into as of {{effectiveDate}}, by and between {{partyA}} and {{partyB}} (each a "Party").

1. Purpose. The Parties wish to explore {{purpose}} and may disclose Confidential Information for that purpose only.

2. Confidential Information. Non-public information disclosed by a Party, in any form, that is marked confidential or that a reasonable person would understand to be confidential given the nature of the information and the circumstances of disclosure.

3. Exclusions. Information that (a) is or becomes public other than by breach; (b) was rightfully known without duty of confidentiality; (c) is independently developed without use of the other Party's information; or (d) is rightfully received from a third party without duty.

4. Non-Use and Non-Disclosure. The receiving Party shall use Confidential Information solely for the Purpose, protect it with no less than reasonable care, and disclose it only to personnel and professional advisors with a need to know who are bound by written duties no less protective.

5. Compelled Disclosure. The receiving Party may disclose as required by law, regulation, or court order, after (to the extent legally permitted) giving prompt notice so the disclosing Party may seek a protective order.

6. Term. Duties survive for three (3) years after disclosure; trade secrets remain protected until they cease to be trade secrets.

7. No License; No Warranty. No IP license is granted. Information is provided "as is."

8. Residual Knowledge. Nothing restricts a Party's use of residual knowledge retained in the unaided memory of its personnel, provided no Confidential Information is itself disclosed or reproduced.

9. Governing Law and Forum. New York law governs. Exclusive venue in the state courts of {{county}} County, New York. GOL §§ 5-1401, 5-1402 as applicable.

10. Fees. The prevailing Party in an action to enforce this Agreement shall recover its reasonably incurred attorneys' fees. Hooper Associates, Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989).

11. Entire Agreement; Writing. Entire agreement as to confidentiality. Modifications only by signed writing. GOL §§ 5-1103, 15-301. Ambiguity is not created by extrinsic evidence. W.W.W. Associates, 77 N.Y.2d 157 (1990).

{{signatureBlock}}`,
  },
  {
    id: "parenting",
    name: "Parenting Stipulation and Order",
    practice: "family",
    summary:
      "So-ordered custody/parenting stipulation under DRL §§ 70/240 and FCA Art. 6, with CSSA recitals and Eschbach factors.",
    requiredStatutes: ["drl-70", "drl-240", "fca-651", "cplr-2104"],
    requiredCases: ["eschbach", "tropea", "friederwitzer", "holterman"],
    skeleton: `SUPREME COURT OF THE STATE OF NEW YORK
COUNTY OF {{county}}

{{partyA}},
                                    Plaintiff,
          -against-                              Index No. {{indexNo}}

{{partyB}},
                                    Defendant.

STIPULATION AND ORDER CONCERNING CUSTODY AND PARENTING TIME
(DRL §§ 70, 240; FCA Art. 6)

The parties, intending to be bound pursuant to CPLR 2104, stipulate as follows:

1. JURISDICTION AND STANDARD
1.1 This Court has jurisdiction over the child(ren) {{children}} under the UCCJEA (DRL Art. 5-A) and DRL §§ 70 and 240. To the extent concurrent Family Court jurisdiction exists, the parties consent to this Court retaining continuing exclusive jurisdiction. FCA § 651.
1.2 There is no prima facie right to custody in either parent. DRL §§ 70, 240. The parties agree the following allocation is in the best interests of the child(ren), considering the factors identified in Eschbach v. Eschbach, 56 N.Y.2d 167 (1982), including the child's needs, home environment, parental guidance, relative fitness, stability, and sibling relationships.

2. LEGAL CUSTODY
2.1 The parties shall share joint legal custody. Major decisions (education, elective medical, religion, extra-curriculars with a material cost) shall be made jointly after good-faith consultation.
2.2 Emergency medical decisions may be made by the parent then in physical care, with prompt notice to the other.

3. RESIDENTIAL CUSTODY AND PARENTING TIME
3.1 {{partyA}} shall be the residential parent for school-district and CSSA purposes, without prejudice to the other parent's relationship.
3.2 Parenting time: {{parentingSchedule}}
3.3 Holidays and vacations alternate as set forth in Exhibit A.
3.4 Relocation. Neither parent shall relocate the child(ren)'s principal residence outside {{county}} County or more than {{miles}} miles from the other parent without written consent or court order. Any relocation dispute shall be determined under Matter of Tropea v. Tropea, 87 N.Y.2d 727 (1996) (true best-interest inquiry; no rigid exceptional-circumstances threshold).

4. COMMUNICATION AND RIGHT OF FIRST REFUSAL
4.1 Each parent shall have reasonable electronic contact when the child is with the other parent.
4.2 If a parent cannot exercise a block of parenting time exceeding four (4) hours, the other parent shall have a right of first refusal.

5. CHILD SUPPORT (CSSA)
5.1 Child support is determined under DRL § 240(1-b) (Child Support Standards Act). Combined parental income, each parent's income, the applicable percentage, and any deviation are set forth in Exhibit B (CSSA worksheet).
5.2 If the parties deviate from the CSSA, they do so knowingly, and they represent that the deviation is in the child(ren)'s best interests for the reasons recited in Exhibit B, as required by DRL § 240(1-b)(h) and Holterman v. Holterman, 3 N.Y.3d 1 (2004).
5.3 Add-ons. Statutory add-ons (health insurance premiums, unreimbursed health, child care necessary for work/education) shall be pro-rated {{proRata}}.
5.4 The support order shall contain the parties' Social Security numbers as required by DRL § 240.

6. MODIFICATION
6.1 This Stipulation may be modified upon a showing of a change in circumstances such that modification is in the child's best interests. Friederwitzer v. Friederwitzer, 55 N.Y.2d 89 (1982). A prior agreement is weighty but not conclusive.

7. DISPUTE RESOLUTION
7.1 Before filing a modification or enforcement petition (emergencies and family-offense petitions excepted), the parties shall attend one session of mediation.

8. BINDING EFFECT
8.1 This Stipulation is binding when subscribed by the parties or counsel, or when so-ordered. CPLR 2104.
8.2 The parties request that the Court so-order this Stipulation and retain jurisdiction to enforce it.

IT IS SO STIPULATED.

{{signatureBlock}}

SO ORDERED:

_______________________________
J.S.C.                              Date: __________`,
  },
  {
    id: "settlement",
    name: "Civil Settlement and Release",
    practice: "civil",
    summary: "NY general release with CPLR 4547 no-admission, Hooper fee clause, and GOL consideration recitals.",
    requiredStatutes: ["cplr-4547", "cplr-2104", "gol-5-1105", "gol-15-301"],
    requiredCases: ["hooper", "www-assoc"],
    skeleton: `SETTLEMENT AGREEMENT AND GENERAL RELEASE

This Settlement Agreement and General Release (the "Agreement") is entered into as of {{effectiveDate}} by {{partyA}} ("Releasor") and {{partyB}} ("Releasee").

RECITALS
A. Disputes have arisen concerning {{dispute}} (the "Claims").
B. The parties wish to resolve the Claims without admission of liability. This Agreement is a compromise of disputed claims. CPLR 4547.

1. SETTLEMENT CONSIDERATION
1.1 Releasee shall pay Releasor {{fees}} (the "Payment") within ten (10) business days of a fully executed Agreement and any required W-9, by {{paymentMethod}}.
1.2 Past consideration, if any, is expressly recited and is intended to be given effect under General Obligations Law § 5-1105.

2. RELEASE
2.1 Upon clearance of the Payment, Releasor hereby releases and forever discharges Releasee and its officers, directors, employees, agents, successors and assigns from any and all claims, known or unknown, arising out of or relating to the Claims, from the beginning of the world to the date of this Agreement, except for obligations created by this Agreement.
2.2 This is a general release of the Claims. It is not a release of claims that cannot be waived as a matter of law (including unemployment insurance, workers' compensation, and claims arising after execution).

3. NO ADMISSION
3.1 Nothing in this Agreement is an admission of liability, wrongdoing, or the validity or invalidity of any claim. Compromise negotiations are inadmissible under CPLR 4547.

4. CONFIDENTIALITY AND NON-DISPARAGEMENT
4.1 The parties shall keep the terms confidential except as required by law, tax, professional advice, or enforcement. Non-disparagement is mutual and limited to statements of objective fact required by legal process.

5. STIPULATION OF DISCONTINUANCE
5.1 Within five (5) days of clearance of the Payment, counsel shall file a stipulation of discontinuance with prejudice pursuant to CPLR 3217 and 2104, in the form of Exhibit A.

6. GOVERNING LAW
6.1 New York law governs. Exclusive venue in {{county}} County, New York.
6.2 The prevailing party in an action to enforce this Agreement shall recover reasonably incurred attorneys' fees. Hooper Associates, Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989).
6.3 Entire agreement; signed writings only. GOL §§ 5-1103, 15-301. W.W.W. Associates, 77 N.Y.2d 157 (1990).

{{signatureBlock}}`,
  },
  {
    id: "lease-res",
    name: "Residential Lease (NY)",
    practice: "real-property",
    summary: "Rent-stabilization-aware residential lease that preserves RPL § 235-b and avoids unenforceable waivers.",
    requiredStatutes: ["rpl-235-b", "rpl-231", "gol-5-701"],
    requiredCases: ["vermont-teddy", "maxton"],
    skeleton: `RESIDENTIAL LEASE AGREEMENT
State of New York

Landlord: {{partyA}}
Tenant: {{partyB}}
Premises: {{premises}}
Term: {{term}} commencing {{effectiveDate}}
Rent: {{fees}} per month, due on the first day of each month.

1. DEMISE. Landlord leases the Premises to Tenant for residential use only.

2. HABITABILITY. Landlord covenants that the Premises are fit for human habitation and for the uses reasonably intended, and that occupants will not be subjected to conditions dangerous to life, health or safety. This warranty of habitability may not be waived. Real Property Law § 235-b. Any clause purporting to waive it is void.

3. REPAIRS. Landlord shall maintain the Premises in accordance with the Housing Maintenance Code and applicable multiple-dwelling law. Tenant shall give prompt written notice of conditions.

4. SECURITY DEPOSIT. Held in trust in a New York bank, with the required notice, in accordance with General Obligations Law §§ 7-103 to 7-108, as applicable.

5. ENTRY. Landlord may enter on reasonable notice (not less than 24 hours except emergency) to inspect, repair, or show.

6. ASSIGNMENT / SUBLET. Subject to RPL § 226-b (if applicable). Landlord's consent shall not be unreasonably withheld as required by statute.

7. RENT STABILIZATION. If the Premises are subject to the Emergency Tenant Protection Act, the Rent Stabilization Law, or successor regulation, those provisions control and are incorporated. This lease shall not waive any non-waivable statutory right.

8. DEFAULT. Notice and opportunity to cure as required by RPAPL and the lease. Holdover and nonpayment proceedings shall be brought in the Housing Part, Civil Court, {{county}} County, or other court of competent jurisdiction.

9. GOVERNING LAW. New York law. Statute of frauds: this subscribed writing satisfies GOL § 5-701 as a contract concerning an interest in real property.

10. ENTIRE AGREEMENT. Entire agreement; signed writings only.

{{signatureBlock}}`,
  },
  {
    id: "operating",
    name: "LLC Operating Agreement",
    practice: "contracts",
    summary: "NY LLC Law § 417 operating agreement with capital, governance, transfer restrictions, and NY forum.",
    requiredStatutes: ["llc-417", "gol-5-1401", "gol-15-301"],
    requiredCases: ["www-assoc", "redbridge"],
    skeleton: `LIMITED LIABILITY COMPANY OPERATING AGREEMENT
of {{partyA}} LLC
a New York limited liability company

This Operating Agreement is entered into pursuant to Limited Liability Company Law § 417 as of {{effectiveDate}} by the Members listed on Schedule A.

ARTICLE I. FORMATION
1.1 The Company was formed by filing Articles of Organization with the New York Department of State. The Company is a New York limited liability company.
1.2 Purpose: {{purpose}}.

ARTICLE II. CAPITAL AND UNITS
2.1 Initial capital contributions and Units are set forth on Schedule A.
2.2 Additional capital calls require Majority-in-Interest approval. Failure to fund is not a personal obligation unless a Member executed a separate written guarantee (GOL § 5-701).

ARTICLE III. GOVERNANCE
3.1 Management is {{management}}.
3.2 Major Decisions (sale of substantially all assets, merger, amendment of this Agreement, incurring debt above {{fees}}, admission of Members) require {{vote}} approval.

ARTICLE IV. ALLOCATIONS AND DISTRIBUTIONS
4.1 Tax items follow § 704(b) capital accounts.
4.2 Available cash is distributed in the following waterfall: (1) tax distributions; (2) return of unreturned capital; (3) pro rata to Units.

ARTICLE V. TRANSFERS
5.1 No Member may transfer Units except (a) to a permitted transferee, or (b) after a right of first refusal in favor of the Company and then the Members.
5.2 An unpermitted transferee is an assignee of economic rights only, not a Member, until admitted by {{vote}}.

ARTICLE VI. FIDUCIARY DUTIES
6.1 Managers owe the duties of care and loyalty to the extent not expressly and lawfully modified herein. The Members acknowledge New York's freedom-of-contract policy. 159 MP Corp. v. Redbridge Bedford, LLC, 33 N.Y.3d 353 (2019).

ARTICLE VII. DISSOLUTION
7.1 The Company dissolves upon the vote of {{vote}} or as required by LLC Law.

ARTICLE VIII. GOVERNING LAW
8.1 New York law, including LLC Law § 417. Exclusive venue: {{county}} County. Entire agreement; signed writings only. W.W.W. Associates, 77 N.Y.2d 157 (1990).

{{signatureBlock}}`,
  },
  {
    id: "plea-plan",
    name: "Criminal Defense Workup (CPL / PL)",
    practice: "criminal",
    summary: "Internal defense matrix — 30.30 clock, Art. 245 discovery, elements and mental states. Not a client-facing plea.",
    requiredStatutes: ["cpl-30-30", "cpl-245-20", "pl-10-00", "pl-15-05"],
    requiredCases: ["people-bay", "people-goetz"],
    skeleton: `CRIMINAL DEFENSE WORKUP — ATTORNEY WORK PRODUCT
People v. {{partyB}}
County: {{county}}    Docket/Index: {{indexNo}}

I. CHARGE GRID
List each count with Penal Law section, degree, class, and culpable mental state (PL §§ 10.00, 15.05). Do not allocute a mental state the client does not admit.

II. SPEEDY TRIAL (CPL 30.30)
Commencement date: {{effectiveDate}}
Readiness period: felony = 6 months; A misdemeanor = 90 days; B misdemeanor = 60 days; violation = 30 days.
Exclusions to track: CPL 30.30(4).
Certificate of compliance: People v. Bay, 41 N.Y.3d 200 (2023) — an invalid COC does not stop the clock. Demand due diligence on each 245.20 category.

III. DISCOVERY (CPL ART. 245)
Automatic discovery under CPL 245.20. Demand letter should enumerate 245.20(1) items. Protective order practice: CPL 245.70.
Brady/Giglio is statutory under 245.20(1)(k) as well as constitutional.

IV. SUPPRESSION / DISMISSAL
CPL 710 (Mapp/Dunaway/Huntley/Wade); CPL 210.20/170.30; facial insufficiency (CPL 100.40 / 200.50).

V. JUSTIFICATION / DEFENSES
If force is in issue, apply People v. Goetz, 68 N.Y.2d 96 (1986) (hybrid objective-subjective). Recite PL 35.15 elements.

VI. PLEA ARCHITECTURE
Any plea must (a) match the allocution to the mental state, (b) preserve 30.30 if bargained, (c) address SORA, Pimentel, and collateral consequences (Padilla).

{{signatureBlock}}`,
  },
];

export function templateById(id: string) {
  return TEMPLATES.find((t) => t.id === id);
}
