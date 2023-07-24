getCurrentLanguage().then((currentLanguage) => {
	var savedLanguage = localStorage.getItem("language") || currentLanguage;
	setLanguageOnPageLoad(savedLanguage);
});

async function getCurrentLanguage() {
	try {
		const response = await fetch("/get-locale");
		return await response.text();
	} catch (error) {
		console.error("Failed to fetch current language");
		return "en";
	}
}

function changeLanguage(lang) {
	fetch("/change-language", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ language: lang }),
	}).then((response) => {
		if (response.ok) {
			localStorage.setItem("language", lang);
			location.reload();
		} else {
			console.error("Failed to change language");
		}
	});
}

function setLanguageOnPageLoad(language) {
	document.getElementById("language").value = language;
}
