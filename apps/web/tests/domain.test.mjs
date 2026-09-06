import { test, assert } from "./harness.mjs";
import { DEFAULT_PRIVACY, rightsFor } from "../dist/domain.js";
import { sanitizeDiagnostic } from "../dist/privacy.js";

test("privacy is local-first and diagnostics off by default",()=>{assert.equal(DEFAULT_PRIVACY.localOnly,true);assert.equal(DEFAULT_PRIVACY.diagnostics,false)});
test("search rights pack preserves non-consent and safety",()=>{const card=rightsFor("search");assert.ok(card.actions.some(x=>x.includes("do not consent")));assert.ok(card.never.some(x=>x.toLowerCase().includes("destroy")))});
test("interrogation rights pack invokes silence and counsel",()=>{const text=rightsFor("interrogation").actions.join(" ").toLowerCase();assert.match(text,/remain silent/);assert.match(text,/lawyer/)});
test("diagnostic sanitizer drops case content and tokens",()=>{assert.deepEqual(sanitizeDiagnostic({event:"error",module:"live",case_text:"secret case",token:"abc",error_code:"TIMEOUT"}),{event:"error",module:"live",error_code:"TIMEOUT"})});
import { createMatter, matterSummary } from "../dist/caseguardian.js";

function memoryStorage(){const m=new Map();return {getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),clear:()=>m.clear(),key:i=>[...m.keys()][i]??null,get length(){return m.size}}}
test("case guardian creates local matter without invented court data",()=>{const storage=memoryStorage();const matter=createMatter("People v Me","NY",storage);assert.equal(matter.jurisdiction,"NY");assert.equal(matter.nextAppearance,undefined);assert.match(matterSummary(matter),/not entered/)});
import { requestLiveGuidance } from "../dist/api.js";
test("live api client posts typed encounter request",async()=>{let seen;const fake=async(url,init)=>{seen={url,init};return {ok:true,json:async()=>({say_now:[],safety:[],preserve_for_later:[],verified_authority:false,authority_note:""})}};await requestLiveGuidance("search","protect my rights",fake);assert.equal(seen.url,"/api/live");assert.match(seen.init.body,/search/)});
import { PROCEDURE_STAGES } from "../dist/domain.js";
test("case guardian exposes release grand jury and plea stages",()=>{assert.ok(PROCEDURE_STAGES.includes("release_bail_remand"));assert.ok(PROCEDURE_STAGES.includes("grand_jury"));assert.ok(PROCEDURE_STAGES.includes("plea"))});
