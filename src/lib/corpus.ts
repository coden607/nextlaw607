import type { CaseDoc, Citation, StatuteDoc } from "./types";

/**
 * Verified New York authority bank. Critic Agent will reject any citation
 * that is not in this bank or returned live from CourtListener / NY Senate.
 * Blackletter is a working paraphrase of operative text — always link the
 * official statute page before relying on it in a signed instrument.
 */
export const STATUTES: StatuteDoc[] = [
  {
    id: "drl-70",
    lawId: "DOM",
    section: "70",
    title: "Habeas corpus for child detained by parent",
    chapter: "Domestic Relations Law",
    blackletter:
      "Either parent may apply to the supreme court for a writ of habeas corpus to have such minor child brought before the court. The court shall determine solely what is for the best interest of the child, and what will best promote its welfare and happiness, and make award accordingly. There is no prima facie right to the custody of the child in either parent.",
    practiceNotes:
      "Standing is equal. Do not draft a custody stipulation that recites a gender presumption. Tie every access schedule to articulable best-interest factors (Eschbach).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/DOM/70",
    practice: ["family"],
  },
  {
    id: "drl-240",
    lawId: "DOM",
    section: "240",
    title: "Custody and child support; orders of protection",
    chapter: "Domestic Relations Law",
    blackletter:
      "In matrimonial actions and habeas/OSC custody proceedings, the court shall enter orders for custody and support as justice requires, having regard to the circumstances of the case and of the respective parties and to the best interests of the child. There shall be no prima facie right to the custody of the child in either parent. Child support is computed under the Child Support Standards Act. An order directing payment of child support shall contain the social security numbers of the named parties.",
    practiceNotes:
      "Every parenting stipulation must address legal custody, residential custody, a parenting time calendar, decision-making, CSSA worksheets or an opt-out with the recitals required by DRL 240(1-b)(h), and add-ons (health, childcare, education).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/DOM/240",
    practice: ["family"],
  },
  {
    id: "drl-240-d",
    lawId: "DOM",
    section: "240-d",
    title: "Support orders for certain adult dependents",
    chapter: "Domestic Relations Law",
    blackletter:
      "A person chargeable with support of a minor child is also chargeable with support of that individual until age 26 when the person is developmentally disabled as defined in Mental Hygiene Law § 1.03(22), resides with the person seeking support, and is principally dependent on that person for maintenance.",
    practiceNotes:
      "Do not treat age-21 emancipation as automatic if developmental disability and co-residence are in the record.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/DOM/240-D",
    practice: ["family"],
  },
  {
    id: "fca-651",
    lawId: "FCT",
    section: "651",
    title: "Jurisdiction over habeas corpus and custody/visitation",
    chapter: "Family Court Act Article 6",
    blackletter:
      "Family Court has jurisdiction to determine habeas corpus proceedings and, when referred from Supreme Court or originated in Family Court, custody and visitation of minors. When determining custody or visitation, Family Court shall apply the same best-interest standard as Supreme Court under DRL §§ 70 and 240.",
    practiceNotes:
      "Forum selection between Supreme (DRL) and Family (FCA Art. 6) is tactical. A so-ordered stipulation should recite which court retains continuing jurisdiction under FCA § 652 / DRL 237/240.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/FCT/651",
    practice: ["family"],
  },
  {
    id: "fca-664",
    lawId: "FCT",
    section: "664",
    title: "Visitation rights of grandparents",
    chapter: "Family Court Act Article 6",
    blackletter:
      "Family Court may make an order of visitation in favor of a grandparent of a child, in accordance with DRL § 72, when such visitation is in the best interests of the child.",
    practiceNotes:
      "Grandparent standing is statutory and fact-intensive (Troxel overlay; NY still applies DRL 72 / FCA 651).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/FCT/664",
    practice: ["family"],
  },
  {
    id: "gol-5-701",
    lawId: "GOB",
    section: "5-701",
    title: "Agreements required to be in writing (Statute of Frauds)",
    chapter: "General Obligations Law",
    blackletter:
      "Every agreement, promise or undertaking is void unless it or some note or memorandum thereof be in writing and subscribed by the party to be charged, if it is (a) a special promise to answer for the debt of another, (b) a contract to make a testamentary provision, (c) an agreement not to be performed within one year, (d) a contract for the sale of real property or an interest therein, among other enumerated categories.",
    practiceNotes:
      "Any retainer, non-compete longer than one year, real-estate deal, or guarantee must be a subscribed writing. Electronic signatures: ESRA (State Technology Law Art. 3) + federal E-SIGN.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/5-701",
    practice: ["contracts", "real-property"],
  },
  {
    id: "gol-5-1103",
    lawId: "GOB",
    section: "5-1103",
    title: "Written agreement to modify or discharge",
    chapter: "General Obligations Law",
    blackletter:
      "An agreement hereafter made to change or modify, or to discharge in whole or in part, any contract, obligation, or lease shall not be invalid because of the absence of consideration, provided that the agreement changing, modifying or discharging such contract, obligation or lease shall be in writing and signed by the party against whom it is sought to enforce the change, modification or discharge.",
    practiceNotes:
      "NY permits consideration-less written modifications. Always include a no-oral-modification clause AND require signed writings so GOL 15-301 is aligned.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/5-1103",
    practice: ["contracts"],
  },
  {
    id: "gol-5-1105",
    lawId: "GOB",
    section: "5-1105",
    title: "Written promise expressing past consideration",
    chapter: "General Obligations Law",
    blackletter:
      "A promise in writing and signed by the promisor shall not be denied effect as a valid contractual obligation on the ground that consideration for the promise is past or executed, if the consideration is expressed in the writing and is proved to have been given or performed and would be a valid consideration but for the time when it was given or performed.",
    practiceNotes:
      "Recite the past consideration in the instrument itself. A bare 'for value received' is weaker than a specific recital.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/5-1105",
    practice: ["contracts"],
  },
  {
    id: "gol-5-1401",
    lawId: "GOB",
    section: "5-1401",
    title: "Choice of New York law",
    chapter: "General Obligations Law",
    blackletter:
      "The parties to any contract, agreement or undertaking, contingent or otherwise, relating to any obligation arising out of a transaction covering in the aggregate not less than two hundred fifty thousand dollars, may agree that the law of this state shall govern their rights and duties in whole or in part, whether or not such contract bears a reasonable relation to this state.",
    practiceNotes:
      "Use this clause when the deal is ≥ $250,000. Below that threshold, include a reasonable-relation recital (place of performance, situs of assets, party domicile).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/5-1401",
    practice: ["contracts"],
  },
  {
    id: "gol-5-1402",
    lawId: "GOB",
    section: "5-1402",
    title: "Choice of New York forum",
    chapter: "General Obligations Law",
    blackletter:
      "Any person may maintain an action or proceeding against a foreign corporation, non-resident, or foreign state where the action arises out of a contract which contains a provision choosing New York law pursuant to § 5-1401 and which contains a provision whereby such person agrees to submit to the jurisdiction of the courts of this state, if the contract covers not less than one million dollars.",
    practiceNotes:
      "Pair 5-1401 (law) with 5-1402 (forum) plus a consent to personal jurisdiction and an agent-for-service clause. For smaller deals, use CPLR 501/327 analysis.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/5-1402",
    practice: ["contracts", "civil"],
  },
  {
    id: "gol-15-301",
    lawId: "GOB",
    section: "15-301",
    title: "No oral modification; written discharge",
    chapter: "General Obligations Law",
    blackletter:
      "A written agreement or other written instrument which contains a provision to the effect that it cannot be changed orally, cannot be changed by an executory agreement unless such executory agreement is in writing and signed by the party against whom enforcement of the change is sought.",
    practiceNotes:
      "Standard 'entire agreement / no oral modification' block. Watch for waiver by course of performance (Rose v Spa Realty).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/GOB/15-301",
    practice: ["contracts"],
  },
  {
    id: "cplr-3211",
    lawId: "CVP",
    section: "3211",
    title: "Motion to dismiss",
    chapter: "Civil Practice Law and Rules",
    blackletter:
      "A party may move to dismiss on enumerated grounds including documentary evidence (a)(1), lack of subject-matter jurisdiction (a)(2), lack of capacity (a)(3), another action pending (a)(4), failure to state a cause of action (a)(7), and statute of limitations (a)(5), among others. Grounds in (a)(2), (7) and (10) may be raised at any time; other enumerated grounds are waived if not raised in a responsive pleading or pre-answer motion.",
    practiceNotes:
      "When drafting contracts, include survival, notice-and-cure, and exclusive-remedy clauses that become 'documentary evidence' on a 3211(a)(1) motion.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/CVP/3211",
    practice: ["civil", "contracts"],
  },
  {
    id: "cplr-4547",
    lawId: "CVP",
    section: "4547",
    title: "Compromise offers and settlement negotiations",
    chapter: "Civil Practice Law and Rules",
    blackletter:
      "Evidence of (a) furnishing or offering to furnish, or (b) accepting or offering to accept, a valuable consideration in compromising or attempting to compromise a claim which is disputed as to either validity or amount, is inadmissible as proof of liability for, or invalidity of, the claim or its amount. Evidence of conduct or statements made in compromise negotiations is likewise inadmissible.",
    practiceNotes:
      "Mark every demand letter 'FOR SETTLEMENT PURPOSES ONLY — CPLR 4547'. Do not recite fault in a release's recitals if you intend to preserve no-admission.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/CVP/4547",
    practice: ["civil", "contracts"],
  },
  {
    id: "cplr-2104",
    lawId: "CVP",
    section: "2104",
    title: "Stipulations",
    chapter: "Civil Practice Law and Rules",
    blackletter:
      "An agreement between parties or their attorneys relating to any matter in an action, other than one made between counsel in open court, is not binding unless it is in a writing subscribed by the party or the attorney, or reduced to the form of an order and entered.",
    practiceNotes:
      "So-order every custody, settlement, and discovery stipulation. Open-court stipulations are binding if the record is clear (In re Dolgin Eldert).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/CVP/2104",
    practice: ["civil", "family"],
  },
  {
    id: "cpl-30-30",
    lawId: "CPL",
    section: "30.30",
    title: "Speedy trial; time limitations",
    chapter: "Criminal Procedure Law",
    blackletter:
      "A motion to dismiss must be granted where the People are not ready for trial within: six months of commencement of a criminal action charging a felony; 90 days for a misdemeanor punishable by more than three months; 60 days for a misdemeanor punishable by not more than three months; 30 days for a violation. Excludable periods are enumerated in subdivision 4.",
    practiceNotes:
      "Track off-calendar adjournments, consent, exceptional circumstances, and discovery readiness (People v. Bay; CPL Art. 245 interplay).",
    officialUrl: "https://www.nysenate.gov/legislation/laws/CPL/30.30",
    practice: ["criminal"],
  },
  {
    id: "cpl-245-20",
    lawId: "CPL",
    section: "245.20",
    title: "Automatic discovery",
    chapter: "Criminal Procedure Law Article 245",
    blackletter:
      "The prosecution shall disclose to the defendant, and permit the defendant to discover, inspect, copy, photograph and test, all items and information that relate to the subject matter of the case and are in the possession, custody or control of the prosecution, the police, or others under the prosecution's direction, including but not limited to police reports, statements, electronic recordings, expert disclosures, and favorable information (Brady/Giglio).",
    practiceNotes:
      "Demand letters should cite 245.20(1) categories by letter. Protective orders: CPL 245.70.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/CPL/245.20",
    practice: ["criminal"],
  },
  {
    id: "pl-10-00",
    lawId: "PEN",
    section: "10.00",
    title: "Definitions of offenses",
    chapter: "Penal Law",
    blackletter:
      "Defines crime, felony, misdemeanor, violation, physical injury, serious physical injury, deadly weapon, dangerous instrument, and other terms that control grading and elements throughout the Penal Law.",
    practiceNotes:
      "Every accusatory-instrument challenge starts with the statutory definition plus the mental state in PL 15.05.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/PEN/10.00",
    practice: ["criminal"],
  },
  {
    id: "pl-15-05",
    lawId: "PEN",
    section: "15.05",
    title: "Culpability; definitions of culpable mental states",
    chapter: "Penal Law",
    blackletter:
      "Intentionally, knowingly, recklessly, and criminal negligence are the four culpable mental states. When a statute is silent, PL 15.15 rules of construction apply.",
    practiceNotes:
      "Plea allocutions must match the mental state. Do not allocute 'I was careless' to an intent crime.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/PEN/15.05",
    practice: ["criminal"],
  },
  {
    id: "lab-190",
    lawId: "LAB",
    section: "190",
    title: "Definitions (wages, employee, employer)",
    chapter: "Labor Law Article 6",
    blackletter:
      "Defines wages, employee, and employer for wage-payment claims. Independent-contractor misclassification is tested against the economic-reality / control factors and industry-specific statutory tests (e.g., Construction Industry Fair Play Act).",
    practiceNotes:
      "Every independent-contractor agreement should include a control recital, but recitals do not control if the facts show employment. Include indemnities for wage claims with a knowing-misclassification kicker.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/LAB/190",
    practice: ["employment", "contracts"],
  },
  {
    id: "rpl-231",
    lawId: "RPP",
    section: "231",
    title: "Lease; liability of landlord and tenant for repairs / injuries",
    chapter: "Real Property Law",
    blackletter:
      "Addresses landlord and tenant duties in connection with premises conditions and, together with the warranty of habitability (RPL § 235-b), frames residential repair and injury exposure.",
    practiceNotes:
      "Residential leases cannot waive the warranty of habitability (RPL 235-b). Commercial leases may allocate repair by express covenant.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/RPP/231",
    practice: ["real-property"],
  },
  {
    id: "rpl-235-b",
    lawId: "RPP",
    section: "235-b",
    title: "Warranty of habitability",
    chapter: "Real Property Law",
    blackletter:
      "In every written or oral lease or rental agreement for residential premises, the landlord or lessor is deemed to covenant that the premises are fit for human habitation and for the uses reasonably intended by the parties, and that occupants will not be subjected to conditions dangerous to life, health or safety. The warranty cannot be waived.",
    practiceNotes:
      "Do not include a waiver. Rent-abatement and repair-and-deduct language should sit beside a notice procedure.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/RPP/235-B",
    practice: ["real-property"],
  },
  {
    id: "llc-417",
    lawId: "LLC",
    section: "417",
    title: "Operating agreement",
    chapter: "Limited Liability Company Law",
    blackletter:
      "The members of a limited liability company may enter into an operating agreement to regulate the affairs of the company and the conduct of its business, and to govern relations among the members, managers and company. The operating agreement may be entered into before, at the time of, or within ninety days after the filing of the articles of organization.",
    practiceNotes:
      "Cover capital accounts, waterfalls, fiduciary duties (waiver limits), transfer restrictions, dissolution, and dispute resolution. File articles with DOS.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/LLC/417",
    practice: ["contracts"],
  },
  {
    id: "ucc-2-201",
    lawId: "UCC",
    section: "2-201",
    title: "Formal requirements; statute of frauds (goods)",
    chapter: "Uniform Commercial Code",
    blackletter:
      "A contract for the sale of goods for the price of $500 or more is not enforceable unless there is some writing sufficient to indicate that a contract for sale has been made between the parties and signed by the party against whom enforcement is sought. Merchant confirmation exception, specially manufactured goods, admission, and payment/acceptance are statutory exceptions.",
    practiceNotes:
      "Use a signed quantity term. Between merchants, a confirmatory memo sent within a reasonable time can bind the recipient who does not object in writing within 10 days.",
    officialUrl: "https://www.nysenate.gov/legislation/laws/UCC/2-201",
    practice: ["contracts"],
  },
];

