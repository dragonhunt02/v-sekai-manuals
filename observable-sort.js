  import { Runtime } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js";

  // Wait for the DOM to be ready.
  document.addEventListener('DOMContentLoaded', () => {
    const runtime = new Runtime();
    runtime.module({
      // Define an Observable cell named “sortableTable.”
      async *sortableTable() {
        // Grab the table by its id.
        const table = document.getElementById("myTable");
        if (!table) return; // If the table isn’t found, exit.

        const headers = table.querySelectorAll("th");
        const tbody = table.querySelector("tbody");

        // Attach click events for each header cell.
        headers.forEach((header, colIndex) => {
          header.style.cursor = "pointer";  // Make it obvious the header is interactive.
          header.addEventListener("click", () => {
            // Get all rows as an array.
            const rows = Array.from(tbody.querySelectorAll("tr"));

            // Sort rows based on the text content of the clicked column.
            rows.sort((a, b) => {
              const aText = a.cells[colIndex].textContent.trim();
              const bText = b.cells[colIndex].textContent.trim();
              return aText.localeCompare(bText, undefined, { numeric: true });
            });

            // Reattach the rows in sorted order.
            rows.forEach(row => tbody.appendChild(row));
          });
        });
        yield table;  // Optional: yield the table element.
      }
    });
  });
