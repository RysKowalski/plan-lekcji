
// getLessons.js
const { Keypair, VulcanHebeCe, VulcanJwtRegister } = require("hebece")

const fs = require('fs');

const APIAP = fs.readFileSync('token.txt', 'utf8')
console.log(APIAP)
// 1) paste the /api/ap JSON string you captured
// const APIAP = `{
//   "Tokens": [
//     "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSmVyenkgVG9tYXNpayAoMDA0OTc5KSIsInVpZCI6IjY2MDBlNzgzLWQ2MGYtNGFjMi04ZWRmLTg3M2YwODA4MmYwNSIsInRlbmFudCI6InBvd2lhdHpnaWVyc2tpIiwidW5pdHVpZCI6IjMzZmI1NzVlLWNiMmEtNDAxMy05Mjc5LTg4NTE3ZTAyY2JmYiIsInVyaSI6Imh0dHBzOi8vdWN6ZW4uZWR1dnVsY2FuLnBsL3Bvd2lhdHpnaWVyc2tpL3N0YXJ0P3Byb2ZpbD02NjAwZTc4My1kNjBmLTRhYzItOGVkZi04NzNmMDgwODJmMDUiLCJzZXJ2aWNlIjoiVHJ1ZSIsImNhcHMiOiJbXCJFRFVWVUxDQU5fUFJFTUlVTVwiXSIsIm5iZiI6MTc2MzU1MjQ5OCwiZXhwIjoxNzYzNTU2MDk4LCJpYXQiOjE3NjM1NTI0OTh9.EwqfQ-89lMKKprNvjpool2kqXz5oZVbJSg34LSzy0wVUwXDA5rEzXw0oIMzTeU_Q0NgilOyV04-He55nDUIfo2Ta5IK5dF2I7J00Cjj5BEgDLGTOYXaEx-dkkTzGiKojnlXQD4_xi0_A4HhLZmy11H-O6lIgqt_r37FHkrms9INDiHw_QpKn4eStKxmpgOj7nQ3hWtydQMxH7qvRHldxckwLWfuDwzcI1jUgEeaVFFyfRCTOdyHKOc34cpACSzWIMF6W-5hFqJl8mnvwpkYlJPdPTlZvZ-Lm8gD4Sy2kbfvRvvhQVkhQCtxck8NAu_5okOq26NC3nNEvq5TjWSC9zw"
//   ],
//   "Alias": "ryskowalski0@gmail.com",
//   "Email": "ryskowalski0@gmail.com",
//   "GivenName": "Jerzy",
//   "Surname": "Tomasik",
//   "IsConsentAccepted": true,
//   "CanAcceptConsent": true,
//   "AccessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiNDdkMTk5MDQtNDVlMC00YmJjLWFhNmUtMzQ1YTdhYzhkZGJjIiwiZ3VpZCI6Ijk5YWM3MzZjLTIyZjctNGExNi1iYWU2LTljNWJkNTJlYTE0NCIsImh0dHA6Ly9zY2hlbWFzLnZ1bGNhbi5lZHUucGwvd3MvaWRlbnRpdHkvY2xhaW1zL3Byb21ldGV1c3ovYWxpYXMiOiJyeXNrb3dhbHNraTBAZ21haWwuY29tIiwiaHR0cDovL3NjaGVtYXMudnVsY2FuLmVkdS5wbC93cy9pZGVudGl0eS9jbGFpbXMvcHJvbWV0ZXVzei9kZXZpY2VJbmZvU2lnbmF0dXJlIjoiMWExZWMxM2QtNTU1OC00YmY5LWI2NGEtZmFlZmRmZGFhZWQ2IiwibmJmIjoxNzYzNTUyNDk4LCJleHAiOjE3OTUwODg0OTgsImlhdCI6MTc2MzU1MjQ5OH0.JrbEXvmv0ij31HeBP6NYBQOstoyJo6w4Ryo75LdLnfZQJxcvevwNEcKRlcfDFlSwLF-Z7DFy2mZPhgLBVq4HRsY7if5hgNZ8gjr7RC3Hpj1knwVGFGg740J-9swKaM3RbqB0QVYb9bAFtcoYHolC6beWBN_gLl7_vMn4iz69iaUgBaPQKb4JjgvVxjsYVVxnmYDDsk5LQbjJixVHvYSxm_BY5fZf4xwdMlKQcwQ4O9yiZTU2i8L2PYikwRe2Cx2rkPwzzNNfVoW2Kwcmoc-Wf8PseTQq0Orgt8fR02olzNqwnjEYbvUea9m9MPiRLb484Jm_blovfpATc1-gNJcFkg",
//   "Capabilities": [
//     "EMAIL_CONFIRMATION": true
//   ],
//   "Success": true,
//   "ErrorMessage": ""
// }`;

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