export const CASES: CaseDoc[] = [
  {
    id: "eschbach",
    name: "Eschbach v. Eschbach",
    bluebook: "Eschbach v. Eschbach, 56 N.Y.2d 167 (1982)",
    court: "N.Y. Court of Appeals",
    year: 1982,
    holding:
      "Best-interest custody determinations consider the child's needs, the home environment, parental guidance, financial status, each parent's relative fitness, and the effect of a change. Stability and the quality of the home are weighty; sibling unity is a factor. Appellate courts give great deference to the trial court's unique opportunity to observe the parties.",
    officialUrl: "https://www.courtlistener.com/?q=Eschbach+v.+Eschbach+56+NY2d+167",
    statutes: ["drl-70", "drl-240"],
    practice: ["family"],
  },
  {
    id: "tropea",
    name: "Matter of Tropea v. Tropea",
    bluebook: "Matter of Tropea v. Tropea, 87 N.Y.2d 727 (1996)",
    court: "N.Y. Court of Appeals",
    year: 1996,
    holding:
      "Relocation petitions are decided by a true best-interest inquiry. There is no formulaic 'exceptional circumstances' threshold. Courts weigh the reasons for the move, the effect on the child's relationship with the noncustodial parent, the quality of the relationships, the feasibility of preserving contact, and the child's needs.",
    officialUrl: "https://www.courtlistener.com/?q=Tropea+v+Tropea+87+NY2d+727",
    statutes: ["drl-70", "drl-240"],
    practice: ["family"],
  },
  {
    id: "friederwitzer",
    name: "Friederwitzer v. Friederwitzer",
    bluebook: "Friederwitzer v. Friederwitzer, 55 N.Y.2d 89 (1982)",
    court: "N.Y. Court of Appeals",
    year: 1982,
    holding:
      "A prior custody award, even one based on a stipulation, may be modified upon a showing of a change in circumstances such that modification is in the child's best interests. The existence of a prior agreement is a weighty but not conclusive factor.",
    officialUrl: "https://www.courtlistener.com/?q=Friederwitzer+v+Friederwitzer+55+NY2d+89",
    statutes: ["drl-70", "drl-240"],
    practice: ["family"],
  },
  {
    id: "bennett-jeffreys",
    name: "Matter of Bennett v. Jeffreys",
    bluebook: "Matter of Bennett v. Jeffreys, 40 N.Y.2d 543 (1976)",
    court: "N.Y. Court of Appeals",
    year: 1976,
    holding:
      "A parent has a superior right to custody of a child as against a nonparent, unless extraordinary circumstances (surrender, abandonment, unfitness, persistent neglect, or other extraordinary circumstances) exist. Only then does the court reach a best-interest analysis as between parent and nonparent.",
    officialUrl: "https://www.courtlistener.com/?q=Bennett+v+Jeffreys+40+NY2d+543",
    statutes: ["drl-70", "fca-651"],
    practice: ["family"],
  },
  {
    id: "holterman",
    name: "Holterman v. Holterman",
    bluebook: "Holterman v. Holterman, 3 N.Y.3d 1 (2004)",
    court: "N.Y. Court of Appeals",
    year: 2004,
    holding:
      "Interprets CSSA application, including how enhanced-earning-capacity awards interact with child support. CSSA is mandatory; deviations require the statutory recitals.",
    officialUrl: "https://www.courtlistener.com/?q=Holterman+v+Holterman+3+NY3d+1",
    statutes: ["drl-240"],
    practice: ["family"],
  },
  {
    id: "wood-lucy",
    name: "Wood v. Lucy, Lady Duff-Gordon",
    bluebook: "Wood v. Lucy, Lady Duff-Gordon, 222 N.Y. 88 (1917)",
    court: "N.Y. Court of Appeals",
    year: 1917,
    holding:
      "A promise may be implied to use reasonable efforts where that implication is necessary to give the transaction the business efficacy the parties intended. Exclusive-agency arrangements carry an implied obligation to use reasonable efforts.",
    officialUrl: "https://www.courtlistener.com/?q=Wood+v+Lucy+Lady+Duff-Gordon+222+NY+88",
    statutes: ["gol-5-701"],
    practice: ["contracts"],
  },
  {
    id: "www-assoc",
    name: "W.W.W. Associates, Inc. v. Giancontieri",
    bluebook: "W.W.W. Associates, Inc. v. Giancontieri, 77 N.Y.2d 157 (1990)",
    court: "N.Y. Court of Appeals",
    year: 1990,
    holding:
      "When a contract is complete, clear and unambiguous on its face, it must be enforced according to its terms. Extrinsic evidence is not admissible to create an ambiguity. This is the cornerstone of NY merger-clause drafting.",
    officialUrl: "https://www.courtlistener.com/?q=WWW+Associates+Giancontieri+77+NY2d+157",
    statutes: ["gol-15-301"],
    practice: ["contracts"],
  },
  {
    id: "greenfield",
    name: "Greenfield v. Philles Records, Inc.",
    bluebook: "Greenfield v. Philles Records, Inc., 98 N.Y.2d 562 (2002)",
    court: "N.Y. Court of Appeals",
    year: 2002,
    holding:
      "A written agreement that is complete, clear and unambiguous must be enforced according to the plain meaning of its terms. Courts may not add or excise terms under the guise of interpretation.",
    officialUrl: "https://www.courtlistener.com/?q=Greenfield+v+Philles+Records+98+NY2d+562",
    statutes: ["gol-15-301"],
    practice: ["contracts"],
  },
  {
    id: "vermont-teddy",
    name: "Vermont Teddy Bear Co. v. 538 Madison Realty Co.",
    bluebook: "Vermont Teddy Bear Co. v. 538 Madison Realty Co., 1 N.Y.3d 470 (2004)",
    court: "N.Y. Court of Appeals",
    year: 2004,
    holding:
      "Courts will not rewrite a clear lease allocation of repair and casualty risk. Parties to a commercial lease are free to allocate risk as they see fit; the court enforces the bargain.",
    officialUrl: "https://www.courtlistener.com/?q=Vermont+Teddy+Bear+538+Madison+1+NY3d+470",
    statutes: ["rpl-231"],
    practice: ["contracts", "real-property"],
  },
  {
    id: "redbridge",
    name: "159 MP Corp. v. Redbridge Bedford, LLC",
    bluebook: "159 MP Corp. v. Redbridge Bedford, LLC, 33 N.Y.3d 353 (2019)",
    court: "N.Y. Court of Appeals",
    year: 2019,
    holding:
      "Freedom of contract is a deeply rooted NY public policy. A commercial tenant's contractual waiver of the right to declare a Yellowstone-style declaratory judgment was enforceable. Sophisticated parties may bargain away even valuable litigation rights if the waiver is clear.",
    officialUrl: "https://www.courtlistener.com/?q=159+MP+Corp+Redbridge+Bedford+33+NY3d+353",
    statutes: ["gol-5-1401"],
    practice: ["contracts", "real-property"],
  },
  {
    id: "hooper",
    name: "Hooper Associates, Ltd. v. AGS Computers, Inc.",
    bluebook: "Hooper Associates, Ltd. v. AGS Computers, Inc., 74 N.Y.2d 487 (1989)",
    court: "N.Y. Court of Appeals",
    year: 1989,
    holding:
      "A promise to indemnify for attorneys' fees must be unmistakably clear. NY will not infer a fee-shifting indemnity from general language.",
    officialUrl: "https://www.courtlistener.com/?q=Hooper+Associates+AGS+Computers+74+NY2d+487",
    statutes: ["gol-5-1103"],
    practice: ["contracts", "civil"],
  },
  {
    id: "bdo-seidman",
    name: "BDO Seidman v. Hirshberg",
    bluebook: "BDO Seidman v. Hirshberg, 93 N.Y.2d 382 (1999)",
    court: "N.Y. Court of Appeals",
    year: 1999,
    holding:
      "A non-compete is enforceable only to the extent it is reasonable in time, geography and scope, necessary to protect a legitimate interest (trade secrets, confidential information, or goodwill with clients the employee independently serviced), not harmful to the public, and not unduly burdensome. Overbreadth is partially enforceable (blue-pencil in equity) rather than void in toto in the employee context under this doctrine.",
    officialUrl: "https://www.courtlistener.com/?q=BDO+Seidman+v+Hirshberg+93+NY2d+382",
    statutes: ["lab-190"],
    practice: ["employment", "contracts"],
  },
  {
    id: "maxton",
    name: "Maxton Builders, Inc. v. Lo Galbo",
    bluebook: "Maxton Builders, Inc. v. Lo Galbo, 68 N.Y.2d 373 (1986)",
    court: "N.Y. Court of Appeals",
    year: 1986,
    holding:
      "Down-payment forfeiture clauses in real-estate contracts are generally enforceable as liquidated damages where the deposit is 10% or less, absent unconscionability. Draft the liquidated-damages clause as the exclusive remedy if that is the bargain.",
    officialUrl: "https://www.courtlistener.com/?q=Maxton+Builders+Lo+Galbo+68+NY2d+373",
    statutes: ["gol-5-701"],
    practice: ["contracts", "real-property"],
  },
  {
    id: "rose-spa",
    name: "Rose v. Spa Realty Associates",
    bluebook: "Rose v. Spa Realty Associates, 42 N.Y.2d 338 (1977)",
    court: "N.Y. Court of Appeals",
    year: 1977,
    holding:
      "A no-oral-modification clause can be overcome by partial performance that is unequivocally referable to the alleged oral modification, or by estoppel. Drafting should require that any waiver be in a signed writing and that course of performance not constitute waiver.",
    officialUrl: "https://www.courtlistener.com/?q=Rose+v+Spa+Realty+Associates+42+NY2d+338",
    statutes: ["gol-15-301"],
    practice: ["contracts"],
  },
  {
    id: "people-goetz",
    name: "People v. Goetz",
    bluebook: "People v. Goetz, 68 N.Y.2d 96 (1986)",
    court: "N.Y. Court of Appeals",
    year: 1986,
    holding:
      "Justification (PL 35.15) uses a hybrid objective-subjective standard: the defendant must actually believe deadly force is necessary, and that belief must be reasonable in light of the circumstances as the defendant perceived them.",
    officialUrl: "https://www.courtlistener.com/?q=People+v+Goetz+68+NY2d+96",
    statutes: ["pl-15-05"],
    practice: ["criminal"],
  },
  {
    id: "people-bay",
    name: "People v. Bay",
    bluebook: "People v. Bay, 41 N.Y.3d 200 (2023)",
    court: "N.Y. Court of Appeals",
    year: 2023,
    holding:
      "The People's certificate of compliance under CPL Art. 245 must be filed in good faith after exercising due diligence. An invalid COC does not stop the 30.30 clock. Discovery readiness is now a speedy-trial fact.",
    officialUrl: "https://www.courtlistener.com/?q=People+v+Bay+41+NY3d+200",
    statutes: ["cpl-30-30", "cpl-245-20"],
    practice: ["criminal"],
  },
];

