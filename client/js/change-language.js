document.addEventListener('DOMContentLoaded', fetchLanguages);  
  
async function fetchLanguages() {  
    try {  
        const [languagesResponse, currentLanguageResponse] = await Promise.all([  
            fetch(`${url_prefix}/get-languages`),  
            fetch(`${url_prefix}/get-locale`)  
        ]);  
  
        const languages = await languagesResponse.json();  
        const currentLanguage = await currentLanguageResponse.text();  
  
        const languageSelect = document.getElementById('language');  
        languages.forEach(lang => {  
            const option = document.createElement('option');  
            option.value = lang;  
            option.textContent = lang;  
            languageSelect.appendChild(option);  
        });  
  
        const savedLanguage = localStorage.getItem("language") || currentLanguage;  
        setLanguageOnPageLoad(savedLanguage);  
    } catch (error) {  
        console.error("Failed to fetch languages or current language");  
    }  
}  
  
function setLanguageOnPageLoad(language) {  
    document.getElementById("language").value = language;  
}  
  
function changeLanguage(lang) {  
    fetch(`${url_prefix}/change-language`, {  
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
