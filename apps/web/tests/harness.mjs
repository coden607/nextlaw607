import assert from "assert/strict";

const cases = [];
export { assert };
export function test(name, fn) { cases.push({ name, fn }); }
export async function run() {
  let failed = 0;
  for (const item of cases) {
    try {
      await item.fn();
      console.log(`ok - ${item.name}`);
    } catch (error) {
      failed += 1;
      console.error(`not ok - ${item.name}`);
      console.error(error && error.stack ? error.stack : error);
    }
  }
  console.log(`tests ${cases.length}; passed ${cases.length - failed}; failed ${failed}`);
  if (failed) process.exitCode = 1;
}
