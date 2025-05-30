const dragBar = document.getElementById("drag-bar");
const leftPane = document.getElementById("tt-input");
const rightPane = document.getElementById("tt-result");
const container = document.querySelector(".container");

let isDragging = false;

dragBar.addEventListener("mousedown", (e) => {
  isDragging = true;
  document.body.style.cursor = "col-resize";
});

document.addEventListener("mousemove", (e) => {
  if (!isDragging) return;

  const containerRect = container.getBoundingClientRect();
  const dragBarWidth = dragBar.offsetWidth;
  const pointerX = e.clientX - containerRect.left;

  // Ensure pointerX is within valid bounds
  const minWidth = 100;
  const maxWidth = containerRect.width - dragBarWidth - minWidth;

  const leftWidth = Math.min(Math.max(pointerX, minWidth), maxWidth);
  const rightWidth = containerRect.width - dragBarWidth - leftWidth;

  leftPane.style.width = `${leftWidth}px`;
  rightPane.style.width = `${rightWidth}px`;
});

document.addEventListener("mouseup", () => {
  isDragging = false;
  document.body.style.cursor = "default";
});
