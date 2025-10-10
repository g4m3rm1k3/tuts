document.addEventListener("DOMContentLoaded", () => {
  const tocList = document.querySelector(
    ".md-sidebar--secondary .md-nav__list"
  );
  if (!tocList) return;

  const scrollActiveIntoView = () => {
    const activeItem = tocList.querySelector(".md-nav__link--active");
    if (activeItem) {
      activeItem.scrollIntoView({ block: "center", behavior: "smooth" });
    }
  };

  // Scroll when active header changes
  const observer = new MutationObserver(scrollActiveIntoView);
  observer.observe(tocList, { attributes: true, subtree: true });

  // Scroll once after initial load
  scrollActiveIntoView();
});
