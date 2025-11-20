
// getLessons.js
const { Keypair, VulcanHebeCe, VulcanJwtRegister } = require("hebece")

const fs = require('fs');

const APIAP = fs.readFileSync('token.txt', 'utf8')
async function main() {
  // 2) generate keypair
  const kpManager = new Keypair();
  const keypair = await kpManager.init();
  console.log("Keypair fingerprint:", keypair.fingerprint);

  // 3) register JWT
  const jwtReg = new VulcanJwtRegister(keypair, APIAP, true);
  await jwtReg.init();
  console.log("JWT registered");

  // 4) connect to Hebe
  const heb = new VulcanHebeCe(keypair);
  await heb.connect();

  console.log("Students:");
  console.log(heb.students);

  // 5) select first student automatically
  await heb.selectStudent();

  console.log(
    "Selected:",
    heb.selectedStudent.FirstName,
    heb.selectedStudent.LastName
  );

  // 6) build date range
  const dateFrom = new Date();
  const dateTo = new Date();
  dateTo.setDate(dateFrom.getDate() + 7);

  // 7) fetch lessons
  const resp = await heb.getLessons(dateFrom, dateTo);

  console.log("Response status:", resp.Status);
  console.log("Number of lessons:", resp.Envelope.length);

  for (const ls of resp.Envelope) {
    const d = ls.Date.DateDisplay;
    const subj = ls.Subject.Name;
    const room = ls.Room ? ls.Room.Code : "--";
    const t = ls.TeacherPrimary.DisplayName;

    console.log(`${d} | ${subj} | ${t} | room: ${room}`);
  }
}

main().catch(err => {
  console.error(err);
});
