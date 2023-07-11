var switch_theme_toggler = document.getElementById("theme-toggler");

switch_theme_toggler.addEventListener("change", toggleTheme);

function setTheme(themeName) {
	localStorage.setItem("theme", themeName);
	document.documentElement.className = themeName;
}

function toggleTheme() {
	var currentTheme = localStorage.getItem("theme");
	var newTheme = currentTheme === "theme-dark" ? "theme-light" : "theme-dark";

	setTheme(newTheme);
	switch_theme_toggler.checked = newTheme === "theme-light";
}

(function () {
	var currentTheme = localStorage.getItem("theme") || "theme-dark";
	setTheme(currentTheme);
	switch_theme_toggler.checked = currentTheme === "theme-light";
})();
