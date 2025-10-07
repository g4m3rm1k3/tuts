/**
 * Theme Management Module
 * Handles light/dark theme switching, system preference detection,
 * and saving the user's choice to localStorage.
 */
class ThemeManager {
  constructor() {
    this.STORAGE_KEY = "pdm-theme";
    this.init();
  }

  // Determines the initial theme based on localStorage or system settings.
  getInitialTheme() {
    const storedTheme = localStorage.getItem(this.STORAGE_KEY);
    if (storedTheme) return storedTheme;
    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      return "dark";
    }
    return "light";
  }

  // Applies a theme by setting the 'data-theme' attribute on the <html> element.
  applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const toggleButton = document.getElementById("theme-toggle");
    if (toggleButton) {
      toggleButton.innerHTML = theme === "dark" ? "☀️" : "�";
      toggleButton.setAttribute(
        "aria-label",
        `Switch to ${theme === "dark" ? "light" : "dark"} mode`
      );
    }
  }

  // Toggles the theme and saves the new preference.
  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    this.applyTheme(newTheme);
    localStorage.setItem(this.STORAGE_KEY, newTheme);
  }

  // Initializes the theme system.
  init() {
    this.applyTheme(this.getInitialTheme());
  }
}

// Create and export a single instance of the ThemeManager.
export const themeManager = new ThemeManager();
