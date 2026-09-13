// self.addEventListener("push", (event) => {
//   const data = event.data
//   ? (() => {
//       try {
//         return event.data.json();
//       } catch {
//         return { body: event.data.text() };
//       }
//     })()
//   : {};

//   event.waitUntil(
//     self.registration.showNotification(
//       data.title || "Notification",
//       {
//         body: data.body || "New notification",
//       }
//     )
//   );
// });

self.addEventListener("push", (event) => {
  console.log("PUSH EVENT RECEIVED");

  let data = {};

  if (event.data) {
    try {
      data = event.data.json();
    } catch (error) {
      data = {
        body: event.data.text()
      };
    }
  }

  console.log("PUSH DATA:", data);

  event.waitUntil(
    self.registration.showNotification(
      data.title || "Test Notification",
      {
        body: data.body || "Web Push is working!"
      }
    )
  );
});