export function statuteById(id: string) {
  return STATUTES.find((s) => s.id === id);
}

export function caseById(id: string) {
  return CASES.find((c) => c.id === id);
}

export function searchCorpus(q: string): { statutes: StatuteDoc[]; cases: CaseDoc[] } {
  const n = q.trim().toLowerCase();
  if (!n) return { statutes: STATUTES, cases: CASES };
  const hit = (s: string) => s.toLowerCase().includes(n);
  return {
    statutes: STATUTES.filter(
      (s) =>
        hit(s.section) ||
        hit(s.title) ||
        hit(s.chapter) ||
        hit(s.blackletter) ||
        hit(s.lawId) ||
        hit(s.id),
    ),
    cases: CASES.filter(
      (c) =>
        hit(c.name) ||
        hit(c.bluebook) ||
        hit(c.holding) ||
        hit(c.court) ||
        c.statutes.some((id) => hit(id)),
    ),
  };
}

export function citationsForPractice(practice: string): Citation[] {
  const statutes = STATUTES.filter((s) => s.practice.includes(practice as never));
  const cases = CASES.filter((c) => c.practice.includes(practice as never));
  return [
    ...statutes.map(
      (s): Citation => ({
        id: s.id,
        kind: "statute",
        bluebook: `${s.chapter} § ${s.section}`,
        url: s.officialUrl,
        verified: true,
        source: "corpus",
        holding: s.blackletter,
      }),
    ),
    ...cases.map(
      (c): Citation => ({
        id: c.id,
        kind: "case",
        bluebook: c.bluebook,
        court: c.court,
        year: c.year,
        url: c.officialUrl,
        verified: true,
        source: "corpus",
        holding: c.holding,
      }),
    ),
  ];
}

export function corpusPromptBlock(): string {
  const statuteLines = STATUTES.map(
    (s) =>
      `- ${s.chapter} § ${s.section} (${s.id}): ${s.title}. ${s.blackletter} Source: ${s.officialUrl}`,
  ).join("\n");
  const caseLines = CASES.map(
    (c) => `- ${c.bluebook} — ${c.holding} Source: ${c.officialUrl}`,
  ).join("\n");
  return `VERIFIED NEW YORK AUTHORITY BANK (cite ONLY these plus any live CourtListener hits provided):\n\nSTATUTES:\n${statuteLines}\n\nCASES:\n${caseLines}`;
}
