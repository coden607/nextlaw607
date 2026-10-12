import { test, assert } from "./harness.mjs";
import { DEFAULT_PRIVACY, rightsFor } from "../dist/domain.js";
import { sanitizeDiagnostic } from "../dist/privacy.js";

test("privacy is local-first and diagnostics off by default",()=>{assert.equal(DEFAULT_PRIVACY.localOnly,true);assert.equal(DEFAULT_PRIVACY.diagnostics,false)});
test("search rights pack preserves non-consent and safety",()=>{const card=rightsFor("search");assert.ok(card.actions.some(x=>x.includes("do not consent")));assert.ok(card.never.some(x=>x.toLowerCase().includes("destroy")))});
test("interrogation rights pack invokes silence and counsel",()=>{const text=rightsFor("interrogation").actions.join(" ").toLowerCase();assert.match(text,/remain silent/);assert.match(text,/lawyer/)});
test("diagnostic sanitizer drops case content and tokens",()=>{assert.deepEqual(sanitizeDiagnostic({event:"error",module:"live",case_text:"secret case",token:"abc",error_code:"TIMEOUT"}),{event:"error",module:"live",error_code:"TIMEOUT"})});
import { createMatter, matterSummary, setMatterStage, setNextAppearance, addMatterIssue } from "../dist/caseguardian.js";

function memoryStorage(){const m=new Map();return {getItem:k=>m.has(k)?m.get(k):null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k),clear:()=>m.clear(),key:i=>[...m.keys()][i]??null,get length(){return m.size}}}
test("case guardian creates local matter without invented court data",()=>{const storage=memoryStorage();const matter=createMatter("People v Me","NY",storage);assert.equal(matter.jurisdiction,"NY");assert.equal(matter.nextAppearance,undefined);assert.match(matterSummary(matter),/not entered/)});
import { requestLiveGuidance } from "../dist/api.js";
test("live api client posts typed encounter request",async()=>{let seen;const fake=async(url,init)=>{seen={url,init};return {ok:true,json:async()=>({say_now:[],safety:[],preserve_for_later:[],verified_authority:false,authority_note:""})}};await requestLiveGuidance("search","protect my rights",fake);assert.equal(seen.url,"/api/live");assert.match(seen.init.body,/search/)});
import { PROCEDURE_STAGES } from "../dist/domain.js";
test("case guardian exposes release grand jury and plea stages",()=>{assert.ok(PROCEDURE_STAGES.includes("release_bail_remand"));assert.ok(PROCEDURE_STAGES.includes("grand_jury"));assert.ok(PROCEDURE_STAGES.includes("plea"))});


test("case guardian updates stage appearance and issues without inventing values",()=>{
  const storage=memoryStorage();
  let matter=createMatter("People v Me","NY",storage);
  matter=setMatterStage(matter,"arraignment",storage);
  matter=setNextAppearance(matter,"2026-09-10T11:00",storage);
  matter=addMatterIssue(matter,"Search consent disputed",storage);
  assert.equal(matter.stage,"arraignment");
  assert.equal(matter.nextAppearance,"2026-09-10T11:00");
  assert.deepEqual(matter.issues,["Search consent disputed"]);
});

const { escapeHtml } = await import("../dist/html.js");
test("html escaping neutralizes stored markup before UI rendering",()=>{
  assert.equal(escapeHtml('<img src=x onerror="alert(1)">&'), '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;&amp;');
});

test("case next-actions client posts stage without inventing an appearance",async()=>{
  const { requestCaseNextActions } = await import("../dist/api.js");
  let seen;
  const fake=async(url,init)=>{seen={url,init};return {ok:true,json:async()=>({stage:"arraignment",next_actions:["Confirm counsel"],next_appearance:null,deadline_source_verified:false})}};
  const result=await requestCaseNextActions({matterId:"m1",jurisdiction:"NY",stage:"arraignment"},fake);
  assert.equal(seen.url,"/api/case/next-actions");
  assert.match(seen.init.body,/arraignment/);
  assert.equal(result.next_appearance,null);
  assert.equal(result.deadline_source_verified,false);
});

import { readFile } from "node:fs/promises";
test("service worker precaches every critical compiled module",async()=>{
  const sw=await readFile(new URL("../sw.js",import.meta.url),"utf8");
  for (const asset of ["/dist/main.js","/dist/domain.js","/dist/privacy.js","/dist/storage.js","/dist/api.js","/dist/caseguardian.js","/dist/html.js"]) assert.ok(sw.includes(asset),asset);
});

test("local data can be exported, cleared, and restored without cloud access",async()=>{
  const { exportLocalData, importLocalData, clearLocalData, writeCases, writePrivacy, readCases, readPrivacy } = await import("../dist/storage.js");
  const storage=memoryStorage();
  const matter=createMatter("People v Export","NY",storage);
  writePrivacy({diagnostics:true,cloudSync:false,cloudAI:false,localOnly:true},storage);
  const snapshot=exportLocalData(storage);
  assert.equal(snapshot.schemaVersion,1);
  assert.equal(snapshot.cases[0].id,matter.id);
  clearLocalData(storage);
  assert.deepEqual(readCases(storage),[]);
  assert.equal(readPrivacy(storage).diagnostics,false);
  importLocalData(snapshot,storage);
  assert.equal(readCases(storage)[0].title,"People v Export");
  assert.equal(readPrivacy(storage).diagnostics,true);
});

test("invalid local-data snapshot fails closed",async()=>{
  const { importLocalData } = await import("../dist/storage.js");
  assert.throws(()=>importLocalData({schemaVersion:99,cases:[],privacy:{}},memoryStorage()),/unsupported local data schema/i);
});

test("founder entitlement is lifetime, billing-free, and not normally revocable",async()=>{
  const { FOUNDER_ENTITLEMENT, hasPremiumAccess } = await import("../dist/entitlements.js");
  assert.equal(FOUNDER_ENTITLEMENT.source,"founder_lifetime_grant");
  assert.equal(FOUNDER_ENTITLEMENT.expiresAt,null);
  assert.equal(FOUNDER_ENTITLEMENT.revocable,false);
  assert.equal(FOUNDER_ENTITLEMENT.billingRequired,false);
  assert.equal(hasPremiumAccess(FOUNDER_ENTITLEMENT),true);
});
